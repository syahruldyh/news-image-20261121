#!/usr/bin/env python3
"""Render build/page.html to ../entry.png at exactly 1024x1024.

Loads the page in headless Chromium at deviceScaleFactor=2 (so text and
art are supersampled), then downscales the shot to 1024x1024 with PIL
Lanczos for crisp edges.
"""
import io
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "page.html"
OUT = HERE.parent / "entry.png"


def main() -> int:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1024, "height": 1024},
                                device_scale_factor=2)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(700)
        height = page.evaluate("document.documentElement.scrollHeight")
        print(f"document scrollHeight: {height}")
        shot = page.screenshot(type="png")
        browser.close()

    img = Image.open(io.BytesIO(shot))
    print(f"screenshot size: {img.size}")
    img = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    # The page uses a limited print palette; quantizing to 256 colours with
    # dithering keeps text crisp and cuts the file to a quarter of the size.
    img = img.quantize(colors=256, method=Image.MEDIANCUT,
                       dither=Image.FLOYDSTEINBERG)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} size={img.size} bytes={OUT.stat().st_size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
