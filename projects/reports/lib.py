# Elevatus documents: small flow-layout engine on PyMuPDF (reports and other paged documents).
# Vector output with live Inter text (Illustrator-editable), colours from brand/tokens.
# How to use it, and the rules for rebranded reports: .claude/skills/elevatus-documents/SKILL.md
import pymupdf as fitz, os, re, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))   # the creative coding folder
BRAND = os.path.join(ROOT, 'brand')              # shared identity: logo, fonts, tokens
FONTS = os.path.join(BRAND, 'fonts')
OUTPUT = os.path.join(HERE, 'output')            # finished PDFs
WORDMARK_SVG = os.path.join(BRAND, 'elevatus-wordmark.svg')

ASSETS = os.path.join(HERE, 'assets')
W, H = 595.28, 841.89    # A4, same as the cover
MX = 48                  # side margin
TOP, BOTTOM = 98, H - 62 # content area
CW = W - 2 * MX

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
C = dict(vivid=rgb('1B15CF'), logo=rgb('051274'), electric=rgb('2962FF'), apricot=rgb('F0A15C'),
         ink=rgb('11162B'), slate=rgb('586177'), mist=rgb('C7D0E1'), line=rgb('E3E7F0'), paper=rgb('F4F7FF'),
         white=(1, 1, 1), night=rgb('07051F'),
         s900=rgb('0F0A3F'), s800=rgb('1A126B'), s700=rgb('241A94'), s600=rgb('2F24B8'),
         s400=rgb('6F7DFF'), s300=rgb('A9B4FF'), s200=rgb('C9D4FF'), s100=rgb('E4EBFF'), s50=rgb('F4F7FF'),
         apricot_tint=rgb('FDEFE2'), apricot_ink=rgb('8A4A12'))

FONTFILES = {'L': 'Inter-Light', 'R': 'Inter-Regular', 'M': 'Inter-Medium', 'S': 'Inter-SemiBold'}
FONTOBJ = {k: fitz.Font(fontfile=os.path.join(FONTS, v + '.ttf')) for k, v in FONTFILES.items()}

def tw(s, f, size): return FONTOBJ[f].text_length(s, fontsize=size)

# ---------------------------------------------------------------- wordmark (vector)
_wm = fitz.open('pdf', fitz.open(WORDMARK_SVG).convert_to_pdf())
WM_DRAW = [d for d in _wm[0].get_drawings() if d.get('fill') is not None]
WM_BOX = fitz.Rect(WM_DRAW[0]['rect'])
for _d in WM_DRAW[1:]: WM_BOX |= _d['rect']
WM_RATIO = WM_BOX.width / WM_BOX.height

def wordmark(p, x, y, width, color=C['vivid']):
    s = width / WM_BOX.width
    M_ = fitz.Matrix(s, 0, 0, s, x - WM_BOX.x0 * s, y - WM_BOX.y0 * s)
    sh = p.new_shape()
    for d in WM_DRAW:
        for it in d['items']:
            k = it[0]
            if k == 'l': sh.draw_line(it[1] * M_, it[2] * M_)
            elif k == 'c': sh.draw_bezier(it[1] * M_, it[2] * M_, it[3] * M_, it[4] * M_)
            elif k == 're': sh.draw_quad(fitz.Quad(it[1]) * M_)
            elif k == 'qu': sh.draw_quad(it[1] * M_)
        sh.finish(fill=color, color=None, closePath=True)
    sh.commit()
    return width / WM_RATIO

# ---------------------------------------------------------------- primitives
def text(p, x, y, s, f='R', size=10, color=C['ink'], align='left', opacity=1, track=0):
    """Single line; y is the baseline. track = letter-spacing in em."""
    if align != 'left':
        w = tw(s, f, size) + track * size * max(len(s) - 1, 0)
        x = x - w if align == 'right' else x - w / 2
    before = len(p.get_contents())
    p.insert_text((x, y), s, fontname='I' + f, fontsize=size, color=color, fill_opacity=opacity)
    if track:
        doc = p.parent
        for xr in p.get_contents()[before:]:
            st = doc.xref_stream(xr).decode('latin-1').replace(' Tf ', f' Tf {track * size:.3f} Tc ', 1)
            doc.update_stream(xr, st.encode('latin-1'))

def rrect(p, r, radius=0, fill=None, color=None, width=1, opacity=1):
    r = fitz.Rect(r)
    rad = min(radius / min(r.width, r.height), 0.5) if radius else None
    p.draw_rect(r, fill=fill, color=color, width=width, radius=rad, fill_opacity=opacity, stroke_opacity=opacity)

def line(p, a, b, color=C['line'], width=0.75, opacity=1):
    p.draw_line(fitz.Point(a), fitz.Point(b), color=color, width=width, stroke_opacity=opacity)

def circle(p, c, r, fill=None, color=None, width=1, opacity=1):
    p.draw_circle(fitz.Point(c), r, fill=fill, color=color, width=width, fill_opacity=opacity, stroke_opacity=opacity)

def poly(p, pts, fill=None, color=None, width=1, opacity=1, stroke_opacity=None):
    sh = p.new_shape()
    sh.draw_polyline([fitz.Point(q) for q in pts])
    sh.finish(fill=fill, color=color, width=width, closePath=True, fill_opacity=opacity,
              stroke_opacity=opacity if stroke_opacity is None else stroke_opacity, lineJoin=1)
    sh.commit()

def ring_segment(p, c, r0, r1, a0, a1, fill):
    """Donut segment; angles in degrees, clockwise from 12 o'clock."""
    def pt(r, a): t = math.radians(a - 90); return (c[0] + r * math.cos(t), c[1] + r * math.sin(t))
    n = max(int(abs(a1 - a0) / 1.5), 2)
    outer = [pt(r1, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    inner = [pt(r0, a1 - (a1 - a0) * i / n) for i in range(n + 1)] if r0 > 0 else [c]
    poly(p, outer + inner, fill=fill)

def bar(p, x, y, w, h, frac, fill=C['vivid'], track=C['s100']):
    rrect(p, (x, y, x + w, y + h), h / 2, fill=track)
    if frac > 0: rrect(p, (x, y, x + max(w * frac, h), y + h), h / 2, fill=fill)

# ---------------------------------------------------------------- rich text (**bold** markup)
def _words(s, f, fb):
    chars = []; bold = False
    for part in re.split(r'(\*\*)', s):
        if part == '**': bold = not bold; continue
        chars += [(ch, fb if bold else f) for ch in part]
    words = []; cur = []
    for ch, fo in chars:
        if ch == ' ':
            if cur: words.append(cur); cur = []
        elif cur and cur[-1][1] == fo: cur[-1][0] += ch
        else: cur.append([ch, fo])
    if cur: words.append(cur)
    return words

def layout(s, size, maxw, f='R', fb='S'):
    """Returns list of lines; a line is a list of (text, font) runs."""
    sp = tw(' ', f, size); lines = []
    for para in s.split('\n'):
        cur = []; curw = 0
        for wd in _words(para, f, fb):
            ww = sum(tw(t, fo, size) for t, fo in wd)
            if cur and curw + sp + ww > maxw:
                lines.append(cur); cur = []; curw = 0
            if cur: curw += sp
            cur.append(wd); curw += ww
        lines.append(cur)
    out = []
    for ln in lines:
        runs = []
        for i, wd in enumerate(ln):
            for j, (t, fo) in enumerate(wd):
                lead_sp = ' ' if (i > 0 and j == 0) else ''
                if runs and runs[-1][1] == fo: runs[-1][0] += lead_sp + t
                else:
                    if lead_sp and runs: runs[-1][0] += ' '
                    runs.append([t, fo])
        out.append(runs)
    return out

def draw_lines(p, x, y, lines, size, lead, color=C['ink'], align='left', maxw=None, bold_color=None):
    """y = top of the first line box."""
    for i, runs in enumerate(lines):
        bx = x
        if align != 'left':
            lw = sum(tw(t, fo, size) for t, fo in runs)
            bx = x + (maxw - lw) / (2 if align == 'center' else 1)
        by = y + lead * 0.74 + i * lead
        for t, fo in runs:
            col = bold_color if (bold_color and fo == 'S') else color
            p.insert_text((bx, by), t, fontname='I' + fo, fontsize=size, color=col)
            bx += tw(t, fo, size)
    return len(lines) * lead

def rich_h(s, size, lead, maxw, f='R', fb='S'): return len(layout(s, size, maxw, f, fb)) * lead

def rich(p, x, y, s, size, lead, maxw, color=C['ink'], f='R', fb='S', align='left', bold_color=None):
    return draw_lines(p, x, y, layout(s, size, maxw, f, fb), size, lead, color, align, maxw, bold_color)

def bullets_h(items, size, lead, maxw, gap=3, indent=12):
    return sum(rich_h(it, size, lead, maxw - indent) + gap for it in items) - gap

def bullets(p, x, y, items, size, lead, maxw, color=C['ink'], dot=C['vivid'], gap=3, indent=12, bold_color=None):
    y0 = y
    for it in items:
        circle(p, (x + 2.5, y + lead * 0.5), 1.6, fill=dot)
        y += rich(p, x + indent, y, it, size, lead, maxw - indent, color, bold_color=bold_color) + gap
    return y - gap - y0

# ---------------------------------------------------------------- report (flow)
def fonts(p):
    for k, v in FONTFILES.items():
        p.insert_font(fontname='I' + k, fontfile=os.path.join(FONTS, v + '.ttf'))

def cover(doc, title, description='', category='', label='', bg='cover-bg.png', image='cover-mockup.png'):
    """The Elevatus document cover (full-bleed blue field, white wordmark, title, product image).
    title / description wrap on their own; category sits bottom left (set in caps), label bottom right.
    Pass image=None for a cover without the product mockup."""
    p = doc.new_page(pno=0, width=W, height=H)
    fonts(p)
    p.insert_image(p.rect, filename=os.path.join(ASSETS, bg), keep_proportion=False)
    if image:
        # the device bleeds off the left edge and stops short of the right margin, as in the master cover
        iw = W * 1.255
        pix = fitz.Pixmap(os.path.join(ASSETS, image)); ih = iw * pix.height / pix.width
        x1 = W; y0 = max(H * 0.392, H - 96 - ih)
        p.insert_image(fitz.Rect(x1 - iw, y0, x1, y0 + ih), filename=os.path.join(ASSETS, image))
    x = 40; white = C['white']
    y = 58 + wordmark(p, x, 58, 178, white)
    y += 46
    size, lead = 44, 50
    while size > 30 and len(layout(title, size, W - 2 * x, f='L')) > 3: size -= 2; lead = size * 1.14
    y += rich(p, x - 2, y, title, size, lead, W - 2 * x, white, f='L')
    if description:
        y += 14
        rich(p, x, y, description, 13.5, 19.5, 440, white, f='R')
    for i, ln in enumerate(category.upper().split('\n')[::-1]):
        text(p, x, H - 40 - i * 14.5, ln, 'M', 9.5, white, track=0.12)
    if label: text(p, W - x, H - 40, label, 'M', 11.5, white, 'right')
    return p

class Report:
    """person / date: top right of every page. name: the report's name under the logo. year: footer copyright year."""
    def __init__(self, person, date, name, year, title=None):
        self.doc = fitz.open(); self.person = person; self.date = date; self.name = name; self.year = year
        self.doc.set_metadata({'title': title or name, 'author': 'Elevatus', 'creator': 'Elevatus', 'producer': 'Elevatus'})
        self.p = None; self.y = TOP; self.has_cover = False
        self.new_page()

    def cover(self, title, description='', category='', label='', **kw):
        cover(self.doc, title, description, category, label, **kw); self.has_cover = True

    def new_page(self):
        p = self.doc.new_page(width=W, height=H)
        fonts(p)
        wordmark(p, MX, 34, 98, C['vivid'])
        text(p, MX, 62, self.name, 'S', 7.6, C['ink'])
        text(p, W - MX, 45, self.person, 'S', 10.5, C['ink'], 'right')
        text(p, W - MX, 59, self.date, 'R', 7.8, C['slate'], 'right')
        line(p, (MX, 74), (W - MX, 74))
        self.p = p; self.y = TOP
        return p

    def ensure(self, h):
        if self.y + h > BOTTOM: self.new_page()

    def space(self, h): self.y += h

    # headings
    def h1(self, s, keep=90, size=17):
        self.ensure(keep + 30)
        self.y += rich(self.p, MX, self.y, s, size, size * 1.3, CW, C['logo'], f='S') + 8

    def h2(self, s, keep=60, size=12.5, x=MX, color=C['logo']):
        self.ensure(keep + 22)
        self.y += rich(self.p, x, self.y, s, size, size * 1.4, CW, color, f='S') + 5

    def h3(self, s, keep=40, size=10.5, color=C['ink'], f='S'):
        self.ensure(keep + 18)
        self.y += rich(self.p, MX, self.y, s, size, size * 1.45, CW, color, f=f) + 4

    def para(self, s, size=9.5, lead=14.6, color=C['ink'], after=8, x=MX, maxw=None):
        maxw = maxw or (W - MX - x)
        lines = layout(s, size, maxw)
        if len(lines) <= 9: self.ensure(len(lines) * lead)
        for ln in lines:
            self.ensure(lead)
            draw_lines(self.p, x, self.y, [ln], size, lead, color)
            self.y += lead
        self.y += after

    def bullets(self, items, size=9.5, lead=14.6, color=C['ink'], after=8, x=MX + 8, gap=5):
        maxw = W - MX - x
        for it in items:
            h = rich_h(it, size, lead, maxw - 12)
            self.ensure(h)
            bullets(self.p, x, self.y, [it], size, lead, maxw, color)
            self.y += h + gap
        self.y += after - gap

    def table(self, widths, header, rows, size=9.2, lead=13.4, pad=(9, 8), head_size=8.6, renderers=None, color=C['ink']):
        """rows: list of lists of rich strings. renderers: {col: fn(p, x, y, w, value) -> None, height fn}."""
        renderers = renderers or {}
        xs = [MX]
        for w in widths: xs.append(xs[-1] + w)
        def row_h(r):
            hs = []
            for i, cell in enumerate(r):
                if i in renderers: hs.append(renderers[i][1](cell, widths[i] - 2 * pad[0]))
                else: hs.append(rich_h(cell, size, lead, widths[i] - 2 * pad[0]))
            return max(hs) + 2 * pad[1]
        hh = 24
        total = hh + sum(row_h(r) for r in rows)
        self.ensure(total if total < BOTTOM - TOP else hh + row_h(rows[0]))
        def head():
            rrect(self.p, (MX, self.y, xs[-1], self.y + hh), 5, fill=C['paper'])
            for i, t in enumerate(header):
                text(self.p, xs[i] + pad[0], self.y + 15.3, t, 'S', head_size, C['logo'])
            self.y += hh
        head()
        for r in rows:
            h = row_h(r)
            if self.y + h > BOTTOM: self.new_page(); head()
            for i, cell in enumerate(r):
                if i in renderers: renderers[i][0](self.p, xs[i] + pad[0], self.y + pad[1], widths[i] - 2 * pad[0], cell, h - 2 * pad[1])
                else: rich(self.p, xs[i] + pad[0], self.y + pad[1], cell, size, lead, widths[i] - 2 * pad[0], color)
            self.y += h
            line(self.p, (MX, self.y), (xs[-1], self.y))

    def save(self, path):
        first = 1 if self.has_cover else 0  # the cover carries no header, footer or page number
        n = len(self.doc) - first
        for i, p in enumerate(self.doc):
            if i < first: continue
            text(p, MX, H - 30, f'{self.year} Elevatus. All rights reserved.', 'R', 7.5, C['slate'])
            text(p, W - MX, H - 30, f'Page {i - first + 1} of {n}', 'R', 7.5, C['slate'], 'right')
        self.doc.subset_fonts()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.doc.save(path, garbage=4, deflate=True)
        return n
