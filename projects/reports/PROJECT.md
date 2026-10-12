# Reports and documents (rebrands)

**What it is:** third-party reports rebuilt in the Elevatus identity, plus the tools to make any PDF report, Word document or Excel sheet in the identity.
**Status:**
- Leadership Style and DISC (from Testlify): FINAL, tag `reports-final-v2`.
- SMART Personality (from Testlify): first version 12 October 2026, `smart.py`. The source candidate was the vendor account, so a sample candidate (Sara Al-Haddad) replaces it.
- 360 Feedback report and presentation (from Central Test): first version sent 6 October 2026, waiting on the user (contact details for the last slide, photos, three product facts to confirm).

## Make a file
`cd projects/reports`, then `python3 disc.py` (or `leadership.py`, `smart.py`, `feedback360.py`, then `feedback360_deck.py`). PDFs land in `output/`. Needs Python with PyMuPDF, Pillow, openpyxl, python-docx.

## What is in this folder
- `lib.py`: the page engine and the cover template. `el_xlsx.py`, `el_docx.py`: Excel and Word. `check.py`: word-for-word comparison with a source PDF.
- `disc.py`, `leadership.py`, `feedback360.py` (+ `feedback360_data.json`), `feedback360_deck.py`: one script per document.
- `assets/`: cover background and mockup, wordmark PNGs, the rating-form picture.
- `output/`: the finished PDFs. `skill/`: a link to the skill below.

## Skill to load
`elevatus-documents` (lives in `.claude/skills/elevatus-documents`, linked here as `skill/`). It holds the two rules: a rebrand adds nothing to the source, and the cover is a template.

## Not in this folder
The source PDFs from the vendors (they were in `~/Downloads`). Copies of the finished files are also in `~/Downloads/Elevatus-Reports/`.

## Shared with the other projects (not copied into this folder)
- Identity: `brand/` (tokens, logos, `fonts/`, the brand book PDF). Brand rules: skill `elevatus-brand`.
- State and history of every project: `docs/backlog.md`.
