# Certificate of Attendance — Elevatus × Beyout AI

- `output/Certificate_Template.ai`: opens in Illustrator. Every text line is live type (not outlined).
- `output/Certificate_Template.pdf`: the same file as a PDF.
- `build_certificate.py`: rebuilds the template, or makes one PDF per name from Excel.
- `names.xlsx`: put the names in column A, starting at row 2.

## Fonts

Inter Regular / Medium / SemiBold are in `fonts/` (free, SIL OFL licence). Install them before you open
the `.ai`, so Illustrator keeps the text editable in the right font.

## Type spec (pt, US Letter landscape 792 × 612)

| Line | Font | Size | Tracking |
|---|---|---|---|
| CERTIFICATE OF ATTENDANCE | Inter Regular | 11 | 290 |
| THIS CERTIFIES THAT | Inter Regular | 12 | 20 |
| Name | Inter SemiBold | 38 (shrinks to fit long names) | 0 |
| has successfully participated… | Inter Regular | 10 | 0 |
| Session title | Inter Medium | 16 | 0 |
| Description (2 lines, 13 leading) | Inter Regular | 10 | 0 |
| Awarded on… | Inter Regular | 12.5 | 0 |
| Seal text | Inter Regular | 5.6 | 20 |
| Footer | Inter Medium | 7.5 | 120 |

## Batch from Excel

```
pip install reportlab openpyxl
python3 build_certificate.py --excel names.xlsx      # → output/PDF, output/AI, output/All_Certificates.pdf
```

Other wording (session, date, description) is in the `CONTENT` block at the top of the script.
Arabic names need an Arabic font and shaping, which this script does not do yet.
