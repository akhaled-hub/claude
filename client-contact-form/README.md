# Elevatus — Client Contact Details Form (interactive PDF)

Fillable A4 PDF that replaces the Google Form. Clients open it in any PDF reader (no Google account or login), fill it, review, save and email it back.

| File | What it is |
|---|---|
| `output/Elevatus - Client Contact Details Form (with cover).pdf` | Blue brand cover + the form page |
| `output/Elevatus - Client Contact Details Form.pdf` | The form page only (light, formal) |

## Flow on the page
Open → Fill (01 Company details, 02 Business decision maker) → Review (confirmation tick) → **Save completed form** → the client sends the saved PDF back to the Elevatus team themselves. Bookmarks jump to each section; clicking the cover opens the form.

## Fields (all required)
| Field name | Label | Checks |
|---|---|---|
| `registration_date` | Date of Registration | DD/MM/YYYY date |
| `company_name` | Company Name | trimmed |
| `bdm_name` | Business Decision Maker Name | trimmed |
| `bdm_email` | Business Decision Maker Email | email format, lower-cased |
| `bdm_country_code` | Contact number: country code | digits only, 1–4 digits (`+` printed on the page) |
| `bdm_phone` | Contact number | digits/spaces/hyphens, 6–14 digits |
| `confirm_details` | Confirmation tick | — |

## Saving
The **Save completed form** button picks a route for each reader:

| Reader | What the button does | Checked |
|---|---|---|
| Adobe Acrobat / Reader (Windows, Mac, mobile), Foxit | `app.execMenuItem("SaveAs")` opens Save As | from Adobe's JS API; not run here |
| Firefox and other pdf.js viewers | same call; pdf.js implements `execMenuItem("SaveAs")` | from pdf.js source |
| Chrome's built-in viewer (PDFium, `app.viewerType == "pdfium"`) | PDFium refuses `execMenuItem`, so the button shows a one-line tip and opens Print with **Save as PDF**; the saved copy keeps all the filled data | tested in Chromium |
| macOS Preview, Safari, iPhone Files / Quick Look | these readers run no PDF scripts; the note beside the button explains File › Save / Share › Save to Files | — |

Field checks (date, email, phone digits) also run in Chrome's viewer, as well as in Acrobat. The `+` before the country code is printed on the page, so the client types digits only and the number reads the same in every reader. When saving in Acrobat/Reader, a reminder lists any required field still empty (the save still goes ahead).

## Rebuild
```
pip install pymupdf pillow
python3 build.py
```
Assets: `assets/cover-bg.png`, `assets/cover-mockup.png` (from the reports cover template), `assets/elevatus-wordmark.svg`, Inter (`assets/fonts`, OFL).
