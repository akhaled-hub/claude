# Elevatus Client Contact Details Form: interactive, fillable A4 PDF in the Elevatus identity.
# Builds two versions into output/: one with the blue brand cover, one without.
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
TX_FONT, TX_SIZE = 'Helv', 10.5


def js_alert(msg): return 'app.alert({cMsg:"%s", cTitle:"Elevatus", nIcon:1});' % msg


VALIDATE = {
    'email': 'if (event.value !== "") { var v = event.value.replace(/^\\s+|\\s+$/g, ""); '
             'if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(v)) { '
             + js_alert('Please enter a valid email address, for example name@company.com.') +
             ' event.rc = false; } else { event.value = v.toLowerCase(); } }',
    'cc': 'if (event.value !== "") { var d = event.value.replace(/[^0-9]/g, ""); '
          'if (d.length < 1 || d.length > 4) { ' + js_alert('Please enter a country code of 1 to 4 digits, for example 966 or 971.') +
          ' event.rc = false; } }',
    'phone': 'if (event.value !== "") { var d = event.value.replace(/[^0-9]/g, ""); '
             'if (d.length < 6 || d.length > 14) { ' + js_alert('Please enter a contact number of 6 to 14 digits, without the country code.') +
             ' event.rc = false; } }',
    'text': 'event.value = event.value.replace(/^\\s+|\\s+$/g, "").replace(/\\s{2,}/g, " ");',
}
KEYSTROKE = {
    'cc': 'if (!event.willCommit) event.rc = /^[0-9]*$/.test(event.change);',
    'phone': 'if (!event.willCommit) event.rc = /^[0-9 \\-]*$/.test(event.change);',
    'date': 'AFDate_KeystrokeEx("dd/mm/yyyy");',
}
FORMAT = {'date': 'AFDate_FormatEx("dd/mm/yyyy");'}

# required fields in reading order: (field name, label shown to the client)
REQUIRED = [('registration_date', 'Date of Registration'), ('company_name', 'Company Name'),
            ('bdm_name', 'Business Decision Maker Name'), ('bdm_email', 'Business Decision Maker Email'),
            ('bdm_country_code', 'Country code'), ('bdm_phone', 'Contact number')]

WILL_SAVE_JS = (
    'var req = [' + ', '.join('["%s", "%s"]' % r for r in REQUIRED) + '];'
    'var miss = [];'
    'for (var i = 0; i < req.length; i++) { var f = this.getField(req[i][0]);'
    '  if (f && f.valueAsString.replace(/\\s/g, "") === "") miss.push(req[i][1]); }'
    'var cb = this.getField("confirm_details"); if (cb && cb.value === "Off") miss.push("Confirmation tick in step 03");'
    'if (miss.length) app.alert({cMsg: "Your copy will be saved. Before sending it to Elevatus, please complete:\\n\\n- " + '
    'miss.join("\\n- "), cTitle: "Elevatus", nIcon: 3});'
)

def text_field(p, name, tooltip, r, kind='text', maxlen=0, required=True):
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_name = name
    w.field_label = tooltip
    w.rect = fitz.Rect(r)
    w.text_font, w.text_fontsize, w.text_color = TX_FONT, TX_SIZE, C['ink']
    w.border_color, w.fill_color, w.border_width = None, None, 0
    w.field_flags = (fitz.PDF_FIELD_IS_REQUIRED if required else 0) | fitz.PDF_TX_FIELD_IS_DO_NOT_SCROLL
    if maxlen: w.text_maxlen = maxlen
    if kind in VALIDATE: w.script_change = VALIDATE[kind]
    else: w.script_change = VALIDATE['text']
    if kind in KEYSTROKE: w.script_stroke = KEYSTROKE[kind]
    if kind in FORMAT: w.script_format = FORMAT[kind]
    p.add_widget(w)


def checkbox(p, name, tooltip, r):
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = name
    w.field_label = tooltip
    w.rect = fitz.Rect(r)
    w.border_color, w.fill_color, w.border_width = C['mist'], C['white'], 1
    w.text_color = C['vivid']
    w.field_value = False
    return p.add_widget(w)


def style_checkbox(doc, w):
    """Brand appearance for the tick box: white with a mist border when empty, vivid blue with a white tick when on."""
    s = w.rect.width

    def box(a, r, b):  # rounded square from (a, a) to (b, b), corner radius r, PDF coordinates
        q = r * 0.4477  # distance from the corner to each bezier control point
        return (f'{a + r} {a} m {b - r} {a} l {b - q} {a} {b} {a + q} {b} {a + r} c '
                f'{b} {b - r} l {b} {b - q} {b - q} {b} {b - r} {b} c '
                f'{a + r} {b} l {a + q} {b} {a} {b - q} {a} {b - r} c '
                f'{a} {a + r} l {a} {a + q} {a + q} {a} {a + r} {a} c h')
    v, m = C['vivid'], C['mist']
    off = f'1 1 1 rg {m[0]:.3f} {m[1]:.3f} {m[2]:.3f} RG 1 w {box(.5, 2.5, s - .5)} B'
    on = (f'{v[0]:.3f} {v[1]:.3f} {v[2]:.3f} rg {box(0, 2.5, s)} f '
          f'1 1 1 RG 1.6 w 1 J 1 j {s * .27:.2f} {s * .52:.2f} m {s * .44:.2f} {s * .34:.2f} l {s * .74:.2f} {s * .68:.2f} l S')
    for state, stream in (('Off', off), ('Yes', on)):
        x = int(doc.xref_get_key(w.xref, f'AP/N/{state}')[1].split()[0])
        doc.update_stream(x, stream.encode())
    doc.xref_set_key(w.xref, 'MK/CA', '(4)')
    doc.xref_set_key(w.xref, 'DA', f'({v[0]:.3f} {v[1]:.3f} {v[2]:.3f} rg /ZaDb 0 Tf)')



# Save button script, one route per viewer family:
# - Acrobat/Reader, Foxit, Firefox and other pdf.js viewers run app.execMenuItem("SaveAs") and open Save As.
# - Chrome's viewer (PDFium, app.viewerType "pdfium") runs form scripts but refuses execMenuItem; it does run
#   this.print(), and Chrome's print dialog offers "Save as PDF", which keeps everything the client typed.
SAVE_JS = (
    '(function () {'
    '  var saved = false;'
    '  if (app.viewerType != "pdfium") { try { app.execMenuItem("SaveAs"); saved = true; } catch (e) {} }'
    '  if (!saved) {'
    '    app.alert({cMsg: "In the next window, choose Save as PDF as the destination, then click Save.", '
    'cTitle: "Save your completed form", nIcon: 3});'
    '    this.print({bUI: true, bSilent: false, bShrinkToFit: true});'
    '  }'
    '}).call(this);'
)


def save_button(doc, p, r):
    """Push button that opens Save As where the reader allows it, and Print > Save as PDF in Chrome."""
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
    w.field_flags = fitz.PDF_BTN_FIELD_IS_PUSHBUTTON | fitz.PDF_FIELD_IS_NO_EXPORT
    w.field_name = 'btn_save'
    w.field_label = 'Save the completed form'
    w.rect = fitz.Rect(r)
    w.button_caption = ''
    w.border_color, w.fill_color, w.border_width = None, None, 0
    w.script = SAVE_JS
    w = p.add_widget(w)
    doc.xref_set_key(w.xref, 'H', '/P')


def will_save(doc):
    """On save (Acrobat/Reader), remind the client of any required field still empty. The save still goes ahead."""
    x = doc.get_new_xref()
    doc.update_object(x, '<< >>')
    doc.update_stream(x, WILL_SAVE_JS.encode('utf-8'))
    doc.xref_set_key(doc.pdf_catalog(), 'AA', f'<< /WS << /S /JavaScript /JS {x} 0 R >> >>')


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
    """Numbered heading with a hairline under it. Returns the y where content starts."""
    text(p, MX, y + 12, num, 'S', 10, C['vivid'])
    text(p, MX + 24, y + 12, title, 'S', 12, C['logo'])
    text(p, W - MX, y + 12, sub, 'R', 7.8, C['slate'], 'right')
    line(p, (MX, y + 22), (W - MX, y + 22), C['line'], 0.75)
    return y + 34


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


STEPS = [('open', 'Open', 'In any PDF reader'), ('fill', 'Fill', 'Sections 01 and 02'), ('review', 'Review', 'Check and confirm'),
         ('save', 'Save', 'Keep the filled PDF'), ('send', 'Send', 'Back to Elevatus')]


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


def form_page(doc, page_no, pages):
    p = doc.new_page(width=W, height=H)
    fonts(p)
    header(p)
    toc = []

    # title + intro
    y = 104
    text(p, MX, y, 'CLIENT ONBOARDING', 'S', 7.4, C['vivid'], track=0.14)
    text(p, MX - 1, y + 30, 'Client Contact Details', 'L', 26, C['logo'])
    y += 52 + para(p, MX, y + 52, "Please provide your company's key contacts so the Elevatus team can coordinate effectively "
                   'with the right people. Include the country code in all contact numbers.',
                   'R', 9.4, 14.2, C['slate'], maxw=CW - 10) + 6
    y += stepper(p, y) + 40

    gap = 16
    half = (CW - gap) / 2

    # 01 company
    toc.append(('01  Company details', y))
    cy = section(p, y, '01', 'Company details', 'Who is registering with Elevatus')
    dw = 150
    r, rh = field_box(p, MX, cy, dw, 'Date of Registration', 'DD/MM/YYYY')
    text_field(p, 'registration_date', 'Date of Registration (DD/MM/YYYY)', r, 'date', 10)
    r, _ = field_box(p, MX + dw + gap, cy, CW - dw - gap, 'Company Name', 'Registered company or trading name')
    text_field(p, 'company_name', 'Company Name', r, 'text', 120)
    y = cy + rh + 40

    # 02 business decision maker
    toc.append(('02  Business decision maker', y))
    cy = section(p, y, '02', 'Business decision maker', 'The person who signs off decisions for your company')
    r, rh = field_box(p, MX, cy, CW, 'Business Decision Maker Name', 'First and last name')
    text_field(p, 'bdm_name', 'Business Decision Maker Name', r, 'text', 100)
    cy += rh + 6
    r, rh = field_box(p, MX, cy, half, 'Business Decision Maker Email', 'Work email, for example name@company.com')
    text_field(p, 'bdm_email', 'Business Decision Maker Email', r, 'email', 120)
    # contact number = country code + number
    xx, ccw = MX + half + gap, 60
    r, _ = field_box(p, xx, cy, ccw, 'Business Decision Maker Contact Number', 'Country code (e.g. +966), then the number', fill=C['paper'])
    # the + is printed on the page, so the code reads the same in every reader; the client types digits only
    text(p, r.x0, r.y0 + r.height / 2 + 3.8, '+', 'R', 10.5, C['ink'])
    r.x0 += 8
    text_field(p, 'bdm_country_code', 'Contact number: country code, digits only, for example 966', r, 'cc', 4)
    by = cy + 15
    rrect(p, (xx + ccw + 6, by, xx + half, by + FIELD_H), R_FIELD, fill=C['white'], color=C['mist'], width=0.75)
    text_field(p, 'bdm_phone', 'Contact number without the country code',
               (xx + ccw + 14, by + 1.5, xx + half - 8, by + FIELD_H - 1.5), 'phone', 18)
    y = cy + rh + 40

    # 03 review & save
    toc.append(('03  Review & save', y))
    cy = section(p, y, '03', 'Review & save', 'Check your answers, then save the completed PDF')
    cb = checkbox(p, 'confirm_details', 'I confirm the details in this form are accurate', (MX, cy + 1, MX + 13, cy + 14))
    style_checkbox(doc, cb)
    para(p, MX + 22, cy + 10.5, 'I confirm the details above are accurate and that Elevatus may use them to contact these people '
         'about our account.', 'R', 8.8, 12.6, C['ink'], maxw=CW - 22)
    cy += 44

    # save button
    bw, bh = 132, 30
    br = fitz.Rect(MX, cy, MX + bw, cy + bh)
    rrect(p, br, R_FIELD, fill=C['vivid'])
    lab = 'Save completed form'
    lw = tw(lab, 'S', 8.6) + 17
    x0 = br.x0 + (bw - lw) / 2
    icon(p, 'save', x0 + 5.5, br.y0 + bh / 2, 11, C['white'])
    text(p, x0 + 17, br.y0 + bh / 2 + 3.1, lab, 'S', 8.6, C['white'])
    save_button(doc, p, br)

    # quiet note beside the button: how to save anywhere, then send
    nx = MX + bw + 18
    icon(p, 'info', nx + 4, cy + 6.5, 9, C['slate'], 0.9)
    para(p, nx + 14, cy + 9.5, 'If nothing opens, use File › Save (Windows, Mac), Download (browser) or '
         'Share › Save to Files (phone). Then send the saved PDF to the Elevatus team.',
         'R', 7.6, 11, C['slate'], maxw=W - MX - nx - 14)

    footer(p, page_no, pages)
    return p, toc



def cover_art(dpi=220):
    """Brand background with the product mockup composited on top, flattened to one JPEG to keep the file light.
    The device bleeds off the left edge and stops short of the right margin, as on the master cover."""
    from PIL import Image
    import io
    k = dpi / 72
    bg = Image.open(os.path.join(ASSETS, 'cover-bg.png')).convert('RGB').resize((round(W * k), round(H * k)), Image.LANCZOS)
    mock = Image.open(os.path.join(ASSETS, 'cover-mockup.png')).convert('RGBA')
    iw = W * 1.255; ih = iw * mock.height / mock.width
    y0 = max(H * 0.392, H - 96 - ih)
    mock = mock.resize((round(iw * k), round(ih * k)), Image.LANCZOS)
    bg.paste(mock, (round((W - iw) * k), round(y0 * k)), mock)
    buf = io.BytesIO(); bg.save(buf, 'JPEG', quality=88, optimize=True, progressive=True)
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
    for i, ln in enumerate(wrap("Share your company's key contacts so the Elevatus team can coordinate "
                                'with the right people from day one.', 'R', 13.5, 440)):
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


def build(with_cover):
    doc = fitz.open()
    if with_cover: cover(doc)
    _, toc = form_page(doc, 1, 1)
    if with_cover:   # clicking anywhere on the cover opens the form
        doc[0].insert_link({'kind': fitz.LINK_GOTO, 'from': fitz.Rect(0, 0, W, H), 'page': 1, 'to': fitz.Point(0, 0)})
    fp = 2 if with_cover else 1
    outline = ([[1, 'Cover', 1, 0]] if with_cover else []) + [[1, 'Client Contact Details', fp, 0]]
    outline += [[2, t, fp, yy] for t, yy in toc]
    doc.set_toc([[l, t, pg, {'kind': fitz.LINK_GOTO, 'page': pg - 1, 'to': fitz.Point(0, yy - 10)}] for l, t, pg, yy in outline])
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
    will_save(doc)
    doc.subset_fonts()
    os.makedirs(OUTPUT, exist_ok=True)
    name = f'Elevatus - {FORM_NAME}' + (' (with cover)' if with_cover else '') + '.pdf'
    path = os.path.join(OUTPUT, name)
    doc.save(path, garbage=4, deflate=True)
    return path


if __name__ == '__main__':
    for wc in (True, False):
        print(build(wc))
