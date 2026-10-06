# Elevatus — A5 roll-fold tri-fold brochure

Flat 442 × 210 mm (148 + 148 + 146 tuck-in), A5 closed. Built in HTML/CSS/SVG with Inter, exported to print PDF.

| Side | Mode | Panels (left → right) |
|---|---|---|
| A · Outside | Dark | P02 Proof, scale & trust (tuck-in) · P06 Back / CTA · P01 Front cover |
| B · Inside | Light | P03 How Elevatus works · P04 Connected ecosystem · P05 One platform |

Reading journey: cover hook → proof & trust → challenges answered → fits your stack → what each product does → scan / book a demo.

## Files
- `index.html`, `styles.css`, `brochure.js`: the brochure. The infographics (rings, ecosystem wiring, hero orbit, laurels, seals, product glyphs) are generated as SVGs in millimetre units.
- `assets/`: Inter font, backgrounds, client logos and photos (taken from the use-case frames), integration logos (Iconify `logos` / Simple Icons), QR → elevatus.io.
- `dist/`: exported `Elevatus_Trifold_A5_trim.pdf`, `Elevatus_Trifold_A5_bleed3mm.pdf` and PNG previews.

## Rebuild
```
cd tools && npm install
node build-assets.mjs   # integration logos + QR
node export.mjs         # PDFs + previews
```
Open `index.html?guides` to see the fold lines.

## Still to swap in before print
- RE/MAX, Bank ABC, Capital Bank, JKB and AlRaedah are typeset placeholders: replace them with the official files from the previous brochure.
- Award and certification marks are drawn renditions: replace them with the official badge artwork, and confirm SOC 2 / CSA STAR status.
- Confirm the contact email (`info@elevatus.io`) and the QR destination (a tracked link).
