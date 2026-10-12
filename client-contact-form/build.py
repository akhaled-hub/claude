# Elevatus Client Contact Details Form: interactive, fillable A4 PDF in the Elevatus identity.
# Builds output/Elevatus - Client Contact Details Form.pdf: the blue brand cover plus two form pages.
#   python3 build.py
# Needs PyMuPDF (pip install pymupdf). Page design is vector with live Inter text;
# form fields use Helvetica so every PDF reader can draw what the client types.
import os
import pymupdf as fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
FONTS = os.path.join(ASSETS, 'fonts')
OUTPUT = os.path.join(HERE, 'output')

YEAR = '2026'
FORM_NAME = 'Client Contact Details Form'

W, H = 595.28, 841.89                 # A4
MX = 48
CW = W - 2 * MX


def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


C = dict(vivid=rgb('1B15CF'), logo=rgb('051274'), electric=rgb('2962FF'), apricot=rgb('F0A15C'),
         ink=rgb('11162B'), slate=rgb('586177'), mist=rgb('C7D0E1'), line=rgb('E3E7F0'), paper=rgb('F4F7FF'),
         white=(1, 1, 1), s100=rgb('E4EBFF'), s200=rgb('C9D4FF'), s300=rgb('A9B4FF'),
         apricot_tint=rgb('FDEFE2'), apricot_ink=rgb('8A4A12'))

FONTFILES = {'L': 'Inter-Light', 'R': 'Inter-Regular', 'M': 'Inter-Medium', 'S': 'Inter-SemiBold'}
FONTOBJ = {k: fitz.Font(fontfile=os.path.join(FONTS, v + '.otf')) for k, v in FONTFILES.items()}


def tw(s, f, size): return FONTOBJ[f].text_length(s, fontsize=size)


def fonts(p):
    for k, v in FONTFILES.items():
        p.insert_font(fontname='I' + k, fontfile=os.path.join(FONTS, v + '.otf'))


# ---------------------------------------------------------------- wordmark (vector, recoloured)
_wm = fitz.open('pdf', fitz.open(os.path.join(ASSETS, 'elevatus-wordmark.svg')).convert_to_pdf())
WM_DRAW = [d for d in _wm[0].get_drawings() if d.get('fill') is not None]
WM_BOX = fitz.Rect(WM_DRAW[0]['rect'])
for _d in WM_DRAW[1:]: WM_BOX |= _d['rect']


def wordmark(p, x, y, width, color):
    s = width / WM_BOX.width
    M = fitz.Matrix(s, 0, 0, s, x - WM_BOX.x0 * s, y - WM_BOX.y0 * s)
    sh = p.new_shape()
    for d in WM_DRAW:
        for it in d['items']:
            k = it[0]
            if k == 'l': sh.draw_line(it[1] * M, it[2] * M)
            elif k == 'c': sh.draw_bezier(it[1] * M, it[2] * M, it[3] * M, it[4] * M)
            elif k == 're': sh.draw_quad(fitz.Quad(it[1]) * M)
            elif k == 'qu': sh.draw_quad(it[1] * M)
        sh.finish(fill=color, color=None, closePath=True)
    sh.commit()
    return WM_BOX.height * s


# ---------------------------------------------------------------- primitives
def text(p, x, y, s, f='R', size=10, color=C['ink'], align='left', track=0):
    """Single line; y is the baseline. track = letter-spacing in em."""
    if align != 'left':
        w = tw(s, f, size) + track * size * max(len(s) - 1, 0)
        x = x - w if align == 'right' else x - w / 2
    if not track:
        p.insert_text((x, y), s, fontname='I' + f, fontsize=size, color=color)
        return
    for ch in s:   # tracked caps: place glyph by glyph
        p.insert_text((x, y), ch, fontname='I' + f, fontsize=size, color=color)
        x += tw(ch, f, size) + track * size


def wrap(s, f, size, maxw):
    lines, cur = [], ''
    for word in s.split():
        t = (cur + ' ' + word).strip()
        if cur and tw(t, f, size) > maxw: lines.append(cur); cur = word
        else: cur = t
    if cur: lines.append(cur)
    return lines


def para(p, x, y, s, f='R', size=9.5, lead=14, color=C['ink'], maxw=CW):
    """y = baseline of the first line. Returns the height used."""
    lines = wrap(s, f, size, maxw)
    for i, ln in enumerate(lines): text(p, x, y + i * lead, ln, f, size, color)
    return len(lines) * lead


def rrect(p, r, radius=0, fill=None, color=None, width=0.8):
    r = fitz.Rect(r)
    rad = min(radius / min(r.width, r.height), 0.5) if radius else None
    p.draw_rect(r, fill=fill, color=color, width=width, radius=rad)


def line(p, a, b, color=C['line'], width=0.75, dashes=None):
    p.draw_line(fitz.Point(a), fitz.Point(b), color=color, width=width, dashes=dashes)


def circle(p, c, r, fill=None, color=None, width=1):
    p.draw_circle(fitz.Point(c), r, fill=fill, color=color, width=width)


# ---------------------------------------------------------------- small icons (stroked, 1em = s)
def icon(p, kind, cx, cy, s, color, width=1.1):
    sh = p.new_shape()
    P = lambda x, y: fitz.Point(cx + x * s, cy + y * s)
    if kind == 'open':        # document
        sh.draw_polyline([P(-.32, -.45), P(.12, -.45), P(.32, -.25), P(.32, .45), P(-.32, .45), P(-.32, -.45)])
        sh.draw_polyline([P(.12, -.45), P(.12, -.25), P(.32, -.25)])
    elif kind == 'fill':      # pencil
        sh.draw_polyline([P(-.38, .38), P(-.38, .16), P(.2, -.42), P(.42, -.2), P(-.16, .38), P(-.38, .38)])
        sh.draw_line(P(.06, -.28), P(.28, -.06))
    elif kind == 'review':    # check in circle
        sh.draw_circle(P(0, 0), .42 * s)
        sh.draw_polyline([P(-.2, 0), P(-.05, .15), P(.22, -.14)])
    elif kind == 'save':      # download tray
        sh.draw_line(P(0, -.42), P(0, .14))
        sh.draw_polyline([P(-.2, -.06), P(0, .14), P(.2, -.06)])
        sh.draw_polyline([P(-.4, .12), P(-.4, .4), P(.4, .4), P(.4, .12)])
    elif kind == 'send':      # paper plane
        sh.draw_polyline([P(-.42, -.02), P(.42, -.38), P(.12, .42), P(-.02, .08), P(-.42, -.02)])
        sh.draw_line(P(-.02, .08), P(.42, -.38))
    elif kind == 'print':
        sh.draw_polyline([P(-.24, -.18), P(-.24, -.42), P(.24, -.42), P(.24, -.18)])
        sh.draw_polyline([P(-.24, .22), P(-.42, .22), P(-.42, -.18), P(.42, -.18), P(.42, .22), P(.24, .22)])
        sh.draw_polyline([P(-.24, .06), P(.24, .06), P(.24, .42), P(-.24, .42), P(-.24, .06)])
    elif kind == 'mail':
        sh.draw_polyline([P(-.42, -.3), P(.42, -.3), P(.42, .3), P(-.42, .3), P(-.42, -.3)])
        sh.draw_polyline([P(-.42, -.3), P(0, .04), P(.42, -.3)])
    elif kind == 'info':
        sh.draw_circle(P(0, 0), .42 * s)
        sh.draw_line(P(0, -.04), P(0, .22))
        sh.finish(color=color, width=width, lineCap=1, lineJoin=1)
        sh.draw_circle(P(0, -.2), .045 * s)
        sh.finish(color=color, fill=color, width=0)
        sh.commit()
        return
    elif kind == 'clear':     # circular arrow
        import math
        pts = [P(.36 * math.cos(math.radians(a)), .36 * math.sin(math.radians(a))) for a in range(-200, 100, 10)]
        sh.draw_polyline(pts)
        sh.draw_polyline([P(-.42, -.32), P(-.36, -.12), P(-.16, -.18)])
    sh.finish(color=color, width=width, lineCap=1, lineJoin=1)
    sh.commit()


# ---------------------------------------------------------------- form widgets
# Plain text fields with no scripts: nothing the client types is ever rejected, reformatted or cleared,
# and every reader (Acrobat, Chrome, Edge, Firefox, Preview, phones) shows the text the same way.
# Format guidance lives in the hint under each field.
TX_FONT, TX_SIZE = 'Helv', 10.5

# contact sections: (field prefix, section title, label prefix, subtitle)
CONTACTS = [
    ('bdm', 'Business decision maker', 'Business Decision Maker', 'The person who signs off decisions for your company.'),
    ('proc', 'Procurement contact', 'Procurement Contact', 'The representative for purchasing and procurement coordination.'),
    ('fin', 'Finance contact', 'Finance Contact', 'The representative for invoices, billing and payment coordination.'),
    ('esc', 'Escalation contact', 'Escalation Contact', 'The point of contact for urgent matters or issues requiring escalation.'),
]


def text_field(p, name, tooltip, r, maxlen=0):
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_name = name
    w.field_label = tooltip
    w.rect = fitz.Rect(r)
    w.text_font, w.text_fontsize, w.text_color = TX_FONT, TX_SIZE, C['ink']
    w.border_color, w.fill_color, w.border_width = None, None, 0
    w.field_flags = fitz.PDF_FIELD_IS_REQUIRED
    if maxlen: w.text_maxlen = maxlen
    p.add_widget(w)


# ---------------------------------------------------------------- layout pieces
R_FIELD = 3          # corner radius: fields, buttons, frames (kept small for a formal look)
FIELD_H = 28


def label(p, x, y, s, required=True):
    text(p, x, y, s, 'M', 8.4, C['ink'])
    if required: text(p, x + tw(s, 'M', 8.4) + 2.5, y, '*', 'S', 8.4, C['vivid'])


def field_box(p, x, y, w, lab, hint, required=True, fill=C['white']):
    """Label above, input box, hint below. Returns (input rect, total height)."""
    label(p, x, y + 9, lab, required)
    by = y + 15
    rrect(p, (x, by, x + w, by + FIELD_H), R_FIELD, fill=fill, color=C['mist'], width=0.75)
    if hint: text(p, x, by + FIELD_H + 11, hint, 'R', 7.1, C['slate'])
    return fitz.Rect(x + 8, by + 1.5, x + w - 8, by + FIELD_H - 1.5), 15 + FIELD_H + (15 if hint else 4)


def section(p, y, num, title, sub):
    """Numbered heading, subtitle under it, hairline. Returns the y where content starts."""
    text(p, MX, y + 12, num, 'S', 10, C['vivid'])
    text(p, MX + 24, y + 12, title, 'S', 12, C['logo'])
    text(p, MX + 24, y + 26, sub, 'R', 8, C['slate'])
    line(p, (MX, y + 36), (W - MX, y + 36), C['line'], 0.75)
    return y + 46


def header(p):
    wordmark(p, MX, 34, 98, C['vivid'])
    text(p, MX, 62, FORM_NAME, 'S', 7.6, C['ink'])
    text(p, W - MX, 45, 'Client Onboarding', 'S', 10.5, C['ink'], 'right')
    text(p, W - MX, 59, 'Fillable form · ' + YEAR, 'R', 7.8, C['slate'], 'right')
    line(p, (MX, 74), (W - MX, 74))


def footer(p, page_no, pages):
    line(p, (MX, H - 46), (W - MX, H - 46))
    text(p, MX, H - 30, f'{YEAR} Elevatus. All rights reserved.', 'R', 7.5, C['slate'])
    text(p, W / 2, H - 30, 'Confidential: shared with Elevatus for client coordination only', 'R', 7.5, C['slate'], 'center')
    text(p, W - MX, H - 30, f'Page {page_no} of {pages}', 'R', 7.5, C['slate'], 'right')


STEPS = [('open', 'Open', 'In any PDF reader'), ('fill', 'Fill', 'Sections 01 to 05'), ('review', 'Review', 'Check your answers'),
         ('save', 'Save', 'Keep a copy'), ('send', 'Send', 'Back to Elevatus')]


def stepper(p, y):
    """Five steps in a thin frame, divided by hairlines."""
    h = 44
    rrect(p, (MX, y, W - MX, y + h), R_FIELD, fill=C['paper'])
    n = len(STEPS); cw = CW / n
    for i, (k, title, sub) in enumerate(STEPS):
        x = MX + cw * i
        if i: line(p, (x, y + 10), (x, y + h - 10), C['s200'], 0.6)
        icon(p, k, x + 18, y + h / 2, 12, C['vivid'], 1)
        text(p, x + 31, y + 19.5, f'{i + 1}  {title}', 'S', 8.6, C['logo'])
        text(p, x + 31, y + 31, sub, 'R', 6.9, C['slate'])
    return h


GAP = 16                    # gutter between fields on one row
HALF = (CW - GAP) / 2
SECTION_GAP = 30


def contact_section(p, y, num, key, title, lab, sub):
    """Name on its own row; email and contact number (country code + number) side by side. Returns the end y."""
    cy = section(p, y, num, title, sub)
    r, rh = field_box(p, MX, cy, CW, f'{lab} Name', 'First and last name')
    text_field(p, f'{key}_name', f'{lab} Name', r)
    cy += rh + 4
    r, rh = field_box(p, MX, cy, HALF, f'{lab} Email', 'Work email, for example name@company.com')
    text_field(p, f'{key}_email', f'{lab} Email', r)
    xx, ccw = MX + HALF + GAP, 60
    num_lab = f'{lab} Number' if lab.endswith('Contact') else f'{lab} Contact Number'
    r, _ = field_box(p, xx, cy, ccw, num_lab, 'Country code (e.g. 966), then the number', fill=C['paper'])
    # the + is printed on the page, so the code reads the same in every reader; the client types digits only
    text(p, r.x0, r.y0 + r.height / 2 + 3.8, '+', 'R', 10.5, C['ink'])
    r.x0 += 8
    text_field(p, f'{key}_country_code', f'{num_lab}: country code, digits only, for example 966', r, 4)
    by = cy + 15
    rrect(p, (xx + ccw + 6, by, xx + HALF, by + FIELD_H), R_FIELD, fill=C['white'], color=C['mist'], width=0.75)
    text_field(p, f'{key}_phone', f'{num_lab} without the country code',
               (xx + ccw + 14, by + 1.5, xx + HALF - 8, by + FIELD_H - 1.5), )
    return cy + rh


def form_pages(doc, first_page_no, pages):
    """Page 1: intro, steps, 01 company, 02 decision maker, 03 procurement.
    Page 2: 04 finance, 05 escalation. Returns [(title, page index, y)] for bookmarks."""
    toc = []

    def page():
        p = doc.new_page(width=W, height=H)
        fonts(p)
        header(p)
        return p

    p = page()
    y = 104
    text(p, MX, y, 'CLIENT ONBOARDING', 'S', 7.4, C['vivid'], track=0.14)
    text(p, MX - 1, y + 30, 'Client Contact Details', 'L', 26, C['logo'])
    y += 52 + para(p, MX, y + 52, "Please provide your company's key contacts so the Elevatus team can coordinate effectively "
                   'with the right people. All fields are required. Include the country code in all contact numbers.',
                   'R', 9.4, 14.2, C['slate'], maxw=CW - 10) + 6
    y += stepper(p, y) + 28

    toc.append(('01  Company details', p.number, y))
    cy = section(p, y, '01', 'Company details', 'Who is registering with Elevatus.')
    dw = 150
    r, rh = field_box(p, MX, cy, dw, 'Date of Registration', 'DD/MM/YYYY')
    text_field(p, 'registration_date', 'Date of Registration (DD/MM/YYYY)', r)
    r, _ = field_box(p, MX + dw + GAP, cy, CW - dw - GAP, 'Company Name', 'Registered company or trading name')
    text_field(p, 'company_name', 'Company Name', r)
    y = cy + rh + SECTION_GAP

    for i, (key, title, lab, sub) in enumerate(CONTACTS):
        num = f'{i + 2:02d}'
        if i == 2:                       # finance and escalation start page 2
            footer(p, first_page_no, pages)
            p = page(); y = 100
        toc.append((f'{num}  {title[0].upper() + title[1:]}', p.number, y))
        y = contact_section(p, y, num, key, title[0].upper() + title[1:], lab, sub) + SECTION_GAP

    footer(p, first_page_no + 1, pages)
    return toc


def cover_art(dpi=220):
    """Brand background with the key-contacts illustration (art/cover-illustration.html, rendered to
    assets/cover-contacts.png) composited on top, flattened to one JPEG to keep the file light."""
    from PIL import Image
    import io
    k = dpi / 72
    bg = Image.open(os.path.join(ASSETS, 'cover-bg.png')).convert('RGB').resize((round(W * k), round(H * k)), Image.LANCZOS)
    art = Image.open(os.path.join(ASSETS, 'cover-contacts.png')).convert('RGBA')
    iw = W * 1.04; ih = iw * art.height / art.width
    x0, y0 = W - iw + 6, H - 78 - ih
    art = art.resize((round(iw * k), round(ih * k)), Image.LANCZOS)
    bg.paste(art, (round(x0 * k), round(y0 * k)), art)
    buf = io.BytesIO(); bg.save(buf, 'JPEG', quality=90, optimize=True, progressive=True)
    return buf.getvalue()


def cover(doc):
    """The Elevatus document cover: full-bleed blue field, white wordmark, title, product image."""
    p = doc.new_page(width=W, height=H)
    fonts(p)
    p.insert_image(p.rect, stream=cover_art(), keep_proportion=False)
    x, white = 40, C['white']
    y = 58 + wordmark(p, x, 58, 178, white) + 46
    for i, ln in enumerate(['Client Contact', 'Details Form']):
        text(p, x - 2, y + 38 + i * 50, ln, 'L', 44, white)
    y += 50 * 2 + 20
    for i, ln in enumerate(wrap('Your key contacts for decisions, procurement, finance and escalation, so the '
                                'Elevatus team always reaches the right person.', 'R', 13.5, 440)):
        text(p, x, y + 13 + i * 19.5, ln, 'R', 13.5, white)
    y += 2 * 19.5 + 22
    # the five steps, as a quiet line of pills
    px = x
    for i, (k, title, _) in enumerate(STEPS):
        lab = title
        pw = tw(lab, 'M', 9) + 34
        rrect(p, (px, y, px + pw, y + 22), 3, color=white, width=0.7)
        icon(p, k, px + 12, y + 11, 10, white, 1)
        text(p, px + 23, y + 14.4, lab, 'M', 9, white)
        px += pw + (14 if i < len(STEPS) - 1 else 0)
        if i < len(STEPS) - 1:
            line(p, (px - 11, y + 11), (px - 3, y + 11), white, 0.7)
    for i, ln in enumerate(['CLIENT', 'ONBOARDING'][::-1]):
        text(p, x, H - 40 - i * 14.5, ln, 'M', 9.5, white, track=0.12)
    text(p, W - x, H - 40, 'Fillable PDF Form', 'M', 11.5, white, 'right')
    return p


def build():
    """Cover + two form pages."""
    doc = fitz.open()
    cover(doc)
    toc = form_pages(doc, 1, 2)
    # clicking anywhere on the cover opens the form
    doc[0].insert_link({'kind': fitz.LINK_GOTO, 'from': fitz.Rect(0, 0, W, H), 'page': 1, 'to': fitz.Point(0, 0)})
    outline = [[1, 'Cover', 0, 0], [1, 'Client Contact Details', 1, 0]] + [[2, t, pg, yy] for t, pg, yy in toc]
    doc.set_toc([[l, t, pg + 1, {'kind': fitz.LINK_GOTO, 'page': pg, 'to': fitz.Point(0, max(yy - 10, 0))}]
                 for l, t, pg, yy in outline])
    doc.set_metadata({'title': 'Elevatus ' + FORM_NAME, 'author': 'Elevatus', 'subject': 'Client onboarding: key contacts',
                      'keywords': 'Elevatus, client onboarding, contact details, form', 'creator': 'Elevatus', 'producer': 'Elevatus'})
    cat = doc.pdf_catalog()
    doc.xref_set_key(cat, 'ViewerPreferences', '<< /DisplayDocTitle true >>')
    doc.xref_set_key(cat, 'PageMode', '/UseNone')
    doc.xref_set_key(cat, 'Lang', '(en)')
    # default resources so any reader can redraw typed text in the fields
    af = doc.xref_get_key(cat, 'AcroForm')
    af_xref = int(af[1].split()[0]) if af[0] == 'xref' else cat
    key = '' if af[0] == 'xref' else 'AcroForm/'
    doc.xref_set_key(af_xref, key + 'DR', '<< /Font << /Helv << /Type /Font /Subtype /Type1 /BaseFont /Helvetica '
                     '/Encoding /WinAnsiEncoding >> /ZaDb << /Type /Font /Subtype /Type1 /BaseFont /ZapfDingbats >> >> >>')
    doc.xref_set_key(af_xref, key + 'DA', '(/Helv 0 Tf 0 g)')
    doc.xref_set_key(af_xref, key + 'NeedAppearances', 'true')   # readers redraw typed text themselves
    doc.subset_fonts()
    os.makedirs(OUTPUT, exist_ok=True)
    name = f'Elevatus - {FORM_NAME}.pdf'
    path = os.path.join(OUTPUT, name)
    doc.save(path, garbage=4, deflate=True)
    return path


if __name__ == '__main__':
    print(build())
