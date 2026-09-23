"""Build Safe_and_Continual/Safe_and_Continual.pdf from SAFE_AND_CONTINUAL.md (a copy of AI_Safety/build/build_pdf.py with the paths and title changed) (a small Markdown subset) with fpdf2.
Supported: '# ', '## ', '### ' headings; paragraphs with **bold**, *italic*, `code`; '- ' bullets and '1. ' numbered lists (wrapped lines indented); pipe tables; fenced code
blocks (``` ... ```, or ```include:PATH[:START-END] to embed a repository file); '$$ ... $$' display mathematics on one line
(rendered with matplotlib mathtext); '> ' callouts (the fifth-grader boxes); '![caption](path)' figures. Fonts: DejaVu
from matplotlib's bundled set. Run: uv run python Safe_and_Continual/build/build_pdf.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from fpdf import FPDF  # noqa: E402
from fpdf.fonts import FontFace  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DOC_DIR = ROOT / "Safe_and_Continual"
MD = DOC_DIR / "SAFE_AND_CONTINUAL.md"
OUT = DOC_DIR / "Safe_and_Continual.pdf"
MATH_DIR = DOC_DIR / "build" / "math"
FONT_DIR = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
INK = (11, 11, 11); INK2 = (82, 81, 78); BOX = (234, 242, 252); CODEBG = (246, 246, 244); RULE = (200, 199, 193)


class Doc(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(18, 16, 18); self.set_auto_page_break(True, margin=18)
        self.add_font("DV", "", str(FONT_DIR / "DejaVuSans.ttf")); self.add_font("DV", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
        self.add_font("DV", "I", str(FONT_DIR / "DejaVuSans-Oblique.ttf")); self.add_font("DV", "BI", str(FONT_DIR / "DejaVuSans-BoldOblique.ttf"))
        self.add_font("DVM", "", str(FONT_DIR / "DejaVuSansMono.ttf")); self.add_font("DVM", "B", str(FONT_DIR / "DejaVuSansMono-Bold.ttf"))
        self.set_font("DV", "", 9.5); self.set_text_color(*INK)
        self.set_creation_date(dt.datetime(2026, 9, 23, tzinfo=dt.timezone.utc))   # a fixed date so two builds are byte-identical (R9)
        self.set_title("Safe and Continual: how the agents are modelled, where they fail and why"); self.set_author("CRR re-validation repository")

    def footer(self):
        self.set_y(-12); self.set_font("DV", "", 7.5); self.set_text_color(*INK2)
        self.cell(0, 6, f"Safe and Continual — CRR re-validation repository, 2026-09-23 — page {self.page_no()}", align="C")
        self.set_text_color(*INK)

    @property
    def usable(self):
        return self.w - self.l_margin - self.r_margin


def inline(text: str) -> str:
    """Markdown inline -> the HTML subset fpdf2's write_html understands."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def render_math(expr: str, size: float = 12) -> Path:
    MATH_DIR.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(expr.encode()).hexdigest()[:16]; out = MATH_DIR / f"m_{key}.png"
    if not out.exists():
        fig = plt.figure(figsize=(0.01, 0.01), facecolor="white")
        fig.text(0, 0, f"${expr}$", fontsize=size, color="black")
        fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.04, facecolor="white"); plt.close(fig)
    return out


def paragraph(pdf: Doc, text: str, size=9.5, color=INK):
    pdf.set_font("DV", "", size); pdf.set_text_color(*color)
    pdf.write_html(f"<p>{inline(text)}</p>", font_family="DV", tag_styles={"code": FontFace(family="DVM")}); pdf.ln(1.2); pdf.set_text_color(*INK)


def heading(pdf: Doc, level: int, text: str):
    sizes = {1: 17, 2: 13, 3: 10.5}
    if level == 1 and pdf.page_no() > 1:
        pdf.add_page()
    pdf.ln(3 if level > 1 else 1); pdf.set_font("DV", "B", sizes[level]); pdf.set_text_color(*INK)
    pdf.multi_cell(0, sizes[level] * 0.5, text, new_x="LMARGIN", new_y="NEXT"); pdf.ln(1.5)
    if level == 1:
        pdf.set_draw_color(*RULE); pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + pdf.usable, pdf.get_y()); pdf.ln(2.5)


def list_html(items, ordered):
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{inline(t)}" + "".join(list_html(sub, o) for sub, o in subs) + "</li>" for t, subs in items) + f"</{tag}>"


def bullets(pdf: Doc, items, ordered: bool = False):
    pdf.set_font("DV", "", 9.5)
    pdf.write_html(list_html(items, ordered), font_family="DV", tag_styles={"code": FontFace(family="DVM")}); pdf.ln(1)


MARK = re.compile(r"^( *)(- |\d+\. )(.*)$")


def list_items(src: list[str], i: int, base: int = 0):
    """A Markdown list starting at line i, at indentation base: items (text, [(sublist, ordered), ...]); a line indented
    deeper than a marker and not itself a marker continues the current item; a deeper marker opens a nested list."""
    items, ordered = [], None
    while i < len(src):
        m = MARK.match(src[i])
        if not m or len(m.group(1)) < base: break
        if len(m.group(1)) > base:
            if not items: break
            sub, i, o = list_items(src, i, len(m.group(1))); items[-1][1].append((sub, o)); continue
        if ordered is None: ordered = m.group(2) != "- "
        text = m.group(3); i += 1
        while i < len(src) and src[i].startswith(" ") and src[i].strip() and not MARK.match(src[i]):
            text += " " + src[i].strip(); i += 1
        items.append((text, []))
    return items, i, bool(ordered)


def plain(text: str) -> str:
    return re.sub(r"`([^`]+)`", r"\1", re.sub(r"\*\*?([^*]+?)\*\*?", r"\1", text))


def callout(pdf: Doc, text: str):
    text = plain(text); pdf.set_font("DV", "", 9.2); x = pdf.l_margin; w = pdf.usable - 6
    lines = pdf.multi_cell(w, 4.6, "In plain words. " + text, dry_run=True, output="LINES")
    hgt = 4.6 * len(lines) + 4
    if pdf.get_y() + hgt > pdf.h - pdf.b_margin: pdf.add_page()
    start = pdf.get_y(); pdf.set_fill_color(*BOX); pdf.rect(x, start, pdf.usable, hgt, style="F")
    pdf.set_xy(x + 3, start + 2); pdf.set_font("DV", "B", 9.2); pdf.write(4.6, "In plain words. "); pdf.set_font("DV", "", 9.2)
    pdf.write(4.6, text); pdf.set_y(start + hgt + 2)


def table(pdf: Doc, rows: list[list[str]]):
    ncol = max(len(r) for r in rows); rows = [[plain(c) for c in r] + [""] * (ncol - len(r)) for r in rows]
    size = 7.4
    while True:
        pdf.set_font("DV", "", size)
        # a column can never be narrower than its longest unbreakable word
        min_w = [max(pdf.get_string_width(max(c.split() or [""], key=len)) for c in (r[j] for r in rows)) + 2.2 for j in range(ncol)]
        if sum(min_w) <= pdf.usable or size <= 5.5:
            break
        size -= 0.4
    tot_len = [sum(min(len(r[j]), 80) for r in rows) for j in range(ncol)]
    spare = max(pdf.usable - sum(min_w), 0.0); tl = sum(tot_len) or 1
    widths = [m + spare * t / tl for m, t in zip(min_w, tot_len)]
    scale = pdf.usable / sum(widths); widths = [w * scale for w in widths]
    with pdf.table(col_widths=widths, text_align="LEFT", line_height=size * 0.5, padding=0.8, borders_layout="HORIZONTAL_LINES",
                   headings_style=FontFace(emphasis="BOLD", fill_color=(236, 235, 231))) as t:
        for r in rows:
            row = t.row()
            for c in r:
                row.cell(c)
    pdf.ln(2)


def code(pdf: Doc, lines: list[str], title: str | None = None):
    if title:
        pdf.set_font("DV", "B", 8.5); pdf.multi_cell(0, 4.5, title, new_x="LMARGIN", new_y="NEXT"); pdf.ln(0.5)
    pdf.set_font("DVM", "", 6.3); pdf.set_fill_color(*CODEBG)
    for ln in lines:
        pdf.multi_cell(0, 2.9, ln.rstrip("\n").replace("\t", "    ") or " ", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def figure(pdf: Doc, path: Path, caption: str):
    if not path.exists():
        raise FileNotFoundError(path)
    from PIL import Image
    with Image.open(path) as im: w, h = im.size
    width = pdf.usable; height = width * h / w
    if height > 150: height = 150; width = height * w / h
    if pdf.get_y() + height + 14 > pdf.h - pdf.b_margin: pdf.add_page()
    pdf.image(str(path), x=pdf.l_margin + (pdf.usable - width) / 2, w=width); pdf.ln(1.5)
    pdf.set_font("DV", "I", 8.2); pdf.set_text_color(*INK2); pdf.write_html(f"<p>{inline(caption)}</p>", font_family="DV", tag_styles={"code": FontFace(family="DVM")}); pdf.set_text_color(*INK); pdf.ln(2)


def display_math(pdf: Doc, expr: str):
    png = render_math(expr)
    from PIL import Image
    with Image.open(png) as im: w, h = im.size
    width_mm = w / 300 * 25.4; height_mm = h / 300 * 25.4
    if width_mm > pdf.usable: height_mm *= pdf.usable / width_mm; width_mm = pdf.usable
    if pdf.get_y() + height_mm + 6 > pdf.h - pdf.b_margin: pdf.add_page()
    pdf.image(str(png), x=pdf.l_margin + (pdf.usable - width_mm) / 2, w=width_mm); pdf.ln(2.5)


def include(spec: str) -> tuple[list[str], str]:
    path, _, rng = spec.partition(":")
    lines = (ROOT / path).read_text().splitlines()
    if rng:
        a, b = rng.split("-"); lines = lines[int(a) - 1:int(b)]
        return lines, f"{path} (lines {a}–{b})"
    return lines, path


def build():
    pdf = Doc(); pdf.add_page()
    src = MD.read_text().splitlines(); i = 0; n = len(src)
    while i < n:
        line = src[i]
        if not line.strip():
            i += 1; continue
        if line.startswith("```"):
            spec = line[3:].strip(); i += 1
            if spec.startswith("include:"):
                lines, title = include(spec[len("include:"):]); code(pdf, lines, title)
                while i < n and not src[i].startswith("```"): i += 1
                i += 1; continue
            buf = []
            while i < n and not src[i].startswith("```"): buf.append(src[i]); i += 1
            i += 1; code(pdf, buf); continue
        if line.startswith("$$"):
            expr = line.strip().strip("$").strip(); display_math(pdf, expr); i += 1; continue
        if line.startswith("### "): heading(pdf, 3, line[4:].strip()); i += 1; continue
        if line.startswith("## "): heading(pdf, 2, line[3:].strip()); i += 1; continue
        if line.startswith("# "): heading(pdf, 1, line[2:].strip()); i += 1; continue
        if line.startswith("!["):
            m = re.match(r"!\[(.*)\]\((.*)\)", line.strip()); figure(pdf, DOC_DIR / m.group(2), m.group(1)); i += 1; continue
        if line.startswith("> "):
            buf = []
            while i < n and src[i].startswith("> "): buf.append(src[i][2:]); i += 1
            callout(pdf, " ".join(buf)); continue
        if line.strip() == "---":
            i += 1; continue
        if line.startswith("- ") or re.match(r"^\d+\. ", line):
            items, i, ordered = list_items(src, i); bullets(pdf, items, ordered); continue
        if line.startswith("|"):
            rows = []
            while i < n and src[i].startswith("|"):
                cells = [c.strip() for c in src[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells): rows.append(cells)
                i += 1
            table(pdf, rows); continue
        buf = []
        while i < n and src[i].strip() and not re.match(r"^(#|\||- |> |!\[|```|\$\$|\d+\. )", src[i]): buf.append(src[i].strip()); i += 1
        paragraph(pdf, " ".join(buf))
    pdf.output(str(OUT))
    print(f"wrote {OUT.relative_to(ROOT)}: {pdf.page_no()} pages, {OUT.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(build())
