# Word version of the Elevatus Client Contact Details Form.
#   python3 build.py && python3 build_docx.py
# Renders the cover (from the built PDF), the wordmark and step icons to PNG, runs word/make_docx.js (npm docx),
# then embeds the Inter fonts (assets/fonts-ttf) in the .docx so it looks the same on machines without Inter.
import json, os, re, subprocess, sys, tempfile, uuid, zipfile
import pymupdf as fitz
import build as B

DOCX = os.path.join(B.OUTPUT, f'Elevatus - {B.FORM_NAME}.docx')
TTF = os.path.join(B.ASSETS, 'fonts-ttf')
EMBED = [('Inter', 'Inter-Regular.ttf'), ('Inter Light', 'Inter-Light.ttf'),
         ('Inter Medium', 'Inter-Medium.ttf'), ('Inter SemiBold', 'Inter-SemiBold.ttf')]


def render_assets(tmp):
    out = {}
    # cover: the same brand cover as the PDF, labelled for Word, flattened to one image
    d = fitz.open(); B.cover(d, label='Fillable Form')
    pix = d[0].get_pixmap(dpi=200)
    out['cover'] = os.path.join(tmp, 'cover.jpg'); pix.save(out['cover'], jpg_quality=90)
    # wordmark, vivid on transparent
    w = 300; h = B.WM_BOX.height * w / B.WM_BOX.width
    d = fitz.open(); p = d.new_page(width=w, height=h); B.wordmark(p, 0, 0, w, B.C['vivid'])
    out['wordmark'] = os.path.join(tmp, 'wordmark.png'); p.get_pixmap(dpi=300, alpha=True).save(out['wordmark'])
    # step icons
    out['icons'] = {}
    for k, *_ in B.STEPS:
        d = fitz.open(); p = d.new_page(width=14, height=14); B.icon(p, k, 7, 7, 12, B.C['vivid'], 1)
        out['icons'][k] = os.path.join(tmp, f'icon-{k}.png'); p.get_pixmap(dpi=600, alpha=True).save(out['icons'][k])
    return out, B.WM_BOX.width / B.WM_BOX.height


def embed_fonts(path):
    """Embed the Inter TTFs as obfuscated fonts (ECMA-376 Part 1, 17.8.1)."""
    zin = zipfile.ZipFile(path); files = {n: zin.read(n) for n in zin.namelist()}; zin.close()
    rels, fonts_xml = [], []
    for i, (name, fn) in enumerate(EMBED, 1):
        key = '{' + str(uuid.uuid4()).upper() + '}'
        data = bytearray(open(os.path.join(TTF, fn), 'rb').read())
        kb = bytes.fromhex(key.strip('{}').replace('-', ''))[::-1]
        for j in range(32): data[j] ^= kb[j % 16]
        files[f'word/fonts/font{i}.odttf'] = bytes(data)
        rels.append(f'<Relationship Id="rIdF{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{i}.odttf"/>')
        fonts_xml.append(f'<w:font w:name="{name}"><w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>'
                         f'<w:embedRegular r:id="rIdF{i}" w:fontKey="{key}"/></w:font>')
    ft = files['word/fontTable.xml'].decode()
    for name, _ in EMBED:   # drop any plain entry docx wrote for the same name
        ft = re.sub(r'<w:font w:name="%s">.*?</w:font>' % re.escape(name), '', ft, flags=re.S)
    if 'xmlns:r=' not in ft.split('>', 2)[1]:
        ft = ft.replace('<w:fonts ', '<w:fonts xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    ft = re.sub(r'<w:fonts([^>]*?)\s*/>', r'<w:fonts\1></w:fonts>', ft)   # docx writes an empty, self-closing table
    ft = ft.replace('</w:fonts>', ''.join(fonts_xml) + '</w:fonts>')
    assert ft.count('w:embedRegular') == len(EMBED)
    files['word/fontTable.xml'] = ft.encode()
    files['word/_rels/fontTable.xml.rels'] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(rels) + '</Relationships>').encode()
    ct = files['[Content_Types].xml'].decode()
    if 'Extension="odttf"' not in ct:
        ct = ct.replace('</Types>', '<Default Extension="odttf" ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"/></Types>')
    files['[Content_Types].xml'] = ct.encode()
    st = files['word/settings.xml'].decode()
    if 'embedTrueTypeFonts' not in st:
        # schema order: ... displayBackgroundShape, printPostScriptOverText, printFractionalCharacterWidth, printFormsData,
        # embedTrueTypeFonts, embedSystemFonts, saveSubsetFonts ...
        anchor = re.search(r'<w:(?:printFormsData|printFractionalCharacterWidth|printPostScriptOverText|displayBackgroundShape)[^>]*/>', st)
        tag = '<w:embedTrueTypeFonts/><w:saveSubsetFonts/>'
        st = st[:anchor.end()] + tag + st[anchor.end():] if anchor else re.sub(r'(<w:settings[^>]*>)', r'\1' + tag, st, count=1)
    files['word/settings.xml'] = st.encode()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in ['[Content_Types].xml'] + [n for n in files if n != '[Content_Types].xml']: z.writestr(n, files[n])


def main():
    with tempfile.TemporaryDirectory() as tmp:
        assets, ratio = render_assets(tmp)
        spec = dict(assets=assets, wordmarkRatio=ratio, formName=B.FORM_NAME, year=B.YEAR,
                    intro="Please provide your company's key contacts so the Elevatus team can coordinate effectively with the "
                          'right people. All fields are required. Include the country code in all contact numbers.',
                    steps=[dict(icon='open', title='Open', sub='In Word or Google Docs'),
                           dict(icon='fill', title='Fill', sub='Sections 01 to 05'),
                           dict(icon='review', title='Review', sub='Check your answers')],
                    contacts=[dict(title=t[0].upper() + t[1:], label=l, sub=s) for _, t, l, s in B.CONTACTS])
        sp = os.path.join(tmp, 'spec.json'); json.dump(spec, open(sp, 'w'))
        env = dict(os.environ, NODE_PATH=subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip())
        subprocess.run(['node', os.path.join(B.HERE, 'word', 'make_docx.js'), sp, DOCX], check=True, env=env)
    embed_fonts(DOCX)
    print(DOCX)


if __name__ == '__main__':
    main()
