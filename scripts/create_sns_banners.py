from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sns"
OUT.mkdir(parents=True, exist_ok=True)

LIME = (232, 255, 58, 255)
BLACK = (14, 14, 16, 255)
TEXT = (242, 239, 230, 255)
MUTED = (166, 163, 154, 255)
LINE = (42, 43, 48, 255)

JP_FONT = Path("/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc")
JP_FONT_MED = Path("/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc")
EN_FONT = Path("/System/Library/Fonts/HelveticaNeue.ttc")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def cover_image(path: Path, size: tuple[int, int], focus: tuple[float, float] = (0.5, 0.5)) -> Image.Image:
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    fx, fy = focus
    left = min(max(round((nw - tw) * fx), 0), nw - tw)
    top = min(max(round((nh - th) * fy), 0), nh - th)
    return src.crop((left, top, left + tw, top + th)).convert("RGBA")


def gradient(size: tuple[int, int], horizontal=True, stops=((0, 0.96), (0.5, 0.82), (1, 0.28))) -> Image.Image:
    w, h = size
    img = Image.new("RGBA", size)
    px = img.load()
    length = w - 1 if horizontal else h - 1
    for y in range(h):
      for x in range(w):
        t = (x if horizontal else y) / length
        prev = stops[0]
        nxt = stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                prev, nxt = stops[i], stops[i + 1]
                break
        span = max(nxt[0] - prev[0], 0.001)
        local = (t - prev[0]) / span
        alpha = prev[1] + (nxt[1] - prev[1]) * local
        px[x, y] = (BLACK[0], BLACK[1], BLACK[2], round(255 * alpha))
    return img


def add_grain(base: Image.Image, opacity=20) -> None:
    rnd = Random(42)
    w, h = base.size
    grain = Image.new("RGBA", (w, h))
    data = []
    for _ in range(w * h):
        v = rnd.randrange(255)
        data.append((v, v, v, opacity))
    grain.putdata(data)
    base.alpha_composite(grain)


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, tracking=5):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def draw_title_line(draw: ImageDraw.ImageDraw, xy, parts, fnt, highlight_pad=(16, 8)):
    x, y = xy
    ascent, _ = fnt.getmetrics()
    for text, mode in parts:
        if mode == "highlight":
            bbox = draw.textbbox((x, y), text, font=fnt)
            pad_x, pad_y = highlight_pad
            draw.rounded_rectangle(
                (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y),
                radius=0,
                fill=LIME,
            )
            draw.text((x, y), text, font=fnt, fill=BLACK)
        else:
            draw.text((x, y), text, font=fnt, fill=TEXT)
        x += draw.textlength(text, font=fnt)
    return y + ascent


def make_banner(spec):
    size = (spec["w"], spec["h"])
    bg = cover_image(ROOT / "assets" / "images" / spec["bg"], size, spec.get("focus", (0.5, 0.5)))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=3))

    canvas = Image.new("RGBA", size, BLACK)
    canvas.alpha_composite(bg)

    if spec["layout"] == "portrait":
        canvas.alpha_composite(gradient(size, horizontal=False, stops=((0, 0.36), (0.46, 0.72), (1, 0.97))))
        canvas.alpha_composite(gradient(size, horizontal=True, stops=((0, 0.86), (0.55, 0.52), (1, 0.22))))
    else:
        canvas.alpha_composite(gradient(size, horizontal=True, stops=((0, 0.96), (0.46, 0.82), (1, 0.28))))
        canvas.alpha_composite(gradient(size, horizontal=False, stops=((0, 0.70), (0.52, 0.22), (1, 0.92))))

    add_grain(canvas, opacity=16)
    draw = ImageDraw.Draw(canvas)

    title_font = font(JP_FONT, spec["title_size"])
    body_font = font(JP_FONT_MED, spec["body_size"])
    date_font = font(JP_FONT, spec["date_size"])
    mono_font = font(EN_FONT, spec["tag_size"])
    foot_font = font(EN_FONT, spec["foot_size"])

    x = spec["x"]
    draw.rectangle((x, spec["tag_y"], x + spec["bar_w"], spec["tag_y"] + 6), fill=LIME)
    draw_tracked(draw, (x, spec["tag_y"] + 34), "AI LEARNING COMMUNITY / TOYOTA", mono_font, MUTED, tracking=5)

    y = spec["title_y"]
    for line in spec["title"]:
        draw_title_line(draw, (x, y), line, title_font, highlight_pad=spec.get("highlight_pad", (16, 8)))
        y += spec["title_gap"]

    meta_y = spec["meta_y"]
    draw.text((x, meta_y), "2026.06.10 WED 18:00—20:00", font=date_font, fill=TEXT)
    draw.text((x, meta_y + spec["meta_gap"]), "ものづくり創造拠点 SENTAN / 参加費無料", font=body_font, fill=MUTED)

    foot_y = spec["h"] - spec["foot_bottom"]
    draw_tracked(draw, (x, foot_y), "SENTAN AX LAB / VOL.01", foot_font, LIME, tracking=4)
    draw.text((x, foot_y + spec["foot_gap"]), "AIではなく、AX。Artificial Intelligence × Transformation", font=body_font, fill=MUTED)

    ax_font = font(EN_FONT, spec["ax_size"])
    ax = "AX"
    ax_bbox = draw.textbbox((0, 0), ax, font=ax_font)
    draw.text((spec["w"] - spec["ax_right"] - (ax_bbox[2] - ax_bbox[0]), spec["h"] - spec["ax_bottom"]), ax, font=ax_font, fill=LIME)

    draw.rectangle((0, 0, spec["w"] - 1, spec["h"] - 1), outline=LINE, width=2)
    canvas.convert("RGB").save(OUT / f"{spec['name']}.png", quality=95)


SPECS = [
    {
        "name": "sentan-ax-lab-sns-16x9",
        "w": 1920,
        "h": 1080,
        "bg": "hero-ax-lab.png",
        "focus": (0.56, 0.5),
        "layout": "wide",
        "x": 92,
        "tag_y": 78,
        "bar_w": 600,
        "title_y": 336,
        "title_size": 142,
        "title_gap": 156,
        "title": [[("豊田を、", "normal"), ("AI", "highlight"), ("で", "normal")], [("もっと、面白く。", "normal")]],
        "body_size": 30,
        "date_size": 38,
        "tag_size": 24,
        "foot_size": 27,
        "meta_y": 742,
        "meta_gap": 56,
        "foot_bottom": 106,
        "foot_gap": 44,
        "ax_size": 86,
        "ax_right": 92,
        "ax_bottom": 96,
    },
    {
        "name": "sentan-ax-lab-sns-1x1",
        "w": 1080,
        "h": 1080,
        "bg": "concept-learning-community.png",
        "focus": (0.58, 0.5),
        "layout": "square",
        "x": 70,
        "tag_y": 76,
        "bar_w": 520,
        "title_y": 310,
        "title_size": 116,
        "title_gap": 126,
        "title": [[("豊田を、", "normal")], [("AI", "highlight"), ("で", "normal")], [("もっと面白く。", "normal")]],
        "body_size": 25,
        "date_size": 38,
        "tag_size": 22,
        "foot_size": 24,
        "meta_y": 724,
        "meta_gap": 54,
        "foot_bottom": 116,
        "foot_gap": 42,
        "ax_size": 82,
        "ax_right": 70,
        "ax_bottom": 88,
    },
    {
        "name": "sentan-ax-lab-sns-3x4",
        "w": 1200,
        "h": 1600,
        "bg": "event-arrival.png",
        "focus": (0.52, 0.5),
        "layout": "portrait",
        "x": 70,
        "tag_y": 86,
        "bar_w": 570,
        "title_y": 392,
        "title_size": 138,
        "title_gap": 152,
        "title": [[("豊田を、", "normal")], [("AI", "highlight"), ("で、", "normal")], [("もっと", "normal")], [("面白く。", "normal")]],
        "body_size": 31,
        "date_size": 44,
        "tag_size": 25,
        "foot_size": 28,
        "meta_y": 1124,
        "meta_gap": 62,
        "foot_bottom": 148,
        "foot_gap": 50,
        "ax_size": 104,
        "ax_right": 82,
        "ax_bottom": 112,
    },
]


for item in SPECS:
    make_banner(item)

print(f"Created {len(SPECS)} PNG banners in {OUT}")
