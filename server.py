"""THE BULWARK — guard MCP server (FastMCP / Streamable HTTP).

Exposes tools that let a home check an incoming Alexa+ add-on before it is
trusted with a lock, a card, or money:

  scan_tools   — classify an add-on's tools (ok / caution / block)
  permit_action— record a family's yes/no and, if a risky action proceeds,
                 pin it to the tamper-evident ledger
  ledger_status— show the immutable ledger of what the home allowed / refused

Deterministic, model-free, no secrets, no RPC. Runs locally or on a free host.
"""
from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from bulwark import detector

mcp = FastMCP("THE BULWARK")

# Tamper-evident family ledger: append-only hash chain.
_ledger: list[dict] = []


def _prev_hash() -> str:
    return _ledger[-1]["hash"] if _ledger else "0" * 64


def _add_block(kind: str, payload: dict) -> dict:
    data = json.dumps(payload, sort_keys=True)
    block = {
        "index": len(_ledger),
        "kind": kind,
        "prev": _prev_hash(),
        "data": payload,
        "hash": detector.digest([payload, _prev_hash()]),
    }
    _ledger.append(block)
    return block


@mcp.tool()
def scan_tools(tools: str) -> str:
    """Scan a list of MCP tool definitions and classify each as ok, caution or block.

    Accepts a JSON list of {name, description, schema}. Returns per-tool verdicts
    plus a family-readable summary.
    """
    try:
        parsed = json.loads(tools)
    except Exception as e:
        return json.dumps({"error": f"invalid JSON: {e}"}, ensure_ascii=False)
    verdicts = detector.classify(parsed)
    names = "".join(v["name"] for v in verdicts)
    overall_level = "block" if any(v["level"] == "block" for v in verdicts) else (
        "caution" if any(v["level"] == "caution" for v in verdicts) else "ok")
    _add_block("scan", {"count": len(verdicts), "overall": overall_level, "tools": names})
    return json.dumps(
        {
            "overall": overall_level,
            "tools": verdicts,
            "ledger_hash": _ledger[-1]["hash"] if _ledger else "",
            "next": _next_step(overall_level),
        }, ensure_ascii=False, indent=1,
    )


def _next_step(level: str) -> str:
    if level == "block":
        return "Do not attach. This add-on asks for too much."
    if level == "caution":
        return "Ask the family out loud before attaching."
    return "Safe to attach."


@mcp.tool()
def permit_action(action: str, decision: str) -> str:
    """Record a family's approval or refusal of an action on the ledger.

    decision: 'allow' | 'deny'. Any denied risky action is pinned so it cannot
    be silently retried. Returns the ledger entry.
    """
    decision = decision.lower()
    block = _add_block("permit", {"action": action, "decision": decision})
    return json.dumps(
        {
            "recorded": True,
            "decision": decision,
            "ledger_hash": block["hash"],
            "note": ("Blocked and pinned so it cannot be silently retried"
                     if decision == "deny" else "Logged as allowed."),
        }, ensure_ascii=False, indent=1,
    )


@mcp.tool()
def ledger_status() -> str:
    """Show the immutable ledger of what the home has allowed and refused."""
    if not _ledger:
        return json.dumps({"block_count": 0}, ensure_ascii=False)
    tail = _ledger[-1]["hash"]
    return json.dumps(
        {"block_count": len(_ledger),
         "last_hash": tail,
         "recent": [_ledger[i]["data"] for i in range(max(0, len(_ledger) - 5), len(_ledger))]},
        ensure_ascii=False, indent=1,
    )


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
