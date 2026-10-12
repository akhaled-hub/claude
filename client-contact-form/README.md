# Elevatus — Client Contact Details Form (interactive PDF)

Fillable A4 PDF that replaces the Google Form. Clients open it in any PDF reader (no Google account or login), fill it, review, save and email it back.

| File | What it is |
|---|---|
| `output/Elevatus - Client Contact Details Form (with cover).pdf` | Blue brand cover + the form page |
| `output/Elevatus - Client Contact Details Form.pdf` | The form page only (light, formal) |

## Flow on the page
Open → Fill (01 Company details, 02 Business decision maker) → Review (confirmation tick + **Check form**) → **Save PDF** → **Email to Elevatus**. Bookmarks jump to each section; clicking the cover opens the form.

## Fields (all required)
| Field name | Label | Checks |
|---|---|---|
| `registration_date` | Date of Registration | DD/MM/YYYY date |
| `company_name` | Company Name | trimmed |
| `bdm_name` | Business Decision Maker Name | trimmed |
| `bdm_email` | Business Decision Maker Email | email format, lower-cased |
| `bdm_country_code` | Contact number: country code | digits only, 1–4 digits, `+` added |
| `bdm_phone` | Contact number | digits/spaces/hyphens, 6–14 digits |
| `confirm_details` | Confirmation tick | must be ticked before sending |

**Email to Elevatus** checks every required field, then opens an email with the filled PDF attached (`mailDoc`) to `SEND_TO` in `build.py` (currently `info@elevatus.io`).

## Reader support
- Adobe Acrobat / Reader (Windows, macOS, mobile), Foxit, PDF-XChange: filling, validation, all buttons.
- macOS Preview, Chrome/Edge/Firefox viewers, most phone viewers: filling and saving work; form scripts (validation, buttons) do not run there. The orange note on the page tells the client to save the file and email it, with a clickable `mailto:` link that works everywhere.

## Rebuild
```
pip install pymupdf pillow
python3 build.py
```
Assets: `assets/cover-bg.png`, `assets/cover-mockup.png` (from the reports cover template), `assets/elevatus-wordmark.svg`, Inter (`assets/fonts`, OFL).
