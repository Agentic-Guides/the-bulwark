# Devpost project card images — THE MAST (pink/purple) & THE BULWARK (steel-blue).
# Dark bg + gradient glow + glassmorphism, 3:2 (1200x800). CPU-only PIL.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def font(sz, bold=True):
    for p in (["C:/Windows/Fonts/arialbd.ttf"] if bold else ["C:/Windows/Fonts/arial.ttf"]):
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def make(name, tagline, c1, c2, glow_col, icon_fn, out):
    W, H = 1200, 800
    # dark radial background
    img = Image.new("RGB", (W, H), (10, 12, 17))
    # big blurred glow blobs (gradient glow)
    for (gx, gy, gr, gc) in icon_fn["glows"]:
        ov = Image.new("L", (W, H), 0); od = ImageDraw.Draw(ov)
        od.ellipse([gx-gr, gy-gr, gx+gr, gy+gr], fill=90)
        ov = ov.filter(ImageFilter.GaussianBlur(gr//2))
        layer = Image.new("RGB", (W, H), gc)
        img = Image.composite(img, layer, ov)
    d = ImageDraw.Draw(img)

    # faint dotted grid / scanlines for texture
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            d.point((x, y), fill=(255, 255, 255, 8) if False else (30, 36, 50))

    # main icon: frosted glass card
    icon = Image.new("RGBA", (W, H), (0,0,0,0))
    idr = ImageDraw.Draw(icon)
    iw, ih, ix, iy = 300, 300, (W-300)//2, 170
    idr.rounded_rectangle([ix, iy, ix+iw, iy+ih], radius=34, fill=(255,255,255,26), outline=(255,255,255,70), width=3)
    icon = icon.filter(ImageFilter.GaussianBlur(0.6))
    img = img.convert("RGBA"); img.alpha_composite(icon); img = img.convert("RGB"); d = ImageDraw.Draw(img)

    # icon glyph
    idr2 = ImageDraw.Draw(Image.new("RGBA",(W,H),(0,0,0,0)))  # reuse
    # draw symbol inside glass
    if "glyph" in icon_fn:
        gf = icon_fn["glyph"]
        if gf == "mast":  # mast / ship mast + waves
            mcx = W//2; my = 320
            d.line([(mcx, my-70),(mcx, my+80)], fill=(235,240,250), width=12)
            d.polygon([(mcx-26, my-110),(mcx, my-150),(mcx+26, my-110)], fill=(235,240,250))
            for k,off in enumerate([-30,0,30]):
                d.arc([mcx-110+off, my+30, mcx+110+off, my+130], 200, 340, fill=(120,130,160), width=6)
        elif gf == "shield":  # shield + house
            sx = W//2; sy = 320
            d.polygon([(sx-90, sy-80),(sx, sy-160),(sx+90, sy-80),(sx+90, sy+40),(sx, sy+100),(sx-90, sy+40)], outline=(200,225,245), width=9)
            # house roof inside
            d.polygon([(sx-40, sy-10),(sx, sy-55),(sx+40, sy-10)], fill=(200,225,245))
            d.rectangle([sx-30, sy-5, sx+30, sy+40], fill=(200,225,245))

    # accent underline
    grad = Image.new("RGB", (1, H), (0,0,0))
    # title
    tf = font(78, True)
    tw = d.textlength(name, font=tf)
    d.text(((W-tw)/2, 560), name, font=tf, fill=(235,240,250))
    # gradient tagline strip (glass)
    tg = font(30, False)
    ttag = tagline
    ttw = d.textlength(ttag, font=tg)
    # gradient bar accent
    bar = Image.new("RGB",(W,H),(0,0,0)); bd=ImageDraw.Draw(bar)
    for x in range(120, W-120):
        t=(x-120)/((W-120)-120); col=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))
        bd.line([(x, 700),(x,704)], fill=col)
    bar=bar.filter(ImageFilter.GaussianBlur(0.5))
    img=Image.composite(img, bar, Image.new("L",(W,H),255))
    d=ImageDraw.Draw(img)
    d.text(((W-ttw)/2, 716), ttag, font=tg, fill=(150,165,190))
    img.save(out)
    print("saved", out, img.size)

# ---- THE MAST ----
make("THE MAST",
     "Your past self sets the rules. Your future self can't break them.",
     (225, 29, 72), (124, 58, 237), (124, 58, 237),
     {"glows":[(W:=(1200)//2 -0, 320, 220, (124,58,237)) for _ in [0]] if False else [(600,280,240,(124,58,237)),(950,600,200,(225,29,72)),(250,600,180,(225,29,72))],
      "glyph":"mast"},
     "C:/Users/hohoh/Desktop/the-mast/assets/devpost-mast.png")

# ---- THE BULWARK ----
make("THE BULWARK",
     "Your home has rules. Now your AI has to follow them.",
     (91,140,184), (111,163,207), (91,140,184),
     {"glows":[(600,280,240,(91,140,184)),(950,600,200,(79,181,126)),(250,600,180,(91,140,184))],
      "glyph":"shield"},
     "C:/Users/hohoh/Desktop/the-bulwark/assets/devpost-bulwark.png")
