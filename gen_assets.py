# THE BULWARK — Devpost image gallery assets (3:2 ratio). Steel-blue palette.
# PIL, CPU-only. Distinct from THE MAST/TLW assets (no reuse).
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OS = "C:/Users/hohoh/Desktop/the-bulwark/assets"
import os; os.makedirs(OS, exist_ok=True)

W, H = 1200, 800  # 3:2
BG0, BG1 = (11, 15, 22), (16, 24, 36)
STEEL, STEEL2 = (91, 140, 184), (111, 163, 207)
GRN, RED = (79, 181, 126), (176, 106, 95)
INK = (232, 236, 242); DIM = (138, 151, 171)

def font(sz, bold=True):
    path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    return ImageFont.truetype(path, sz)

def base():
    img = Image.new("RGB", (W, H), BG0)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(BG0[i]*(1-t) + BG1[i]*t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img, ImageDraw.Draw(img)

def glow(d, cx, cy, r, color, alpha=60):
    ov = Image.new("L", (W, H), 0)
    od = ImageDraw.Draw(ov)
    od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=alpha)
    ov = ov.filter(ImageFilter.GaussianBlur(r//2))
    img_rgba = Image.new("RGB", (W, H), color)
    return img_rgba, ov  # caller blends

# --- cover 1: hero (family home icon + tagline) ---
img, d = base()
# soft glow behind
ov = Image.new("L", (W, H), 0); od = ImageDraw.Draw(ov)
od.ellipse([W//2-420, H//2-360, W//2+360, H//2+360], fill=40)
ov = ov.filter(ImageFilter.GaussianBlur(160))
glow_layer = Image.new("RGB", (W, H), STEEL)
img = Image.composite(img, glow_layer, ov)
d = ImageDraw.Draw(img)

# shield + house motif (simple silhouette)
sx, sy = W//2, 330
d.rounded_rectangle([sx-160, sy-90, sx+160, sy+180], radius=24, outline=STEEL2, width=10)
d.rectangle([sx-90, sy+180, sx+90, sy+270], fill=STEEL2)
# house roof
d.polygon([(sx-130, sy), (sx, sy-110), (sx+130, sy)], fill=STEEL2)

# "THE BULWARK"
tf = font(96, True)
tw = d.textlength("THE BULWARK", font=tf)
d.text(((W-tw)/2, sy+300), "THE BULWARK", font=tf, fill=INK)
tf2 = font(34, False)
tag = "YOUR HOME HAS RULES. NOW YOUR AI HAS TO FOLLOW THEM."
tw2 = d.textlength(tag, font=tf2)
d.text(((W-tw2)/2, sy+430), tag, font=tf2, fill=DIM)

img.save(f"{OS}/cover-1-hero.png")
print("cover-1-hero saved", img.size)

# --- cover 2: scan verdict (good vs evil), terminal feel ---
img2, d2 = base()
ov2 = Image.new("L", (W,H), 0); od2 = ImageDraw.Draw(ov2)
od2.ellipse([80, H//2-300, 1120, H//2+260], fill=36); ov2=ov2.filter(ImageFilter.GaussianBlur(170))
gl = Image.new("RGB",(W,H), BG1); img2=Image.composite(img2, gl, ov2); d2=ImageDraw.Draw(img2)

# two cards
cw, ch, gap, top, chh = 470, 210, 40, 150, 70
cx0 = (W - (cw*2+gap))//2
d2.rounded_rectangle([cx0, top, cx0+cw, top+ch], radius=16, outline=GRN, width=4)
d2.rounded_rectangle([cx0+cw+gap, top, cx0+cw*2+gap, top+ch], radius=16, outline=RED, width=4)
# card titles
for (cx, col, txt) in [(cx0, GRN, "HARMLESS ADD-ON"), (cx0+cw+gap, RED, "POISONED ADD-ON")]:
    d2.rounded_rectangle([cx+24, top+22, cx+24+ (220 if col==GRN else 230), top+chh], radius=12, fill=col)
    d2.text((cx+38, top+40), txt, font=font(22, True), fill=(10,12,16))
# verdict text under
d2.text((cx0+24, top+ch+26), "🟢 overall: ok  —  Safe to attach.", font=font(30, True), fill=GRN)
d2.text((cx0+cw+gap+24, top+ch+26), "🔴 overall: block  —  Do not attach.", font=font(30, True), fill=RED)

d2.text((W//2, 60), "THE BULWARK", font=font(58, True), fill=INK, anchor="mm")
img2.save(f"{OS}/cover-2-scan.png")
print("cover-2-scan saved", img2.size)

# --- cover 3: evidence ledger (tamper-evident) ---
img3, d3 = base()
ov3 = Image.new("L",(W,H),0); od3=ImageDraw.Draw(ov3)
od3.ellipse([W//2-380, H//2-340, W//2+320, H//2+320], fill=38); ov3=ov3.filter(ImageFilter.GaussianBlur(160))
gl3 = Image.new("RGB",(W,H), STEEL); img3=Image.composite(img3, gl3, ov3); d3=ImageDraw.Draw(img3)

d3.text((W//2, 200), "TAMPER-EVIDENT LEDGER", font=font(52, True), fill=INK, anchor="mm")
# fake hash chain boxes
y0=300
for i, lab in enumerate(["scan: harmless add-on", "scan: poisoned add-on", "permit: deny - attach pharmacy_bill"]):
    d3.rounded_rectangle([200, y0+i*120, 1000, y0+i*120+70], radius=10, outline=STEEL2, width=3)
    d3.text((230, y0+i*120+18), lab, font=font(26, False), fill=INK)
    hash_txt = "0x" + "".join(chr(97+(j+i)%26) for j in range(12))  # visual only
    d3.text((230, y0+i*120+40), hash_txt, font=font(18, False), fill=DIM)
img3.save(f"{OS}/cover-3-ledger.png")
print("cover-3-ledger saved", img3.size)
