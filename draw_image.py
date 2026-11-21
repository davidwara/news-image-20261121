#!/usr/bin/env python3
"""Draw the world news of Saturday 21 November 2026 as one 1024x1024 page.

Fresh layout for the 21 Nov edition: black masthead, a wide lead banner on
the Shenzhen trilateral summit, a red markets-rout band, a 2x3 grid of story
cards, and a dark "also today" ticker. Deterministic: same bytes every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
RED = (185, 28, 28)
DARKRED = (127, 29, 29)
REDTINT = (253, 236, 236)
NAVY = (30, 58, 95)
BLUE = (29, 78, 216)
GREEN = (22, 101, 52)
TEAL = (13, 116, 128)
GRAY = (107, 114, 128)
BORDER = (216, 210, 196)
CARD = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    paths = {
        "serif_b": os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"),
        "serif": os.path.join(FONT_DIR, "DejaVuSerif.ttf"),
        "sans_b": os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"),
        "sans": os.path.join(FONT_DIR, "DejaVuSans.ttf"),
    }
    return ImageFont.truetype(paths[name], size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, color, max_w, leading):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def card(d, x, y, w, h, kicker, kcolor, headline, body):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=1)
    d.rectangle([x, y, x + w, y + 3], fill=kcolor)
    kx, ky = x + 14, y + 12
    d.text((kx, ky), kicker, font=font("sans_b", 12), fill=kcolor)
    hy = text_block(d, kx, ky + 20, headline, font("serif_b", 19), INK,
                    w - 28, 24)
    text_block(d, kx, hy + 4, body, font("sans", 13), (55, 55, 55),
               w - 28, 15)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 104], fill=INK)
    d.text((28, 22), "THE WORLD IN ONE PAGE", font=font("serif_b", 40),
           fill=WHITE)
    d.text((28, 70), "WORLD NEWS  •  SUMMED UP IN A SINGLE IMAGE",
           font=font("sans_b", 13), fill=(200, 200, 200))
    d.text((W - 28, 20), "SATURDAY", font=font("serif_b", 24),
           fill=WHITE, anchor="ra")
    d.text((W - 28, 50), "21 NOVEMBER 2026", font=font("sans_b", 16),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - 28, 74), "10 STORIES  •  ONE DAY", font=font("sans", 12),
           fill=(200, 200, 200), anchor="ra")
    d.rectangle([0, 104, W, 110], fill=RED)

    # ---------- lead: Shenzhen summit ----------
    y = 110
    d.text((28, y + 10), "SHENZHEN SUMMIT  —  THE NEW YALTA?",
           font=font("sans_b", 15), fill=RED)
    y = text_block(d, 28, y + 32,
                   "Trump, Xi and Putin close historic trilateral "
                   "with a joint declaration",
                   font("serif_b", 30), INK, W - 56, 36)
    y = text_block(d, 28, y + 4,
                   "The three leaders agree to pursue UN reform, boost oil "
                   "supplies and cut nuclear risks — then Trump dials into "
                   "Europe's Ukraine meeting.",
                   font("sans", 14), (55, 55, 55), W - 56, 19)
    y = text_block(d, 28, y + 8,
                   "THE TAKEAWAYS — Trump: Putin \u201ca friend of mine\u201d  •  "
                   "Xi on Taiwan: the US must \u201cdo what is right\u201d  •  "
                   "Putin, Trump target the ICC in the declaration.",
                   font("sans", 13), INK, W - 56, 17)
    d.line([28, 288, W - 28, 288], fill=BORDER, width=1)

    # ---------- markets rout band ----------
    d.rectangle([0, 296, W, 458], fill=REDTINT)
    d.rectangle([0, 296, W, 326], fill=DARKRED)
    d.text((28, 303), "WALL STREET ROUT  —  THE AI SELL-OFF",
           font=font("sans_b", 16), fill=WHITE)
    d.text((W - 28, 303), "FRIDAY'S CLOSE, REPORTED SATURDAY",
           font=font("sans_b", 12), fill=(255, 200, 200), anchor="ra")
    tiles = [
        ("DOW JONES", "48,147", "-1.9%", "-950 pts"),
        ("S&P 500", "6,910", "-3.7%", "correction"),
        ("NASDAQ", "22,618", "-5.3%", "2026 gains gone"),
    ]
    tw = 210
    for i, (name, val, pct, note) in enumerate(tiles):
        tx = 28 + i * (tw + 14)
        d.rectangle([tx, 336, tx + tw, 420], fill=WHITE, outline=BORDER)
        d.text((tx + 12, 344), name, font=font("sans_b", 12), fill=GRAY)
        d.text((tx + 12, 362), val, font=font("serif_b", 26), fill=INK)
        d.text((tx + 12, 394), pct, font=font("sans_b", 15), fill=RED)
        d.text((tx + 62, 396), note, font=font("sans", 12), fill=(55, 55, 55))
    rx = 28 + 3 * (tw + 14) + 6
    chips = [
        ("VIX  35.89", "+86% this week"),
        ("NVIDIA  -13.8%", "$125.84 — SEC probe"),
        ("ANTHROPIC  -8.5%", "$88.91, day after IPO"),
        ("BITCOIN", "below $60,000"),
    ]
    for j, (name, note) in enumerate(chips):
        cx = rx + (j % 2) * 148
        cy = 340 + (j // 2) * 42
        d.text((cx, cy), name, font=font("sans_b", 13), fill=INK)
        d.text((cx, cy + 17), note, font=font("sans", 12), fill=(55, 55, 55))
    d.text((28, 432), "Stocks lose $4 trillion in a week — the worst week "
           "since 2020.  S&P's 7th straight loss; Dow down 8% in a week.",
           font=font("sans_b", 13), fill=DARKRED)

    # ---------- 2x3 story grid ----------
    stories = [
        ("WAR IN EUROPE", RED,
         "Missiles rain on Kyiv — and land in Poland",
         "Three Kyiv bridges hit in a massive Russian strike; Kh-101 "
         "missiles fall near coalition units in Poland. Danish Gripens "
         "scrambled; Warsaw seeks NATO help."),
        ("JUSTICE", NAVY,
         "ICJ: Myanmar committed genocide of the Rohingya",
         "A historic ruling. Myanmar and China reject it as \u201cunjust\u201d; "
         "Switzerland calls it an important step forward for justice."),
        ("TECH WAR", BLUE,
         "US cleared ~900,000 AI chips for China in six months",
         "A House committee reports the sales; California's attorney "
         "general subpoenas Nvidia over its ex-CEO and China ties."),
        ("RED SEA", RED,
         "Coalition destroys Houthi missile workshops in Sana'a",
         "Six drone and missile sites hit. Saudi Arabia intercepts a "
         "Houthi missile over Riyadh; Hodeidah's ports under fire."),
        ("EUROPE", GREEN,
         "EU sends record \u20ac7.9bn to Ukraine",
         "The largest-ever aid package, plus \u20ac1bn in military aid. "
         "An EU\u2013UK summit seals farm and youth-mobility deals."),
        ("CLIMATE", TEAL,
         "Climate talks hit crunch time — no deal in sight",
         "UN negotiations stall as the deadline nears. The IEA says the "
         "Iran-war energy shock cannot be undone."),
    ]
    gx, gy = 28, 468
    cw = (W - 56 - 16) // 2
    ch = 130
    for i, (kicker, kcolor, headline, body) in enumerate(stories):
        cx = gx + (i % 2) * (cw + 16)
        cy = gy + (i // 2) * (ch + 10)
        card(d, cx, cy, cw, ch, kicker, kcolor, headline, body)

    # ---------- bottom ticker ----------
    d.rectangle([0, 884, W, H], fill=INK)
    d.text((28, 900), "ALSO TODAY", font=font("sans_b", 14), fill=(255, 90, 90))
    text_block(d, 28, 926,
               "Japan and India sign a defence pact  •  Bukele seeks a third "
               "term in El Salvador  •  Rikers Island to close by 2032 under "
               "the Mamdani plan  •  Malaysia\u2013Turkey deal moves 10,000 "
               "Rohingya  •  Pentagon: the US war with Iran cost $48.3bn",
               font("sans", 14), (220, 220, 220), W - 56, 20)
    d.line([28, 992, W - 28, 992], fill=(70, 70, 70), width=1)
    d.text((28, 999), "THE WORLD IN ONE PAGE  •  SATURDAY 21 NOVEMBER 2026  •  "
           "10 STORIES, ONE IMAGE", font=font("sans", 11), fill=(160, 160, 160))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
