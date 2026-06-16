from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


CARD_W, CARD_H = 938, 1313
ART_X, ART_Y = 24, 24
ART_W, ART_H = 890, 1084
BAND_Y = 1112

TEAL = (0, 78, 104)
DARK = (0, 72, 112)
PRIMARY = (35, 135, 159)
SECONDARY = (22, 183, 167)
CYAN = (80, 211, 223)
MINT = (189, 246, 224)
CREAM = (239, 248, 215)
CHANCE = (228, 224, 154)
INK = (34, 68, 82)
WHITE = (255, 255, 250)


RESTAURANT_CARDS = [
    ("pizza", "a pizza"),
    ("burger", "a burger"),
    ("pasta", "a bowl of pasta"),
    ("sushi", "a sushi roll"),
    ("tacos", "a taco"),
    ("salad", "a salad"),
    ("soup", "a bowl of soup"),
    ("steak", "a steak"),
    ("fries", "a portion of fries"),
    ("sandwich", "a sandwich"),
    ("curry", "a curry"),
    ("noodles", "a bowl of noodles"),
    ("dumplings", "a dumpling"),
    ("pancakes", "a pancake"),
    ("omelet", "an omelet"),
    ("falafel", "a falafel"),
    ("shawarma", "a shawarma"),
    ("ramen", "a bowl of ramen"),
    ("burrito", "a burrito"),
    ("lasagna", "a lasagna"),
    ("risotto", "a risotto"),
    ("kebab", "a kebab"),
    ("fish", "a fish"),
    ("chicken", "a chicken dish"),
    ("rice-bowl", "a rice bowl"),
    ("hot-dog", "a hot dog"),
    ("nachos", "a plate of nachos"),
    ("ice-cream", "an ice cream cone"),
    ("cake", "a slice of cake"),
    ("coffee", "a cup of coffee"),
]

HOME_CARDS = [
    ("sofa", "a sofa"),
    ("chair", "a chair"),
    ("table", "a table"),
    ("lamp", "a lamp"),
    ("bed", "a bed"),
    ("pillow", "a pillow"),
    ("blanket", "a blanket"),
    ("mirror", "a mirror"),
    ("clock", "a clock"),
    ("keys", "a key"),
    ("door", "a door"),
    ("window", "a window"),
    ("plant", "a plant"),
    ("books", "a book"),
    ("phone", "a phone"),
    ("laptop", "a laptop"),
    ("remote", "a remote"),
    ("towel", "a towel"),
    ("toothbrush", "a toothbrush"),
    ("soap", "a bar of soap"),
    ("shampoo", "a bottle of shampoo"),
    ("shoes", "a shoe"),
    ("coat", "a coat"),
    ("bag", "a bag"),
    ("cup", "a cup"),
    ("plate", "a plate"),
    ("fork", "a fork"),
    ("spoon", "a spoon"),
    ("fridge", "a fridge"),
    ("oven", "an oven"),
]


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def fit_font(draw, text, max_width, start_size=146):
    size = start_size
    while size > 42:
        fnt = font(size)
        bbox = draw.textbbox((0, 0), text, font=fnt)
        if bbox[2] - bbox[0] <= max_width:
            return fnt
        size -= 4
    return font(size)


def watercolor_background(seed):
    rng = random.Random(seed)
    art = Image.new("RGBA", (ART_W, ART_H), WHITE + (255,))
    wash = Image.new("RGBA", (ART_W, ART_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wash, "RGBA")
    palette = [MINT, CREAM, CHANCE, (196, 247, 229), (218, 251, 233), CYAN]
    for _ in range(42):
        color = rng.choice(palette)
        alpha = rng.randint(22, 54)
        x = rng.randint(-120, ART_W - 80)
        y = rng.randint(-80, ART_H - 80)
        w = rng.randint(160, 420)
        h = rng.randint(110, 360)
        draw.ellipse((x, y, x + w, y + h), fill=color + (alpha,))
    wash = wash.filter(ImageFilter.GaussianBlur(18))
    art.alpha_composite(wash)
    return art


def draw_restaurant_icon(draw, title, rng):
    cx, cy = ART_W // 2, ART_H // 2 - 10
    plate = (cx - 250, cy - 190, cx + 250, cy + 190)
    draw.ellipse(plate, fill=(255, 255, 250, 230), outline=INK + (170,), width=7)
    draw.ellipse((cx - 192, cy - 138, cx + 192, cy + 138), outline=PRIMARY + (115,), width=3)
    lower = title.lower()

    if "pizza" in lower:
        pts = [(cx - 120, cy - 110), (cx + 145, cy - 10), (cx - 55, cy + 135)]
        draw.polygon(pts, fill=(235, 194, 92, 230), outline=INK + (180,))
        draw.line(pts + [pts[0]], fill=INK + (180,), width=5)
        for dx, dy in [(-30, -30), (35, 5), (-20, 52)]:
            draw.ellipse((cx + dx - 22, cy + dy - 22, cx + dx + 22, cy + dy + 22), fill=(190, 64, 58, 220))
    elif "burger" in lower or "sandwich" in lower:
        layers = [(-130, -88, 130, -42, (219, 154, 72)), (-150, -35, 150, 5, (61, 96, 56)), (-135, 10, 135, 50, (116, 72, 45)), (-120, 58, 120, 104, (219, 154, 72))]
        for x1, y1, x2, y2, color in layers:
            draw.rounded_rectangle((cx + x1, cy + y1, cx + x2, cy + y2), radius=28, fill=color + (225,), outline=INK + (145,), width=4)
    elif "sushi" in lower:
        for i in range(3):
            x = cx - 135 + i * 135
            draw.ellipse((x - 48, cy - 54, x + 48, cy + 54), fill=INK + (210,))
            draw.ellipse((x - 33, cy - 38, x + 33, cy + 38), fill=WHITE + (255,))
            draw.ellipse((x - 16, cy - 19, x + 16, cy + 19), fill=(225, 106, 84, 240))
    elif any(word in lower for word in ["soup", "curry", "ramen", "risotto", "rice", "noodles", "pasta"]):
        draw.ellipse((cx - 160, cy - 105, cx + 160, cy + 105), fill=(245, 202, 112, 230), outline=INK + (165,), width=5)
        for i in range(9):
            y = cy - 55 + i * 14
            draw.arc((cx - 122, y - 26, cx + 122, y + 26), 8, 172, fill=PRIMARY + (185,), width=4)
    elif any(word in lower for word in ["taco", "burrito", "shawarma", "hot dog"]):
        draw.arc((cx - 190, cy - 120, cx + 190, cy + 180), 190, 350, fill=(222, 170, 79, 240), width=54)
        for i in range(7):
            draw.ellipse((cx - 135 + i * 44, cy - 10 + rng.randint(-28, 20), cx - 105 + i * 44, cy + 22), fill=rng.choice([(80, 138, 70), (210, 68, 58), (245, 224, 135)]) + (220,))
    elif "fries" in lower:
        draw.rectangle((cx - 95, cy - 18, cx + 95, cy + 145), fill=(190, 64, 58, 220), outline=INK + (155,), width=5)
        for i in range(8):
            x = cx - 120 + i * 34
            draw.rounded_rectangle((x, cy - 170 + rng.randint(-20, 20), x + 22, cy + 60), radius=8, fill=(237, 194, 72, 235), outline=INK + (90,))
    elif any(word in lower for word in ["ice cream", "cake", "pancake", "coffee"]):
        if "coffee" in lower:
            draw.rounded_rectangle((cx - 115, cy - 95, cx + 95, cy + 95), radius=30, fill=(246, 248, 231, 245), outline=INK + (170,), width=6)
            draw.arc((cx + 70, cy - 45, cx + 170, cy + 65), 265, 95, fill=INK + (170,), width=8)
            draw.ellipse((cx - 75, cy - 55, cx + 55, cy + 40), fill=(88, 52, 38, 235))
        else:
            for i in range(3):
                draw.ellipse((cx - 120 + i * 45, cy - 112 - i * 18, cx + 120 - i * 45, cy + 88 - i * 18), fill=rng.choice([(238, 177, 142), (239, 221, 151), (196, 247, 229)]) + (230,), outline=INK + (110,))
    else:
        for i in range(10):
            angle = i * math.pi / 5
            x = cx + math.cos(angle) * rng.randint(40, 145)
            y = cy + math.sin(angle) * rng.randint(32, 110)
            draw.ellipse((x - 28, y - 22, x + 28, y + 22), fill=rng.choice([(211, 86, 69), (80, 138, 70), (237, 194, 72), (245, 229, 178)]) + (230,), outline=INK + (80,))


def draw_home_icon(draw, title, rng):
    cx, cy = ART_W // 2, ART_H // 2
    lower = title.lower()
    color = rng.choice([PRIMARY, SECONDARY, CYAN, CHANCE, (145, 188, 166)])
    if any(word in lower for word in ["sofa", "chair", "bed", "pillow", "blanket"]):
        draw.rounded_rectangle((cx - 210, cy - 80, cx + 210, cy + 100), radius=34, fill=color + (215,), outline=INK + (175,), width=7)
        draw.rounded_rectangle((cx - 240, cy + 30, cx + 240, cy + 150), radius=34, fill=(color[0], color[1], color[2], 235), outline=INK + (175,), width=7)
        draw.line((cx - 150, cy + 150, cx - 185, cy + 205), fill=INK + (160,), width=8)
        draw.line((cx + 150, cy + 150, cx + 185, cy + 205), fill=INK + (160,), width=8)
    elif "lamp" in lower:
        draw.polygon([(cx - 120, cy - 190), (cx + 120, cy - 190), (cx + 70, cy - 20), (cx - 70, cy - 20)], fill=CHANCE + (230,), outline=INK + (165,))
        draw.line((cx, cy - 20, cx, cy + 170), fill=INK + (170,), width=9)
        draw.ellipse((cx - 105, cy + 150, cx + 105, cy + 198), fill=PRIMARY + (210,), outline=INK + (140,), width=5)
    elif any(word in lower for word in ["table", "door", "window", "mirror", "fridge", "oven"]):
        draw.rounded_rectangle((cx - 150, cy - 210, cx + 150, cy + 190), radius=18, fill=(255, 255, 250, 235), outline=INK + (175,), width=8)
        draw.rectangle((cx - 120, cy - 168, cx + 120, cy + 135), outline=color + (180,), width=8)
        if "door" in lower:
            draw.ellipse((cx + 92, cy - 5, cx + 112, cy + 15), fill=CHANCE + (230,))
    elif any(word in lower for word in ["keys", "fork", "spoon", "toothbrush", "remote"]):
        draw.line((cx - 170, cy + 80, cx + 130, cy - 120), fill=INK + (190,), width=18)
        draw.ellipse((cx - 210, cy + 88, cx - 115, cy + 183), outline=PRIMARY + (230,), width=14)
        for i in range(3):
            draw.line((cx + 60 + i * 24, cy - 80 - i * 6, cx + 105 + i * 24, cy - 30 - i * 6), fill=INK + (170,), width=9)
    elif any(word in lower for word in ["plant", "books", "phone", "laptop", "clock"]):
        if "plant" in lower:
            draw.rounded_rectangle((cx - 95, cy + 45, cx + 95, cy + 185), radius=20, fill=PRIMARY + (220,), outline=INK + (160,), width=6)
            for angle in [-65, -32, 0, 32, 65]:
                x = cx + math.cos(math.radians(angle)) * 110
                y = cy - 60 + math.sin(math.radians(angle)) * 110
                draw.ellipse((x - 58, y - 96, x + 58, y + 24), fill=SECONDARY + (210,), outline=INK + (90,))
        elif "clock" in lower:
            draw.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=WHITE + (245,), outline=INK + (185,), width=8)
            draw.line((cx, cy, cx, cy - 92), fill=INK + (180,), width=8)
            draw.line((cx, cy, cx + 74, cy + 38), fill=INK + (180,), width=8)
        else:
            draw.rounded_rectangle((cx - 190, cy - 125, cx + 190, cy + 125), radius=18, fill=WHITE + (245,), outline=INK + (175,), width=8)
            draw.rectangle((cx - 150, cy - 88, cx + 150, cy + 82), fill=(218, 251, 233, 210), outline=color + (160,), width=5)
    else:
        draw.rounded_rectangle((cx - 170, cy - 150, cx + 170, cy + 170), radius=42, fill=color + (210,), outline=INK + (170,), width=7)
        for i in range(4):
            draw.arc((cx - 120 + i * 24, cy - 98 + i * 22, cx + 120 - i * 18, cy + 98 + i * 18), 10, 170, fill=WHITE + (170,), width=5)


def crop_sheet_art(deck, index):
    sheet_number = index // 6 + 1
    sheet_position = index % 6
    sheet_path = Path("assets") / "generated-sheets" / f"{deck}-{sheet_number:02}.png"
    if not sheet_path.exists():
        return None

    sheet = Image.open(sheet_path).convert("RGB")
    cell_w = sheet.width / 3
    cell_h = sheet.height / 2
    col = sheet_position % 3
    row = sheet_position // 3
    margin_x = int(cell_w * 0.045)
    margin_y = int(cell_h * 0.06)
    crop_box = (
        int(col * cell_w + margin_x),
        int(row * cell_h + margin_y),
        int((col + 1) * cell_w - margin_x),
        int((row + 1) * cell_h - margin_y),
    )
    art = sheet.crop(crop_box)
    return art.resize((ART_W, ART_H), Image.Resampling.LANCZOS).convert("RGBA")


def draw_card(slug, title, deck, out_path, index=None):
    seed = f"{deck}:{title}"
    rng = random.Random(seed)
    card = Image.new("RGB", (CARD_W, CARD_H), TEAL)
    art = crop_sheet_art(deck, index) if index is not None else None
    if art is None:
        art = watercolor_background(seed)
        art_draw = ImageDraw.Draw(art, "RGBA")
        if deck == "restaurant":
            draw_restaurant_icon(art_draw, title, rng)
        else:
            draw_home_icon(art_draw, title, rng)
    card.paste(art.convert("RGB"), (ART_X, ART_Y))
    draw = ImageDraw.Draw(card)
    draw.rectangle((ART_X, ART_Y, ART_X + ART_W, ART_Y + ART_H), outline=(0, 54, 78), width=5)
    draw.rectangle((0, BAND_Y, CARD_W, CARD_H), fill=TEAL)
    draw.line((0, BAND_Y, CARD_W, BAND_Y), fill=CYAN, width=4)
    fnt = fit_font(draw, title, CARD_W - 90, start_size=124)
    bbox = draw.textbbox((0, 0), title, font=fnt)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((CARD_W - text_w) / 2, BAND_Y + (CARD_H - BAND_Y - text_h) / 2 - 10), title, fill=WHITE, font=fnt)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    card.save(out_path, quality=94, optimize=True)


def draw_logo(out_path):
    w, h = 760, 260
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle((18, 42, w - 18, h - 32), radius=44, fill=(255, 255, 255, 232), outline=CYAN + (160,), width=4)
    for i in range(5):
        x = 54 + i * 31
        y = 98 - i * 5
        draw.rounded_rectangle((x, y, x + 72, y + 102), radius=10, fill=(PRIMARY[0], PRIMARY[1], PRIMARY[2], 50), outline=DARK + (105,), width=3)
    title_font = font(92, bold=True)
    sub_font = font(28)
    draw.text((312, 70), "Re-Call", fill=DARK + (255,), font=title_font)
    draw.text((318, 166), "memory in motion", fill=PRIMARY + (235,), font=sub_font)
    draw.arc((204, 74, 306, 196), 112, 324, fill=SECONDARY + (230,), width=9)
    draw.polygon([(282, 76), (312, 82), (290, 104)], fill=SECONDARY + (230,))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def main():
    root = Path("assets")
    for index, (slug, label) in enumerate(RESTAURANT_CARDS):
        draw_card(slug, label, "restaurant", root / "cards" / "restaurant" / f"restaurant-{slug}.jpg", index)
    for index, (slug, label) in enumerate(HOME_CARDS):
        draw_card(slug, label, "home", root / "cards" / "home" / f"home-{slug}.jpg", index)
    draw_logo(root / "recall-logo-v2.png")


if __name__ == "__main__":
    main()
