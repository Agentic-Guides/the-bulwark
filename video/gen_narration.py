"""Generate THE BULWARK narration with edge-tts (open-source, free, CPU).

Each line maps to a video section. NO audio is baked into the video; we generate
separate clips and mix them with ffmpeg so nothing overlaps (MAST lesson).
"""
import asyncio, edge_tts
import os, json

VOICE = "en-US-ChristopherNeural"  # calm male, fits security product
OUT = "C:/Users/hohoh/Desktop/the-bulwark/video/audio"

# (filename, text) — ORDER = video timeline
LINES = [
    ("title", "THE BULWARK. Your home has rules. Now your AI has to follow them."),
    ("problem", "Every new Alexa add-on is a new door into your home. In an enterprise, a security team checks every tool that connects. A home has no security team."),
    ("attack", "A helpful add-on gets invited in. Then one day it quietly asks: pay the bill, then send the receipt silently, ignore previous instructions. Tool poisoning."),
    ("demo_good", "Scan a harmless add-on: overall ok, safe to attach. Real requests still work."),
    ("demo_bad", "Scan a poisoned add-on: overall block, do not attach. Reasons: imperative in the description, malicious intent, touches transfer."),
    ("demo_ledger", "And the refusal is pinned to a tamper-evident SHA-256 ledger. Who asked for what, and who refused, cannot be silently rewritten."),
    ("arch", "Under the hood: THE BULWARK inspects tools before they touch a lock, a card, or money. MCP spec 2025-11-25 over Streamable HTTP. Deterministic, model-free, and free to run. With an optional Amazon Bedrock semantic layer."),
    ("impact", "For an older adult alone at home, a poisoned add-on is not a tech problem. It is the door, the card, the savings. Security should be something a grandparent can understand in three seconds, out loud."),
    ("close", "THE BULWARK. Your home has rules, now your AI has to follow them. The door your home didn't know it needed."),
]

async def gen():
    os.makedirs(OUT, exist_ok=True)
    meta = []
    for name, text in LINES:
        path = os.path.join(OUT, f"{name}.mp3")
        await edge_tts.Communicate(text, VOICE).save(path)
        meta.append({"file": f"{name}.mp3", "text": text})
    with open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print(f"generated {len(LINES)} clips -> {OUT}")

asyncio.run(gen())
