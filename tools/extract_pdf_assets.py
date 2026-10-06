"""Merge pdfimages output (image + soft mask) into web-ready photos and transparent client logos."""
import sys
from pathlib import Path
from PIL import Image

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
jobs = {
    "a01f7e1c-Frame_33": ("pdo", "photo-pdo"),
    "260bda9c-Frame_34": ("omantel-academy", "photo-omantel"),
    "870db704-Frame_35": ("mep", "photo-mep"),
}
for stem, (logo, photo) in jobs.items():
    Image.open(src / f"{stem}-000.png").convert("RGB").save(dst / "img" / f"{photo}.jpg", quality=90)
    rgb = Image.open(src / f"{stem}-002.png").convert("RGB")
    mask = Image.open(src / f"{stem}-003.png").convert("L").resize(rgb.size)
    rgb.putalpha(mask)
    rgb = rgb.crop(rgb.getbbox())
    rgb.save(dst / "clients" / f"{logo}.png")
    print(logo, rgb.size)
