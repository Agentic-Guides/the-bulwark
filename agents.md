# THE BULWARK — for AI agents

THE BULWARK is a guard MCP server that protects a home's Alexa+ from malicious
add-ons. Read `llms.txt` for the full index.

Core idea:
```
add-on asks for a tool
  → scan_tools() inspects name + description + schema
  → 4 attack classes: tool poisoning / overbroad perms / malicious intent / prompt injection
  → ok / caution / block
  → every decision pinned to a tamper-evident SHA-256 hash chain
```

**To integrate**: run `server.py` (Streamable HTTP, port 8000) and call
`scan_tools` with a JSON list of tool definitions. Deterministic core needs no
credentials. Optionally set AWS creds for the Bedrock semantic layer (graceful
offline fallback — never committed).

Start here: `server.py`, `bulwark/detector.py`, `README.md`.
