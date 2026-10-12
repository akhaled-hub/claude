# Word-for-word comparison of a rebranded report against its source PDF.
# Usage: python3 check.py source.pdf new.pdf [--cover]   (--cover skips page 1 of the new file)
# Expect: only the old brand name missing, only "Elevatus" (and chart labels that were images in the source) extra.
import sys, re
from collections import Counter
import pymupdf as fitz

def words(path, skip=0):
    doc = fitz.open(path)
    t = ' '.join(p.get_text() for i, p in enumerate(doc) if i >= skip)
    t = t.replace('', ' ').replace('•', ' ').replace('·', ' ')
    return Counter(re.findall(r"[A-Za-z0-9%'’.\-:]+", t)), len(doc)

src, new = sys.argv[1], sys.argv[2]
a, na = words(src); b, nb = words(new, 1 if '--cover' in sys.argv else 0)
print(f'source: {na} pages · new: {nb} pages')
print('missing from new:', dict(a - b) or 'nothing')
print('extra in new:   ', dict(b - a) or 'nothing')
