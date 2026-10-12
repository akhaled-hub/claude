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

SEND_TO = 'info@elevatus.io'          # where the completed form is emailed
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
          'if (d.length < 1 || d.length > 4) { ' + js_alert('Please enter a country code of 1 to 4 digits, for example +966 or +971.') +
          ' event.rc = false; } else { event.value = "+" + d; } }',
    'phone': 'if (event.value !== "") { var d = event.value.replace(/[^0-9]/g, ""); '
             'if (d.length < 6 || d.length > 14) { ' + js_alert('Please enter a contact number of 6 to 14 digits, without the country code.') +
             ' event.rc = false; } }',
    'text': 'event.value = event.value.replace(/^\\s+|\\s+$/g, "").replace(/\\s{2,}/g, " ");',
}
KEYSTROKE = {
    'cc': 'if (!event.willCommit) event.rc = /^[+0-9]*$/.test(event.change);',
    'phone': 'if (!event.willCommit) event.rc = /^[0-9 \\-]*$/.test(event.change);',
    'date': 'AFDate_KeystrokeEx("dd/mm/yyyy");',
}
FORMAT = {'date': 'AFDate_FormatEx("dd/mm/yyyy");'}

# required fields in reading order: (field name, label shown to the client)
REQUIRED = [('registration_date', 'Date of Registration'), ('company_name', 'Company Name'),
            ('bdm_name', 'Business Decision Maker Name'), ('bdm_email', 'Business Decision Maker Email'),
            ('bdm_country_code', 'Country code'), ('bdm_phone', 'Contact number')]

CHECK_JS = (
    'var req = [' + ', '.join('["%s", "%s"]' % r for r in REQUIRED) + '];'
    'var miss = [], first = null;'
    'for (var i = 0; i < req.length; i++) { var f = this.getField(req[i][0]);'
    '  if (f.valueAsString.replace(/\\s/g, "") === "") { miss.push(req[i][1]); if (!first) first = f; } }'
    'if (miss.length) { app.alert({cMsg: "Please complete these required fields:\\n\\n\\u2022 " + miss.join("\\n\\u2022 "), cTitle: "Elevatus", nIcon: 1});'
    '  first.setFocus(); ok = false; }'
    'else if (this.getField("confirm_details").value === "Off") {'
    '  app.alert({cMsg: "Please tick the confirmation box in step 03 to confirm the details are correct.", cTitle: "Elevatus", nIcon: 1});'
    '  this.getField("confirm_details").setFocus(); ok = false; }'
)


def button_js(action):
    body = 'var ok = true;' + CHECK_JS
    if action == 'check':
        return ('(function(){' + body + 'if (ok) app.alert({cMsg: "Everything is complete. Next, save the PDF and send it to the Elevatus team.", '
                'cTitle: "Elevatus", nIcon: 3}); }).call(this);')
    if action == 'send':
        return ('(function(){' + body + 'if (!ok) return;'
                'var co = this.getField("company_name").valueAsString;'
                'try { this.mailDoc({bUI: true, cTo: "%s", cSubject: "Client Contact Details: " + co, '
                'cMsg: "Hello Elevatus team,\\n\\nPlease find attached our completed Client Contact Details Form.\\n\\nKind regards,\\n" + '
                'this.getField("bdm_name").valueAsString + "\\n" + co}); }'
                'catch (e) { app.alert({cMsg: "Your PDF reader could not open an email. Please save this file and email it to %s.", cTitle: "Elevatus", nIcon: 3}); }'
                '}).call(this);') % (SEND_TO, SEND_TO)
    if action == 'save':
        return 'app.execMenuItem("SaveAs");'
    if action == 'print':
        return 'this.print({bUI: true, bSilent: false, bShrinkToFit: true});'
    if action == 'clear':
        return ('if (app.alert({cMsg: "Clear every field in this form?", cTitle: "Elevatus", nIcon: 2, nType: 2}) == 4) '
                'this.resetForm();')


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


def push_button(p, name, tooltip, r, action):
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
    w.field_flags = fitz.PDF_BTN_FIELD_IS_PUSHBUTTON | fitz.PDF_FIELD_IS_NO_EXPORT
    w.field_name = name
    w.field_label = tooltip
    w.rect = fitz.Rect(r)
    w.button_caption = ''
    w.border_color, w.fill_color, w.border_width = None, None, 0
    w.script = button_js(action)
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
    off = f'1 1 1 rg {m[0]:.3f} {m[1]:.3f} {m[2]:.3f} RG 1 w {box(.5, 3.5, s - .5)} B'
    on = (f'{v[0]:.3f} {v[1]:.3f} {v[2]:.3f} rg {box(0, 3.5, s)} f '
          f'1 1 1 RG 1.6 w 1 J 1 j {s * .27:.2f} {s * .52:.2f} m {s * .44:.2f} {s * .34:.2f} l {s * .74:.2f} {s * .68:.2f} l S')
    for state, stream in (('Off', off), ('Yes', on)):
        x = int(doc.xref_get_key(w.xref, f'AP/N/{state}')[1].split()[0])
        doc.update_stream(x, stream.encode())
    doc.xref_set_key(w.xref, 'MK/CA', '(4)')
    doc.xref_set_key(w.xref, 'DA', f'({v[0]:.3f} {v[1]:.3f} {v[2]:.3f} rg /ZaDb 0 Tf)')


# ---------------------------------------------------------------- layout pieces
def field_box(p, x, y, w, label, hint, required=True, h=31):
    """Label above, rounded input box, hint below. Returns (input rect, total height)."""
    text(p, x, y + 9, label, 'M', 8.6, C['ink'])
    if required: text(p, x + tw(label, 'M', 8.6) + 2.5, y + 9, '*', 'S', 8.6, C['vivid'])
    by = y + 16
    rrect(p, (x, by, x + w, by + h), 7, fill=C['white'], color=C['mist'], width=0.8)
    if hint: text(p, x + 1, by + h + 11.5, hint, 'R', 7.2, C['slate'])
    return fitz.Rect(x + 9, by + 2, x + w - 9, by + h - 2), 16 + h + (16 if hint else 6)


def section(p, y, num, title, sub, h):
    """Card with a numbered header. Returns the y where content starts."""
    rrect(p, (MX, y, W - MX, y + h), 12, fill=C['white'], color=C['line'], width=0.9)
    rrect(p, (MX + 18, y + 16, MX + 44, y + 36), 6, fill=C['s100'])
    text(p, MX + 31, y + 29.6, num, 'S', 8.6, C['vivid'], 'center')
    text(p, MX + 54, y + 26, title, 'S', 12, C['logo'])
    text(p, MX + 54, y + 38.5, sub, 'R', 7.8, C['slate'])
    return y + 54


def button(p, r, label, kind, primary=False):
    r = fitz.Rect(r)
    if primary: rrect(p, r, r.height / 2, fill=C['vivid'])
    else: rrect(p, r, r.height / 2, fill=C['white'], color=C['s200'], width=0.9)
    col = C['white'] if primary else C['vivid']
    lw = tw(label, 'S', 8.8) + 16
    x0 = r.x0 + (r.width - lw) / 2
    icon(p, kind, x0 + 5.5, r.y0 + r.height / 2, 11, col)
    text(p, x0 + 16, r.y0 + r.height / 2 + 3.1, label, 'S', 8.8, col)


def header(p):
    wordmark(p, MX, 34, 98, C['vivid'])
    text(p, MX, 62, FORM_NAME, 'S', 7.6, C['ink'])
    text(p, W - MX, 45, 'Client Onboarding', 'S', 10.5, C['ink'], 'right')
    text(p, W - MX, 59, 'Interactive form · ' + YEAR, 'R', 7.8, C['slate'], 'right')
    line(p, (MX, 74), (W - MX, 74))


def footer(p, page_no, pages):
    text(p, MX, H - 30, f'{YEAR} Elevatus. All rights reserved.', 'R', 7.5, C['slate'])
    text(p, W / 2, H - 30, 'Confidential: shared with Elevatus for client coordination only', 'R', 7.5, C['slate'], 'center')
    text(p, W - MX, H - 30, f'Page {page_no} of {pages}', 'R', 7.5, C['slate'], 'right')


STEPS = [('open', 'Open', 'Any PDF reader'), ('fill', 'Fill', 'Steps 01 and 02'), ('review', 'Review', 'Check and confirm'),
         ('save', 'Save', 'Keep your copy'), ('send', 'Send', 'Email to Elevatus')]


def stepper(p, y):
    h = 66
    rrect(p, (MX, y, W - MX, y + h), 12, fill=C['paper'])
    n = len(STEPS); cw = CW / n
    cy = y + 22
    for i in range(n - 1):
        line(p, (MX + cw * i + cw / 2 + 15, cy), (MX + cw * (i + 1) + cw / 2 - 15, cy), C['s200'], 1, dashes='[2 2.5] 0')
    for i, (k, title, sub) in enumerate(STEPS):
        cx = MX + cw * i + cw / 2
        circle(p, (cx, cy), 12, fill=C['vivid'] if i == 0 else C['white'], color=None if i == 0 else C['s200'], width=0.9)
        icon(p, k, cx, cy, 11.5, C['white'] if i == 0 else C['vivid'])
        text(p, cx, y + 47, f'{i + 1}. {title}', 'S', 8.6, C['logo'], 'center')
        text(p, cx, y + 58, sub, 'R', 7.1, C['slate'], 'center')
    return h


def form_page(doc, page_no, pages):
    p = doc.new_page(width=W, height=H)
    fonts(p)
    header(p)
    toc = []

    # title + intro
    y = 100
    text(p, MX, y, 'CLIENT ONBOARDING', 'S', 7.6, C['vivid'], track=0.14)
    text(p, MX - 1, y + 30, 'Client Contact Details', 'L', 27, C['logo'])
    y += 52 + para(p, MX, y + 52, "Please provide your company's key contacts so the Elevatus team can coordinate effectively "
                   'with the right people. Include the country code in all contact numbers. No Google account or login is needed.',
                   'R', 9.4, 14.2, C['slate'], maxw=CW - 10) + 4

    y += stepper(p, y) + 14

    # 01 company
    sh = 124
    toc.append(('01  Company details', y))
    cy = section(p, y, '01', 'Company details', 'Who is registering with Elevatus', sh)
    gx, gap = MX + 18, 14
    iw = CW - 36
    dw = 150
    r, _ = field_box(p, gx, cy, dw, 'Date of Registration', 'Format DD/MM/YYYY')
    text_field(p, 'registration_date', 'Date of Registration (DD/MM/YYYY)', r, 'date', 10)
    r, _ = field_box(p, gx + dw + gap, cy, iw - dw - gap, 'Company Name', 'Registered company or trading name')
    text_field(p, 'company_name', 'Company Name', r, 'text', 120)
    y += sh + 10

    # 02 business decision maker
    sh = 188
    toc.append(('02  Business decision maker', y))
    cy = section(p, y, '02', 'Business decision maker', 'The person who signs off decisions for your company', sh)
    half = (iw - gap) / 2
    r, rh = field_box(p, gx, cy, iw, 'Business Decision Maker Name', 'First and last name')
    text_field(p, 'bdm_name', 'Business Decision Maker Name', r, 'text', 100)
    cy += rh + 2
    r, _ = field_box(p, gx, cy, half, 'Business Decision Maker Email', 'Work email, for example name@company.com')
    text_field(p, 'bdm_email', 'Business Decision Maker Email', r, 'email', 120)
    # contact number = country code + number
    xx = gx + half + gap
    ccw = 62
    text(p, xx, cy + 9, 'Business Decision Maker Contact Number', 'M', 8.6, C['ink'])
    text(p, xx + tw('Business Decision Maker Contact Number', 'M', 8.6) + 2.5, cy + 9, '*', 'S', 8.6, C['vivid'])
    by = cy + 16
    rrect(p, (xx, by, xx + ccw, by + 31), 7, fill=C['paper'], color=C['mist'], width=0.8)
    rrect(p, (xx + ccw + 6, by, xx + half, by + 31), 7, fill=C['white'], color=C['mist'], width=0.8)
    text(p, xx + 1, by + 31 + 11.5, 'Country code (e.g. +966) and number', 'R', 7.2, C['slate'])
    text_field(p, 'bdm_country_code', 'Contact number: country code, for example +966', (xx + 8, by + 2, xx + ccw - 6, by + 29), 'cc', 5)
    text_field(p, 'bdm_phone', 'Contact number without the country code', (xx + ccw + 15, by + 2, xx + half - 9, by + 29), 'phone', 18)
    y += sh + 10

    # 03 review & send
    sh = 190
    toc.append(('03  Review, save & send', y))
    cy = section(p, y, '03', 'Review, save & send', 'Check your answers, keep a copy, and send the form to Elevatus', sh)
    cb = checkbox(p, 'confirm_details', 'I confirm the details in this form are accurate', (gx, cy + 1, gx + 14, cy + 15))
    style_checkbox(doc, cb)
    para(p, gx + 22, cy + 11, 'I confirm the details above are accurate and that Elevatus may use them to contact these people '
         'about our account.', 'R', 8.8, 12.6, C['ink'], maxw=iw - 22)
    cy += 40
    bw, bh = (iw - 3 * 10) / 4, 30
    labels = [('Check form', 'review', 'check', False), ('Save PDF', 'save', 'save', False),
              ('Print', 'print', 'print', False), ('Email to Elevatus', 'send', 'send', True)]
    for i, (lab, ic, act, prim) in enumerate(labels):
        bx = gx + i * (bw + 10)
        button(p, (bx, cy, bx + bw, cy + bh), lab, ic, prim)
        push_button(p, f'btn_{act}', lab, (bx, cy, bx + bw, cy + bh), act)
    cy += bh + 12
    # fallback note for readers without form scripts
    nh = 38
    rrect(p, (gx, cy, gx + iw, cy + nh), 8, fill=C['apricot_tint'])
    icon(p, 'info', gx + 15, cy + 13.5, 11, C['apricot_ink'])
    note1 = 'Buttons not responding? Some browsers and phone viewers do not run form buttons.'
    text(p, gx + 28, cy + 16, note1, 'M', 7.9, C['apricot_ink'])
    note2a = 'Save the file (File › Save or Download), then email it to '
    text(p, gx + 28, cy + 28, note2a, 'R', 7.9, C['apricot_ink'])
    ex = gx + 28 + tw(note2a, 'R', 7.9)
    text(p, ex, cy + 28, SEND_TO, 'S', 7.9, C['vivid'])
    ew = tw(SEND_TO, 'S', 7.9)
    line(p, (ex, cy + 30), (ex + ew, cy + 30), C['vivid'], 0.5)
    p.insert_link({'kind': fitz.LINK_URI, 'from': fitz.Rect(ex, cy + 19, ex + ew, cy + 32),
                   'uri': f'mailto:{SEND_TO}?subject=Client%20Contact%20Details%20Form'})
    # clear link, bottom right of the note
    cl = 'Clear form'
    cx = gx + iw - 12 - tw(cl, 'M', 7.9)
    icon(p, 'clear', cx - 8, cy + 13.3, 9, C['apricot_ink'], 0.9)
    text(p, cx, cy + 16, cl, 'M', 7.9, C['apricot_ink'])
    push_button(p, 'btn_clear', 'Clear form', (cx - 15, cy + 6, gx + iw - 8, cy + 20), 'clear')

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
        rrect(p, (px, y, px + pw, y + 22), 11, color=white, width=0.7)
        icon(p, k, px + 12, y + 11, 10, white, 1)
        text(p, px + 23, y + 14.4, lab, 'M', 9, white)
        px += pw + (14 if i < len(STEPS) - 1 else 0)
        if i < len(STEPS) - 1:
            line(p, (px - 11, y + 11), (px - 3, y + 11), white, 0.7)
    for i, ln in enumerate(['CLIENT', 'ONBOARDING'][::-1]):
        text(p, x, H - 40 - i * 14.5, ln, 'M', 9.5, white, track=0.12)
    text(p, W - x, H - 40, 'Interactive Fillable Form', 'M', 11.5, white, 'right')
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
    doc.subset_fonts()
    os.makedirs(OUTPUT, exist_ok=True)
    name = f'Elevatus - {FORM_NAME}' + (' (with cover)' if with_cover else '') + '.pdf'
    path = os.path.join(OUTPUT, name)
    doc.save(path, garbage=4, deflate=True)
    return path


if __name__ == '__main__':
    for wc in (True, False):
        print(build(wc))
