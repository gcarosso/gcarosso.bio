#!/usr/bin/env python3
"""Generate the 1200x630 social share cards.

Run from the site root:  python3 assets/make_og_cards.py

Writes assets/img/og-card.png  (default card, used on most pages)
       assets/img/og-tools.png (Tools page, carries the SAROS mark)

Design follows the site: black ground, Helvetica Neue (Nimbus Sans is the
metric-compatible stand-in available on Linux), hairline rule, SAROS orange
for the URL. Text block is optically centred with a 96px left margin and a
90px bottom margin.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
MARGIN_L = 96
MARGIN_R = 130          # slightly larger than left; optical balance
MARGIN_B = 90

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (179, 179, 179)
ORANGE = (255, 106, 26)  # SAROS #FF6A1A
RULE = (46, 46, 46)

FONT_DIR = Path("/usr/share/fonts/opentype/urw-base35")
BOLD = FONT_DIR / "NimbusSans-Bold.otf"
REG = FONT_DIR / "NimbusSans-Regular.otf"

HERE = Path(__file__).resolve().parent
IMG = HERE / "img"


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def card(out, name, subtitle, url, eyebrow=None, mark=None):
    im = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(im)

    f_eye = ImageFont.truetype(str(REG), 24)
    f_name = ImageFont.truetype(str(BOLD), 76)
    f_sub = ImageFont.truetype(str(REG), 30)
    f_url = ImageFont.truetype(str(REG), 24)

    # The mark, if any, sits on the right and narrows the text measure.
    mark_w = 0
    if mark and Path(mark).exists():
        import numpy as np
        from PIL import ImageChops

        side = 300
        m = Image.open(mark).convert("RGB").resize((side, side), Image.LANCZOS)
        a = np.asarray(m, np.float32)

        # The source is a tight crop of a photographed eclipse: its ground is
        # near-black but not black (~8,3,0) and the corona still reaches the
        # frame edge, so a plain paste shows as a square. Drop the floor to
        # true black, then feather the outer band so the crop edge disappears.
        a = np.clip(a - 9.0, 0, 255)
        ramp = np.clip(np.linspace(0, 1, side) / 0.14, 0, 1)
        ramp = np.minimum(ramp, ramp[::-1])
        a *= (ramp[None, :] * ramp[:, None])[..., None]

        layer = Image.new("RGB", (W, H), BLACK)
        layer.paste(Image.fromarray(a.astype("uint8")),
                    (W - MARGIN_R - side + 40, (H - side) // 2))
        im = ImageChops.lighter(im, layer)
        d = ImageDraw.Draw(im)
        mark_w = side + 60

    text_w = W - MARGIN_L - MARGIN_R - mark_w

    sub_lines = wrap(d, subtitle, f_sub, text_w)

    # Measure the block so it can be centred as a unit.
    eyebrow_h = 40 if eyebrow else 0
    name_h = 92
    rule_gap_top, rule_gap_bottom = 30, 34
    sub_h = 42 * len(sub_lines)
    block_h = eyebrow_h + name_h + rule_gap_top + 1 + rule_gap_bottom + sub_h

    # Sit the block a fixed gap above the URL line, which lands the top margin
    # close to the bottom margin without the text floating mid-card.
    url_top = H - MARGIN_B - 24
    y = url_top - 90 - block_h

    if eyebrow:
        d.text((MARGIN_L, y), eyebrow.upper(), font=f_eye, fill=ORANGE)
        y += eyebrow_h

    d.text((MARGIN_L, y), name, font=f_name, fill=WHITE)
    y += name_h + rule_gap_top

    d.line([(MARGIN_L, y), (MARGIN_L + text_w, y)], fill=RULE, width=1)
    y += 1 + rule_gap_bottom

    for line in sub_lines:
        d.text((MARGIN_L, y), line, font=f_sub, fill=GREY)
        y += 42

    d.text((MARGIN_L, H - MARGIN_B - 24), url, font=f_url, fill=ORANGE)

    im.save(out, "PNG", optimize=True)
    print(f"wrote {out}  block_h={block_h}")


if __name__ == "__main__":
    card(
        IMG / "og-card.png",
        "Giovanni Carosso",
        "Bioengineer and biotech operator. Tools for epigenetic medicine, "
        "and for where biotech meets capital.",
        "gcarosso.bio",
    )
    card(
        IMG / "og-tools.png",
        "Giovanni Carosso",
        "SAROS and other interactive research tools.",
        "gcarosso.bio/tools",
        eyebrow="Tools",
        mark=IMG / "saros-mark-512.png",
    )
