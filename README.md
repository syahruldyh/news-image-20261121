# The World on One Page — Saturday 21 November 2026

A make.fun entry for **news-image-20261121**: one 1024×1024 image that sums
up the world's news of a single day, Saturday 21 November 2026.

The page is a classic broadsheet front page: a dated masthead, the day in
UTC and in numbers, three illustrated lead stories, eleven smaller cards,
a dotted world map with numbered markers, thirty further stories in
numbered columns, and a date-check box that names the older stories left
out on purpose. Every story carries a status tag (CONFIRMED, OFFICIALS or
REPORTED) and a source.

## Running it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, defaulting to `/output`. It runs offline
and writes the same bytes every time.

## How the page was made

The sources live in `build/`:

- `build/page.html` — the whole page: layout, stories, inline SVG art for
  the small cards, and the dotted world map drawn from a coarse ASCII
  land grid by a short script at the end of the file.
- `build/art/` — the three lead illustrations (flat editorial style),
  generated as images and cropped into the page as banners.
- `build/fonts/` — Playfair Display, Archivo and Source Serif, used for
  the masthead, labels and body text.
- `build/render.py` — renders the page with headless Chromium
  (Playwright) at 2× and downscales to exactly 1024×1024, then quantizes
  to a 256-colour palette so the final PNG stays small.

## Layout of this repository

- `main.ts` — the entrypoint described above.
- `entry.png` — the finished front page, 1024×1024.
- `build/` — page source, art, fonts and the render script.
- `LICENSE` — MIT.
