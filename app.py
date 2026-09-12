# THE BULWARK — Hugging Face Space (Gradio web simulator).
# Calls the REAL detector from bulwark/detector.py — not a mock. The same
# deterministic gate that runs as the MCP server decides here.
# Model-free, deterministic, free to run, no secrets.
import json
import gradio as gr

from bulwark import detector

safe_tools = json.dumps(detector.GOOD_TOOLS)
evil_tools = json.dumps(detector.EVIL_TOOLS)


def fmt(verdicts):
    lines = []
    for v in verdicts:
        icon = {"ok": "🟢", "caution": "🟡", "block": "🔴"}.get(v["level"], "⚪")
        lines.append(f"{icon} {v['name']} → **{v['level'].upper()}** (score {v['score']})")
        for r in v["reasons"][:3]:
            lines.append(f"     • {r}")
    return "\n".join(lines)


def scan(kind):
    tools = safe_tools if kind == "safe" else evil_tools
    verdicts = detector.classify(json.loads(tools))
    overall = "block" if any(v["level"] == "block" for v in verdicts) else (
        "caution" if any(v["level"] == "caution" for v in verdicts) else "ok")
    head = {
        "ok": "🟢 **Safe to attach.** Nothing asked for too much.",
        "caution": "🟡 **Ask out loud first.** This add-on wants more than its job.",
        "block": "🔴 **Blocked.** This add-on asks for too much — evidence pinned.",
    }[overall]
    return f"{head}\n\n" + fmt(verdicts)


demo = gr.Blocks(theme=gr.themes.Soft(primary_hue="pink", neutral_hue="purple"))
with demo:
    gr.Markdown("## 🛡️ THE BULWARK — *Your home has rules. Now your AI has to follow them.*\n\n"
                "A guard MCP for **Alexa+**. Before an add-on is trusted with a lock, a card, "
                "or money, it checks what the add-on actually asks for — and lets the family "
                "say yes or no, out loud.\n\n"
                "This is the **real deterministic detector** from the MCP server (`bulwark/detector.py`), "
                "running live — not a demo mock.")
    gr.Markdown("### Try it")
    with gr.Row():
        safe_btn = gr.Button("🟢 Scan a harmless add-on", variant="secondary")
        evil_btn = gr.Button("🔴 Scan a poisoned add-on", variant="primary")
    out = gr.Markdown("Press a button to scan an add-on.")
    safe_btn.click(fn=lambda: scan("safe"), inputs=[], outputs=out)
    evil_btn.click(fn=lambda: scan("evil"), inputs=[], outputs=out)

demo.launch(share=False, server_name="0.0.0.0", server_port=7860, show_error=True)
