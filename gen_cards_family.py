# Devpost card images in THE LAST WORD's Neo-Brutalist family style.
# Cream bg + black heavy sans + hard colored drop-shadow + ruler ticks + scan line.
# Accent color varies per brand (mast=pink/purple, bulwark=steel blue). 1200x800 (3:2).
from PIL import Image, ImageDraw, ImageFont
import os

CREAM = (242, 240, 235)
BLACK = (10, 10, 12)
GRAY  = (200, 200, 200)
LIGHT = (240, 210, 212)

def font_heavy(sz):
    for p in ("C:/Windows/Fonts/impact.ttf",):
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def font_body(sz, bold=True):
    p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try: return ImageFont.truetype(p, sz)
    except: return ImageFont.load_default()

def make(kicker, title, accent, scan_color, out):
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # dot texture
    for x in range(14, W, 26):
        for y in range(14, H, 26):
            d.point((x, y), fill=(210, 208, 202))

    # corner box (tech frame)
    d.rectangle([30, 30, 130, 130], outline=BLACK, width=4)

    # ruler ticks top & bottom
    for x in range(0, W, 24):
        d.line([(x, 40), (x, 48)], fill=GRAY, width=2)
        d.line([(x, H-48), (x, H-40)], fill=GRAY, width=2)

    # kicker (subtitle)
    kf = font_body(54, True)
    d.text((80, 250), kicker, font=kf, fill=BLACK)

    # accent underline bar (hard glow)
    bar_h = 14
    d.rectangle([82, 330, 1118, 330+bar_h], fill=accent)

    # main title with hard offset shadow (accent color) + black on top
    tf = font_heavy(150)
    ts = d.textlength(title, font=tf)
    tx = (W - ts) / 2
    ty = 420
    # hard shadow: draw title in accent, offset down-right few px, then black on top
    d.text((tx+10, ty+12), title, font=tf, fill=accent)
    d.text((tx, ty), title, font=tf, fill=BLACK)

    # scan line across lower half
    d.rectangle([0, ty+180, W, ty+186], fill=scan_color)

    # repo line at bottom
    rl = "AMAZON DEVELOPER HACKATHON · ALEXA+ · MCP"
    rf = font_body(26, True)
    rw = d.textlength(rl, font=rf)
    d.text(((W-rw)/2, H-92), rl, font=rf, fill=(120, 120, 120))

    img.save(out)
    print("saved", out, img.size)

# THE MAST — pink/purple accent family
make("AGENTS FOR HUMANS · AWS",
     "THE MAST",
     (200, 30, 90),        # pink-red
     (240, 200, 210),      # light pink
     "C:/Users/hohoh/Desktop/the-mast/assets/card-mast.png")

# THE BULWARK — steel blue accent family
make("AMAZON HACKATHON · ALEXA+",
     "THE BULWARK",
     (60, 120, 190),       # steel blue
     (190, 210, 235),      # light blue
     "C:/Users/hohoh/Desktop/the-bulwark/assets/card-bulwark.png")
