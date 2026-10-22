"""Markdown → DOCX 转换器（中文排版版）。

用法：
    python md2docx.py <输入.md> <输出.docx> [--title "文档标题"]
    python md2docx.py --merge <out.docx> <in1.md> <in2.md> ...

支持：#~#### 标题、段落、- 列表、1. 有序列表、| 表格 |、> 引用、``` 代码块、
**粗体**、*斜体*、`行内代码`、[文字](链接)、--- 分隔线。
中文使用 宋体/黑体 + w:eastAsia；A4 页面；页脚含页码。
"""
import os
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_FONT_CN = "宋体"
HEAD_FONT_CN = "黑体"
BODY_FONT_EN = "Times New Roman"
MONO_FONT = "Consolas"
BODY_SIZE = Pt(10.5)   # 五号
TABLE_SIZE = Pt(9)


# ---------------------------------------------------------------- 底层样式工具
def set_run_font(run, cn=BODY_FONT_CN, en=BODY_FONT_EN, size=None, bold=None, color=None):
    run.font.name = en
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), en)
    rfonts.set(qn("w:hAnsi"), en)
    rfonts.set(qn("w:eastAsia"), cn)
    if size is not None:
        run.font.size = size
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def style_font(style, cn, en, size, bold=False, color=None):
    style.font.name = en
    style.font.size = size
    style.font.bold = bold
    if color is not None:
        style.font.color.rgb = color
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi"):
        rfonts.set(qn(attr), en)
    rfonts.set(qn("w:eastAsia"), cn)


def shade(paragraph_or_cell, hex_fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    el = paragraph_or_cell._element
    ppr = el.get_or_add_pPr() if hasattr(el, "get_or_add_pPr") else el.get_or_add_tcPr()
    ppr.append(shd)


def add_page_number_footer(section, label="菌护禾 · 金种子杯 · 2026-10-22"):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(label + "    第 ")
    set_run_font(run, size=Pt(8), color=RGBColor(0x80, 0x80, 0x80))
    fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = "PAGE"
    fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
    r = p.add_run(); set_run_font(r, size=Pt(8), color=RGBColor(0x80, 0x80, 0x80))
    r._element.append(fld_begin); r._element.append(instr); r._element.append(fld_end)
    run2 = p.add_run(" 页")
    set_run_font(run2, size=Pt(8), color=RGBColor(0x80, 0x80, 0x80))


def init_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.2)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.4)
    sec.right_margin = Cm(2.2)
    normal = doc.styles["Normal"]
    style_font(normal, BODY_FONT_CN, BODY_FONT_EN, BODY_SIZE)
    normal.paragraph_format.line_spacing = 1.45
    normal.paragraph_format.space_after = Pt(4)
    for name, size in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12), ("Heading 4", 11)):
        st = doc.styles[name]
        style_font(st, HEAD_FONT_CN, BODY_FONT_EN, Pt(size), bold=True,
                   color=RGBColor(0x1F, 0x3B, 0x2E))
        st.paragraph_format.space_before = Pt(12 if name == "Heading 1" else 8)
        st.paragraph_format.space_after = Pt(6)
    add_page_number_footer(sec)
    return doc


# ---------------------------------------------------------------- 行内格式
INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`|\[[^\]\n]+\]\([^)\n]+\))")


def add_inline(paragraph, text, base_size=None, bold=False):
    for token in INLINE.split(text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**") and len(token) > 4:
            run = paragraph.add_run(token[2:-2])
            set_run_font(run, size=base_size, bold=True)
        elif token.startswith("`") and token.endswith("`") and len(token) > 2:
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, cn=BODY_FONT_CN, en=MONO_FONT, size=Pt(9.5))
        elif token.startswith("*") and token.endswith("*") and len(token) > 2:
            run = paragraph.add_run(token[1:-1])
            run.italic = True
            set_run_font(run, size=base_size, bold=bold)
        elif token.startswith("[") and "](" in token:
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            label, url = m.group(1), m.group(2)
            run = paragraph.add_run(label)
            set_run_font(run, size=base_size, bold=bold, color=RGBColor(0x1E, 0x4E, 0x8C))
            run2 = paragraph.add_run(f"（{url}）" if url.startswith("http") else "")
            set_run_font(run2, size=Pt(8), color=RGBColor(0x80, 0x80, 0x80))
        else:
            run = paragraph.add_run(token)
            set_run_font(run, size=base_size, bold=bold)


# ---------------------------------------------------------------- 块级解析
def parse_blocks(lines):
    blocks, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i].rstrip("\n")
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            blocks.append(("code", code))
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            blocks.append(("h", len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if re.match(r"^[-*_]{3,}$", s):
            i += 1
            continue
        if s.startswith("|") and s.count("|") >= 2:
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.match(r"^:?-{2,}:?$", c.replace(" ", "")) or c == "" for c in row):
                    rows.append(row)
                i += 1
            if rows:
                blocks.append(("table", rows))
            continue
        if s.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(("quote", " ".join(quote)))
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", s)
        if m:
            blocks.append(("ol", m.group(2).strip()))
            i += 1
            continue
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            blocks.append(("ul", m.group(1).strip()))
            i += 1
            continue
        blocks.append(("p", s))
        i += 1
    return blocks


def render_markdown(doc, text):
    lines = text.split("\n")
    first_heading = True
    for block in parse_blocks(lines):
        kind = block[0]
        if kind == "h":
            level, title = block[1], block[2]
            if level == 1 and first_heading:
                p = doc.add_paragraph(style="Title")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_inline(p, title, base_size=Pt(22))
                p.paragraph_format.space_after = Pt(18)
                first_heading = False
            else:
                doc.add_heading(level=min(level, 4))
                p = doc.paragraphs[-1]
                add_inline(p, title)
        elif kind == "p":
            p = doc.add_paragraph()
            add_inline(p, block[1])
        elif kind == "ul":
            p = doc.add_paragraph(style="List Bullet")
            add_inline(p, block[1])
        elif kind == "ol":
            p = doc.add_paragraph(style="List Number")
            add_inline(p, block[1])
        elif kind == "quote":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            run = p.add_run("┃ ")
            set_run_font(run, size=Pt(10), color=RGBColor(0x4F, 0x7A, 0x5E))
            add_inline(p, block[1], base_size=Pt(10))
        elif kind == "code":
            for cl in block[1]:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.5)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                run = p.add_run(cl if cl else " ")
                set_run_font(run, cn=BODY_FONT_CN, en=MONO_FONT, size=Pt(9))
                shade(p, "F2F2F2")
            doc.add_paragraph().paragraph_format.space_after = Pt(2)
        elif kind == "table":
            rows = block[1]
            cols = max(len(r) for r in rows)
            table = doc.add_table(rows=len(rows), cols=cols)
            table.style = "Table Grid"
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False
            # 固定列宽：按内容长度加权，总宽 = 版心宽度，避免表格溢出页边距
            sec = doc.sections[0]
            avail_cm = (sec.page_width - sec.left_margin - sec.right_margin) / 360000.0
            weights = []
            for ci in range(cols):
                longest = 4
                for row in rows:
                    if ci < len(row):
                        longest = max(longest, min(len(re.sub(r"\*\*|`", "", row[ci])), 40))
                weights.append(longest)
            total = sum(weights)
            widths = [max(1.4, avail_cm * w / total) for w in weights]
            factor = avail_cm / sum(widths)
            widths = [w * factor for w in widths]
            tbl_pr = table._tbl.tblPr
            layout = OxmlElement("w:tblLayout")
            layout.set(qn("w:type"), "fixed")
            tbl_pr.append(layout)
            tbl_w = OxmlElement("w:tblW")
            tbl_w.set(qn("w:type"), "dxa")
            tbl_w.set(qn("w:w"), str(int(avail_cm / 2.54 * 1440)))
            tbl_pr.append(tbl_w)
            for ci, w in enumerate(widths):
                table.columns[ci].width = Cm(w)
            for ri, row in enumerate(rows):
                for ci in range(cols):
                    cell = table.cell(ri, ci)
                    cell.width = Cm(widths[ci])
                    cell.text = ""
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_after = Pt(1)
                    p.paragraph_format.line_spacing = 1.05
                    txt = row[ci] if ci < len(row) else ""
                    txt = re.sub(r"\*\*|`", "", txt)
                    run = p.add_run(txt)
                    set_run_font(run, size=TABLE_SIZE, bold=(ri == 0))
                    if ri == 0:
                        shade(cell, "E8EFEA")
            doc.add_paragraph().paragraph_format.space_after = Pt(2)


def cover_page(doc, title, subtitle):
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p, title, base_size=Pt(26))
    for r in p.runs:
        r.font.bold = True
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p2, subtitle, base_size=Pt(13))
    for r in p2.runs:
        r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
    doc.add_paragraph()
    p3 = doc.add_paragraph(); p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p3, "2026-10-22 · 第三届“金种子杯”大学生创业大赛 · 现代农业与大健康产业赛道", base_size=Pt(10))
    doc.add_page_break()


def main():
    args = sys.argv[1:]
    merge = False
    if args and args[0] == "--merge":
        merge = True
        out = args[1]
        inputs = args[2:]
    else:
        if len(args) < 2:
            print("usage: md2docx.py <in.md> <out.docx> | --merge <out.docx> <in1..>")
            return 2
        out, inputs = args[1], [args[0]]

    doc = init_document()
    if merge:
        cover_page(doc, "菌护禾 · 项目交付合集",
                    "技能说明 / 深度分析 / 论文初稿 / 试验方案 / 工具调研 / 交付说明")
        toc_lines = ["## 本合集包含", ""]
        for path in inputs:
            stem = os.path.splitext(os.path.basename(path))[0]
            toc_lines.append(f"- {stem}")
        toc_lines += ["", "---", ""]
        render_markdown(doc, "\n".join(toc_lines))
        for idx, path in enumerate(inputs):
            if idx > 0:
                doc.add_page_break()
            with open(path, encoding="utf-8") as f:
                render_markdown(doc, f.read())
    else:
        with open(inputs[0], encoding="utf-8") as f:
            render_markdown(doc, f.read())

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    doc.save(out)
    print(f"OK {out} paragraphs={len(doc.paragraphs)} tables={len(doc.tables)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
