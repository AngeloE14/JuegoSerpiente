#!/usr/bin/env python
import os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets" / "images"

def strip_png_iccp(path: Path) -> bool:
    try:
        with Image.open(path) as im:
            # Ensure RGBA to preserve transparency
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA")
            # Re-save without ICC profile and ancillary chunks
            tmp = path.with_suffix(".tmp.png")
            # Explicitly drop ICC profile to avoid libpng iCCP warning
            im.save(tmp, format="PNG", optimize=True, icc_profile=None)
            os.replace(tmp, path)
            return True
    except Exception:
        return False

def main():
    if not ASSETS_DIR.exists():
        print(f"No assets found at {ASSETS_DIR}")
        return
    changed = 0
    total = 0
    for p in ASSETS_DIR.rglob("*.png"):
        total += 1
        if strip_png_iccp(p):
            changed += 1
            print(f"✓ Stripped iCCP/sRGB from: {p.relative_to(ROOT)}")
        else:
            print(f"✗ Skipped (error): {p.relative_to(ROOT)}")
    print(f"Done. Processed {total} PNG(s), updated {changed}.")

if __name__ == "__main__":
    main()
