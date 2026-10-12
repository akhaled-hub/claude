# Elevatus Word documents (python-docx): an editable .docx in the identity, with the same cover as the PDF reports.
# Inter is referenced by name: Word shows it when the font is installed, otherwise it falls back to the system sans.
# Usage: see .claude/skills/elevatus-documents/SKILL.md
import os, tempfile
import fitz
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
import lib

ASSETS = lib.ASSETS
LOGO, VIVID, INK, SLATE = RGBColor(0x05, 0x12, 0x74), RGBColor(0x1B, 0x15, 0xCF), RGBColor(0x11, 0x16, 0x2B), RGBColor(0x58, 0x61, 0x77)

def _font(style, size, color, bold=False, name='Inter'):
    f = style.font; f.name = name; f.size = Pt(size); f.bold = bold; f.color.rgb = color
    style.element.rPr.rFonts.set(qn('w:eastAsia'), name)

def _shade(cell, hex_):
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hex_)
    cell._tc.get_or_add_tcPr().append(sh)

def document(name, person='', date='', cover=None):
    """New A4 document with Elevatus styles, a running header (wordmark + name, person + date) and a page-number footer.
    cover = dict(title=, description=, category=, label=) adds the full-bleed cover as page 1."""
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    if cover:
        # page 1: the PDF cover rendered once and placed edge to edge
        pdf = fitz.open(); lib.cover(pdf, **cover)
        png = os.path.join(tempfile.mkdtemp(), 'cover.png'); pdf[0].get_pixmap(dpi=200).save(png)
        for side in ('left_margin', 'right_margin', 'top_margin', 'bottom_margin'): setattr(sec, side, Mm(0))
        sec.header_distance = sec.footer_distance = Mm(0)
        p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.add_run().add_picture(png, width=Mm(210), height=Mm(296.5))
        sec = doc.add_section(WD_SECTION.NEW_PAGE)
        sec.header.is_linked_to_previous = False; sec.footer.is_linked_to_previous = False
    sec.left_margin = sec.right_margin = Mm(17); sec.top_margin = Mm(34); sec.bottom_margin = Mm(22)
    sec.header_distance = Mm(11); sec.footer_distance = Mm(10)

    st = doc.styles
    _font(st['Normal'], 10, INK)
    st['Normal'].paragraph_format.space_after = Pt(6); st['Normal'].paragraph_format.line_spacing = 1.3
    for lvl, size in ((1, 18), (2, 13), (3, 11)):
        h = st[f'Heading {lvl}']; _font(h, size, LOGO, True)
        h.paragraph_format.space_before = Pt(14 if lvl == 1 else 10); h.paragraph_format.space_after = Pt(5)
    _font(st['List Bullet'], 10, INK)

    # header: wordmark + document name on the left, person + date on the right
    t = sec.header.add_table(1, 2, Mm(176)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    left, right = t.rows[0].cells
    lp = left.paragraphs[0]; lp.add_run().add_picture(os.path.join(ASSETS, 'wordmark-vivid.png'), width=Mm(34))
    r = left.add_paragraph().add_run(name); r.font.size = Pt(7.5); r.font.bold = True; r.font.name = 'Inter'
    rp = right.paragraphs[0]; rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = rp.add_run(person); r.font.size = Pt(10.5); r.font.bold = True; r.font.name = 'Inter'
    dp = right.add_paragraph(); dp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = dp.add_run(date); r.font.size = Pt(7.8); r.font.color.rgb = SLATE; r.font.name = 'Inter'
    for par in sec.header.paragraphs:
        if not par.text and not par.runs: par.paragraph_format.space_after = Pt(0)

    # footer: copyright + page number field
    fp = sec.footer.paragraphs[0]
    r = fp.add_run('Elevatus. All rights reserved.\t\tPage '); r.font.size = Pt(7.5); r.font.color.rgb = SLATE; r.font.name = 'Inter'
    run = fp.add_run(); run.font.size = Pt(7.5); run.font.color.rgb = SLATE
    for tag, text in (('begin', None), (None, 'PAGE'), ('end', None)):
        if tag:
            el = OxmlElement('w:fldChar'); el.set(qn('w:fldCharType'), tag)
        else:
            el = OxmlElement('w:instrText'); el.set(qn('xml:space'), 'preserve'); el.text = text
        run._r.append(el)
    return doc

def table(doc, header, rows, widths_mm=None):
    """Branded table: Logo Blue header row with white type, light rules, no vertical lines."""
    t = doc.add_table(rows=1, cols=len(header)); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, label in enumerate(header):
        c = t.rows[0].cells[i]; c.text = ''; _shade(c, '051274')
        r = c.paragraphs[0].add_run(label); r.font.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(255, 255, 255); r.font.name = 'Inter'
    for k, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ''
            r = cells[i].paragraphs[0].add_run(str(v)); r.font.size = Pt(9.5); r.font.name = 'Inter'
            if k % 2: _shade(cells[i], 'F4F7FF')
    if widths_mm:
        for row in t.rows:
            for i, w in enumerate(widths_mm): row.cells[i].width = Mm(w)
    doc.add_paragraph()
    return t
