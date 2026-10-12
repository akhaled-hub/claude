# Elevatus — Client Contact Details Form (interactive PDF)

Fillable A4 PDF that replaces the Google Form. Clients open it in any PDF reader (no Google account or login), fill it, review, save and email it back.

`output/Elevatus - Client Contact Details Form.pdf`: blue brand cover + two form pages.

The cover image is a key-contacts UI illustration built in `art/cover-illustration.html` and rendered to `assets/cover-contacts.png` (re-render it with Playwright/Chromium if you change it).

## Flow on the page
Open → Fill (01 to 05) → Review. The steps strip on the cover and the first form page shows these three steps. Bookmarks jump to each section; clicking the cover opens the form.

| Page | Sections |
|---|---|
| 1 | Intro, steps, 01 Company details, 02 Business decision maker, 03 Procurement contact |
| 2 | 04 Finance contact, 05 Escalation contact |

## Fields (all required)
| Field names | Labels |
|---|---|
| `registration_date` | Date of Registration (hint: DD/MM/YYYY) |
| `company_name` | Company Name |
| `{bdm,proc,fin,esc}_name` | … Name |
| `{bdm,proc,fin,esc}_email` | … Email |
| `{bdm,proc,fin,esc}_country_code` | … Contact Number: country code (the `+` is printed on the page, max 4 characters) |
| `{bdm,proc,fin,esc}_phone` | … Contact Number |

`bdm` = Business Decision Maker, `proc` = Procurement, `fin` = Finance, `esc` = Escalation.

## Why the fields have no scripts
The fields are plain text fields: no format, keystroke or validation scripts, no buttons, no document scripts. An earlier version checked dates, emails and numbers with scripts; in Acrobat a rejected value is put back to the previous one, which looked like the field being erased. Without scripts nothing the client types is rejected or changed, and every reader (Acrobat, Chrome, Edge, Firefox, Preview, phones) shows the same thing. `NeedAppearances` is set so readers redraw typed text themselves. Format guidance is in the hint under each field.

Tested in Chromium's built-in viewer: all 18 fields filled with Tab, values stay visible after leaving each field and after scrolling between pages; a copy filled elsewhere renders its values in Poppler.

## Rebuild
```
pip install pymupdf pillow
python3 build.py
```
Assets: `assets/cover-bg.png`, `assets/cover-mockup.png` (from the reports cover template), `assets/elevatus-wordmark.svg`, Inter (`assets/fonts`, OFL).
