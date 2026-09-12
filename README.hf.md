---
title: THE BULWARK
emoji: 🛡️
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# THE BULWARK

**Your home has rules. Now your AI has to follow them.**

A guard MCP server for **Alexa+**. It sits between a home and every add-on,
checks what a tool actually asks for, and lets the family say **yes** or **no**
— out loud — before it touches a lock, a card, or money.

Built for the **Amazon Developer Hackathon (Alexa+ track)**, MCP spec
**2025-11-25** over **Streamable HTTP**, with an optional **Amazon Bedrock**
semantic layer (AWS Builder).

## Try it
- Open the web simulator and scan a **harmless** add-on → 🟢 passes
- Scan a **poisoned** add-on → 🔴 blocked, with reasons, pinned to the evidence ledger

## MCP server
The Streamable HTTP MCP server runs at `/mcp` (JSON-RPC 2.0, MCP 2025-11-25).
Tools: `scan_tools`, `permit_action`, `ledger_status`.

## Source
github.com/Agentic-Guides/the-bulwark (MIT)
