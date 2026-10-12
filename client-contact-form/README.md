# Elevatus — Client Contact Details Form (interactive PDF)

Fillable A4 PDF that replaces the Google Form. Clients open it in any PDF reader (no Google account or login), fill it, review, save and email it back.

`output/Elevatus - Client Contact Details Form.pdf`: blue brand cover + two form pages.

The cover image is a key-contacts UI illustration built in `art/cover-illustration.html` and rendered to `assets/cover-contacts.png` (re-render it with Playwright/Chromium if you change it).

## Flow on the page
Open → Fill (01 to 05) → Review (confirmation tick) → **Save completed form** → the client sends the saved PDF back to the Elevatus team themselves. Bookmarks jump to each section; clicking the cover opens the form.

| Page | Sections |
|---|---|
| 1 | Intro, steps, 01 Company details, 02 Business decision maker, 03 Procurement contact |
| 2 | 04 Finance contact, 05 Escalation contact, 06 Review & save |

## Fields (all required)
| Field names | Labels | Checks |
|---|---|---|
| `registration_date` | Date of Registration | DD/MM/YYYY date |
| `company_name` | Company Name | trimmed |
| `{bdm,proc,fin,esc}_name` | … Name | trimmed |
| `{bdm,proc,fin,esc}_email` | … Email | email format |
| `{bdm,proc,fin,esc}_country_code` | … Contact Number (code) | digits only, 1–4 (`+` printed on the page) |
| `{bdm,proc,fin,esc}_phone` | … Contact Number | digits/spaces/hyphens, 6–14 digits |
| `confirm_details` | Confirmation tick | — |

`bdm` = Business Decision Maker, `proc` = Procurement, `fin` = Finance, `esc` = Escalation.

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
