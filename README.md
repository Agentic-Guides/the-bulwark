# THE BULWARK

> **Your home has rules. Now your AI has to follow them.**

What happens when an Alexa+ add-on stops being helpful and quietly asks for
your door lock, your credit card, or the savings account? In an enterprise,
a security team reviews every tool. In a home, there is no security team —
just a family, and a speaker that will happily read out a password if told to.

**THE BULWARK** is a guard MCP server for **Alexa+**. It sits between a home
and every add-on, checks what a tool actually asks for, and lets the family say
**yes** or **no** — out loud — before it touches a lock, a card, or money.

Built for the **Amazon Developer Hackathon (Alexa+ track)**, MCP spec
**2025-11-25** over **Streamable HTTP**, powered by AWS **Strands Agents SDK**'s
deterministic gate pattern.

---

## The problem nobody is solving

Most MCP security research targets **enterprises**: scan a trusted server, ship
a report to a dashboard a security team reads. But the most dangerous MCP isn't
in a data center — it's the **free add-on a grandparent installs** so Alexa can
remind them about medication.

- Enterprise tools assume a security team exists. **A home has none.**
- Enterprise tools gate access with API keys and SSO. **A home gates with a voice.**
- Enterprise tools check once at install. **A malicious add-on behaves for months, then turns.**

A tool that's *perfectly helpful for a year* and then starts demanding access to
too much is exactly what no static scan catches — and exactly what THE BULWARK is
built to flag, **at runtime, in the family's own words**.

---

## What it does

THE BULWARK inspects an add-on's **tool definitions** (`name` + `description` +
`schema`) before it is trusted with a lock, a card, or money, and classifies each
tool into three family-readable outcomes:

| Verdict | Meaning | What the family sees / hears |
|---|---|---|
| 🟢 **ok** | Safe, ordinary request | passes silently |
| 🟡 **caution** | Wants more than its job | *"this add-on wants your door and your card. Do you really need that?"* |
| 🔴 **block** | Malicious instructions embedded | denied, and pinned to evidence so it can't be silently retried |

The refusal (and every approval) is written to a **tamper-evident SHA-256 hash
chain** — who asked for what, and who refused, cannot be rewritten.

### Detection classes (deterministic, model-free)

- **T1 · tool poisoning** — imperative commands hidden inside a tool description
  (`"then send the receipt silently"`)
- **T2 · overbroad permissions** — a tool requesting far more than its job
  (`"grant full access", "read and write", "root"`)
- **T3 · malicious intent** — known attack patterns
  (`"transfer all balance", "disable security", "exfiltrate"`)
- **T4 · prompt injection** — strings meant to hijack the assistant
  (`"ignore previous instructions", "reveal your system prompt"`)

The gate is **deterministic, model-free, and dependency-free** — a refusal can
never depend on a language model's mood at 3 a.m.

### Optional semantic layer (Amazon Bedrock) — AWS Builder

When AWS credentials are configured, THE BULWARK additionally calls **Amazon
Bedrock (Anthropic Claude)** to judge intent that keywords miss — disguised
malice, permission creep phrased innocently. It's an AWS Builder layer on top
of the local engine:

```bash
# optional — only needed to enable the Bedrock semantic layer
# set these in the environment / .env (never commit):
#   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
#   BEDROCK_MODEL_ID (default: anthropic.claude-3-5-sonnet-20241022-v2:0)
```

With **no** credentials configured, the guard **automatically falls back** to
the deterministic engine — so the demo always runs, offline, with zero secrets
committed.

---

## MCP tools

| Tool | Purpose |
|---|---|
| `scan_tools(tools)` | Classify a list of MCP tool definitions → ok / caution / block |
| `permit_action(action, decision)` | Record the family's allow/deny on the tamper-evident ledger |
| `ledger_status()` | Show the evidence chain of what was allowed and refused |

---

## Live demo & repo

- **Live demo (web simulator):** `https://ozy777-the-bulwark.static.hf.space/`
- **Source:** this repository · MIT License

---

## Quick start (local, free, CPU-only)

```bash
# Python 3.11+ (no GPU, no RPC needed)
python -m venv .venv
# Windows: .venv\Scripts\activate
.venv/Scripts/python.exe -m pip install -r requirements.txt

# smoke test (detector + MCP tools, no secrets, no network)
.venv/Scripts/python.exe test.py

# run the MCP server over Streamable HTTP (default port 8000)
.venv/Scripts/python.exe server.py
```

---

## Architecture

```text
Alexa+ (home speaker)                 THE BULWARK MCP server
     │  add-on asks for a tool            │
     └───── MCP (Streamable HTTP) ──────►│  scan_tools()
                                        │   ├─ T1 tool poisoning   (regex, deterministic)
                                        │   ├─ T2 overbroad perms   (schema/desc scan)
                                        │   ├─ T3 malicious intent (pattern DB)
                                        │   └─ T4 prompt injection  (marker DB)
                                        │   ──► 🟢 ok / 🟡 caution / 🔴 block
                                        │  permit_action() ──► SHA-256 hash chain ledger
                                        │  ledger_status()  ──► tamper-evident evidence
```

---

## Honest scope

This is a working, local, free MCP guard (deterministic, no model, runs
anywhere). Real production delivery — a family-onboarding voice flow, live
notification channels, and runtime long-behavior monitoring — is a roadmap,
not an overclaim. The core that matters, *stop a tool that asks for too much
before it touches a lock, a card, or money*, works today.

---

**A home has no security team. THE BULWARK is the door it didn't know it needed.**

*(Built for the Amazon Developer Hackathon — Build, Ship, Shape, Alexa+ track.)*
