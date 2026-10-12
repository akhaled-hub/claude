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
| `bdm_country_code` | Contact number: country code | digits only, 1–4 digits, `+` added |
| `bdm_phone` | Contact number | digits/spaces/hyphens, 6–14 digits |
| `confirm_details` | Confirmation tick | — |

## Saving
- **Save completed form** runs the reader's own Save As command (a PDF named action, no script). It works in Adobe Acrobat/Reader and in pdf.js-based viewers such as Firefox.
- When saving in Acrobat/Reader, a reminder lists any required field that is still empty (the save still goes ahead).
- No PDF button can save in every reader: Chrome/Edge's built-in viewers, macOS Preview and most phone viewers ignore it. The short note beside the button tells the client how to save there (File › Save, Download, Share › Save to Files). Typing into the fields and saving work in all of them.
- Field validation (date, email, phone) runs in Acrobat/Reader, Foxit and PDF-XChange; other readers just accept the text.

## Rebuild
```
pip install pymupdf pillow
python3 build.py
```
Assets: `assets/cover-bg.png`, `assets/cover-mockup.png` (from the reports cover template), `assets/elevatus-wordmark.svg`, Inter (`assets/fonts`, OFL).
