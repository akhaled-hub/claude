// Builds the Word version of the Elevatus Client Contact Details Form from a JSON spec.
// Run through ../build_docx.py, which renders the images first and embeds the Inter fonts afterwards.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, BorderStyle,
  ShadingType, VerticalAlign, HeightRule, AlignmentType, TabStopType, Header, Footer, PageNumber,
  HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType, SectionType,
} = require('docx');

const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const A = spec.assets;
const C = { vivid: '1B15CF', logo: '051274', ink: '11162B', slate: '586177', mist: 'C7D0E1', line: 'E3E7F0',
            paper: 'F4F7FF', s200: 'C9D4FF', white: 'FFFFFF' };
const F = { L: 'Inter Light', R: 'Inter', M: 'Inter Medium', S: 'Inter SemiBold' };
const PAGE_W = 11906, PAGE_H = 16838, MX = 960, CW = PAGE_W - 2 * MX;   // A4, 48pt side margins
const pt = v => Math.round(v * 2);                                         // half-points

const run = (text, f = 'R', size = 10, color = C.ink, extra = {}) =>
  new TextRun({ text, font: F[f], size: pt(size), color, ...extra });
const img = (file, wPt, hPt, extra = {}) =>
  new ImageRun({ type: file.endsWith('.png') ? 'png' : 'jpg', data: fs.readFileSync(file),
                 transformation: { width: wPt * 96 / 72, height: hPt * 96 / 72 }, ...extra });
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const NO_BORDERS = { top: NONE, bottom: NONE, left: NONE, right: NONE };
const BOX = { style: BorderStyle.SINGLE, size: 6, color: C.mist };
const spacer = (after, keepNext = false) => new Paragraph({ keepNext, spacing: { before: 0, after, line: 40, lineRule: 'exact' }, children: [run('', 'R', 2)] });

// ---------------------------------------------------------------- cover (full-bleed image of the brand cover)
const coverSection = {
  properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 0, bottom: 0, left: 0, right: 0, header: 0, footer: 0 } } },
  children: [new Paragraph({ spacing: { before: 0, after: 0, line: 20, lineRule: 'exact' }, children: [
    img(A.cover, 595.3, 841.9, { floating: {
      horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
      verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
      behindDocument: true, allowOverlap: true, wrap: { type: TextWrappingType.NONE }, zIndex: 0 },
      altText: { title: 'Cover', description: 'Elevatus Client Contact Details Form cover', name: 'cover' } }),
  ] })],
};

// ---------------------------------------------------------------- header / footer
const header = new Header({ children: [
  new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: CW }], spacing: { after: 40 }, children: [
    img(A.wordmark, 98, 98 / spec.wordmarkRatio), run('\tClient Onboarding', 'S', 10.5, C.ink) ] }),
  new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: CW }], spacing: { after: 0 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C.line, space: 8 } }, children: [
    run(spec.formName, 'S', 7.6, C.ink), run('\tFillable form · ' + spec.year, 'R', 7.8, C.slate) ] }),
] });
const footer = new Footer({ children: [
  new Paragraph({ style: 'FooterText', tabStops: [{ type: TabStopType.CENTER, position: CW / 2 }, { type: TabStopType.RIGHT, position: CW }],
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: C.line, space: 8 } }, children: [
    run(`${spec.year} Elevatus. All rights reserved.`, 'R', 7.5, C.slate),
    run('\tConfidential: shared with Elevatus for client coordination only', 'R', 7.5, C.slate),
    new TextRun({ children: ['\tPage ', PageNumber.CURRENT], font: F.R, size: pt(7.5), color: C.slate }),
  ] }),
] });

// ---------------------------------------------------------------- building blocks
function steps() {
  const n = spec.steps.length, w = Math.floor(CW / n);
  const widths = Array(n).fill(w); widths[n - 1] = CW - w * (n - 1);
  const sep = { style: BorderStyle.SINGLE, size: 6, color: C.s200 };
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: widths,
    borders: { ...NO_BORDERS, insideHorizontal: NONE, insideVertical: NONE },
    rows: [new TableRow({ children: spec.steps.map((s, i) => new TableCell({
      width: { size: widths[i], type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: 'auto', fill: C.paper },
      borders: { top: NONE, bottom: NONE, left: i ? sep : NONE, right: NONE },
      margins: { top: 120, bottom: 120, left: 240, right: 120 }, verticalAlign: VerticalAlign.CENTER,
      children: [
        new Paragraph({ spacing: { after: 20 }, children: [img(A.icons[s.icon], 11, 11), run(`   ${i + 1}  ${s.title}`, 'S', 8.6, C.logo)] }),
        new Paragraph({ indent: { left: 330 }, spacing: { after: 0 }, children: [run(s.sub, 'R', 7, C.slate)] }),
      ] })) })] });
}

function sectionHead(num, title, sub, pageBreak) {
  return [
    new Paragraph({ pageBreakBefore: !!pageBreak, keepNext: true, spacing: { before: pageBreak ? 0 : 400, after: 30 },
      tabStops: [{ type: TabStopType.LEFT, position: 480 }], children: [run(num, 'S', 10, C.vivid), run('\t' + title, 'S', 12, C.logo)] }),
    new Paragraph({ keepNext: true, indent: { left: 480 }, spacing: { after: 170 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C.line, space: 10 } },
      children: [run(sub, 'R', 8, C.slate)] }),
  ];
}

// One row of fields. cols: [{w, input?, fill?, prefill?}], labels/hints: [{span, text}]
function fieldRow(cols, labels, hints, keep = false) {
  const widths = cols.map(c => c.w);
  const spanCells = (items, mk) => {
    let i = 0; return items.map(it => { const w = widths.slice(i, i + it.span).reduce((a, b) => a + b, 0); i += it.span;
      return new TableCell({ columnSpan: it.span, width: { size: w, type: WidthType.DXA }, borders: NO_BORDERS,
        margins: { top: 0, bottom: 0, left: 0, right: 0 }, children: [mk(it)] }); });
  };
  const labelRow = new TableRow({ cantSplit: true, children: spanCells(labels, it => new Paragraph({ keepNext: true, spacing: { after: 70 },
    children: it.text ? [run(it.text, 'M', 8.5, C.ink), run(' *', 'S', 8.5, C.vivid)] : [run('', 'R', 2)] })) });
  const inputRow = new TableRow({ cantSplit: true, height: { value: 560, rule: HeightRule.ATLEAST }, children: cols.map(c => new TableCell({
    width: { size: c.w, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
    borders: c.input ? { top: BOX, bottom: BOX, left: BOX, right: BOX } : NO_BORDERS,
    shading: c.input ? { type: ShadingType.CLEAR, color: 'auto', fill: c.fill || C.white } : undefined,
    margins: { top: 60, bottom: 60, left: c.input ? 160 : 0, right: c.input ? 120 : 0 },
    children: [new Paragraph({ keepNext: true, spacing: { after: 0 }, children: [run(c.prefill || '', 'R', 10.5, C.ink)] })] })) });
  const hintRow = new TableRow({ cantSplit: true, children: spanCells(hints, it => new Paragraph({ keepNext: !!keep, spacing: { before: 50, after: 0 },
    children: [run(it.text || '', 'R', 7, C.slate)] })) });
  return [new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: widths, borders: { ...NO_BORDERS, insideHorizontal: NONE, insideVertical: NONE },
    rows: [labelRow, inputRow, hintRow] }), spacer(70, keep)];
}

const GAP = 320, HALF = Math.floor((CW - GAP) / 2), CC = 1200, CCGAP = 120;

function contactRows(lab) {
  const numLab = lab.endsWith('Contact') ? `${lab} Number` : `${lab} Contact Number`;
  return [
    ...fieldRow([{ w: CW, input: true }], [{ span: 1, text: `${lab} Name` }], [{ span: 1, text: 'First and last name' }], true),
    ...fieldRow(
      [{ w: HALF, input: true }, { w: GAP }, { w: CC, input: true, fill: C.paper, prefill: '+' }, { w: CCGAP }, { w: CW - HALF - GAP - CC - CCGAP, input: true }],
      [{ span: 1, text: `${lab} Email` }, { span: 1 }, { span: 3, text: numLab }],
      [{ span: 1, text: 'Work email, for example name@company.com' }, { span: 1 }, { span: 3, text: 'Country code (e.g. +966), then the number' }]),
  ];
}

// ---------------------------------------------------------------- form
const body = [
  new Paragraph({ spacing: { before: 0, after: 120 }, children: [run('CLIENT ONBOARDING', 'S', 7.4, C.vivid, { characterSpacing: 21 })] }),
  new Paragraph({ spacing: { after: 120 }, children: [run('Client Contact Details', 'L', 26, C.logo)] }),
  new Paragraph({ spacing: { after: 220, line: 284, lineRule: 'exact' }, children: [run(spec.intro, 'R', 9.4, C.slate)] }),
  steps(),
  ...sectionHead('01', 'Company details', 'Who is registering with Elevatus.'),
  ...fieldRow([{ w: 3000, input: true }, { w: GAP }, { w: CW - 3000 - GAP, input: true }],
    [{ span: 1, text: 'Date of Registration' }, { span: 1 }, { span: 1, text: 'Company Name' }],
    [{ span: 1, text: 'DD/MM/YYYY' }, { span: 1 }, { span: 1, text: 'Registered company or trading name' }]),
];
spec.contacts.forEach((c, i) => {
  body.push(...sectionHead(String(i + 2).padStart(2, '0'), c.title, c.sub, i === 2), ...contactRows(c.label));
});

const doc = new Document({
  creator: 'Elevatus', title: 'Elevatus ' + spec.formName, description: 'Client onboarding: key contacts',
  styles: { default: { document: { run: { font: F.R, size: pt(10), color: C.ink }, paragraph: { spacing: { after: 0 } } } },
    paragraphStyles: [{ id: 'FooterText', name: 'Footer Text', run: { font: F.R, size: pt(7.5), color: C.slate } }] },
  sections: [
    coverSection,
    { properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, pageNumbers: { start: 1 },
        margin: { top: 1900, bottom: 1300, left: MX, right: MX, header: 680, footer: 560 } } },
      headers: { default: header }, footers: { default: footer }, children: body },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[3], b); console.log('wrote', process.argv[3]); });
