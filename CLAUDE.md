# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the scripts

There is no build step. Install dependencies once, then run scripts directly.

```bash
pip install -r requirements.txt

# JSON-driven (no credentials needed)
python TestPatternMakerJSON.py

# Google Sheets-driven (requires credentials file — see below)
python TestPatternFromGoogleSheet.py

# Interactive CLI (prompts for all values at runtime)
python src/TestPatternMakerX.py

# Full vs limited range grey steps pattern (prompts if width/height omitted)
python src/greyStepsPatternMaker_v3.py 1920 1080 [--steps 16]

# Grey steps web GUI: static page, no server — open docs/index.html in a browser
```

**Docker:**
```bash
docker compose run json       # JSON workflow
docker compose run gsheet     # Google Sheets workflow
```

All scripts save PNG output to `./images/`.

## Google Sheets credentials

`TestPatternFromGoogleSheet.py` requires a service account JSON file at:
```
secret/credentials_python-int-2023-2e89fbfc8ab6.json
```
This file is gitignored and must be provided manually.

## Architecture

The codebase has a layered design: entry-point scripts collect configuration, pass it to a `raster_maker` module, which returns a PIL `Image` that the entry point composites onto a canvas and saves.

### Entry points → raster_maker pairs

| Entry point | raster_maker module | Config source |
|---|---|---|
| `TestPatternMakerJSON.py` | `raster_maker_json.py` | `JSON_test_pattern_configs/TestPatterConfig1.json` |
| `TestPatternFromGoogleSheet.py` | `raster_maker_google.py` | Google Sheets (via `pygsheets`) |
| `src/TestPatternMakerX.py` | `src/raster_maker.py` | Interactive CLI prompts |

`raster_maker_json.py` and `raster_maker_google.py` are non-interactive variants of `src/raster_maker.py`. They expose a `make_raster(rasterDict)` function that accepts a dict of raster parameters instead of prompting the user. `src/raster_maker.py` is the interactive original and is called only by `src/TestPatternMakerX.py`.

### Core concepts

- **Pixelspace**: the full output canvas (e.g. 3840×2160). Defined once per output image.
- **Raster**: an LED panel grid placed within the pixelspace at an `(x offset, y offset)`. Multiple rasters can be composited onto a single pixelspace canvas.
- **Tile**: individual LED panel within a raster. Rasters are built by tiling two slightly different shades of the `background color` in a checkerboard pattern.
- **Festival pattern**: an alternate raster mode that renders a circle + X-lines overlay instead of a tile grid (used for simple color reference patterns with no panel outlines).
- **Half-tile**: a row of tiles at half height. The `half tile top` field in config controls placement — `0` = top, `99` = bottom, `1-98` = after that row number.

### JSON config structure

`JSON_test_pattern_configs/TestPatterConfig1.json` is a list of pixelspace entries. Each entry is a two-element list:
```json
[
  { "pixelspace": { "name": "...", "size": [width, height] } },
  {
    "raster1": { "x offset": 0, "y offset": 0, "tile width": 48, "tile height": 48,
                 "panels wide": 10, "panels high": 8, "half tile top": "n",
                 "background color": "darkblue", "raster label": "...",
                 "festival pattern": false, "width": 480, "height": 384 },
    "raster2": { ... }
  }
]
```

### Google Sheets config structure

The sheet named in `TestPatternFromGoogleSheet.py` (`g_sht_name`) must have two worksheets:
- `rasters` — one row per raster, columns match the raster dict keys (`ps label`, `tile width`, `tile height`, `panels wide`, `panels high`, `x offset`, `y offset`, `background color`, `raster label`, `festival pattern`, `half tile top`, `ps width`, `ps height`)
- `pixelspaces` — one row per pixelspace with a `ps label` column used to group rasters

### Font resolution

Fonts are resolved at runtime based on `sys.platform`:
- macOS → `Arial.ttf`
- Windows → `arial.ttf`
- Linux → `Ubuntu-B.ttf` (only in `src/raster_maker.py`)

`fontsFolder` is set to the string `'FONT_FOLDER'` as a placeholder — on macOS this resolves correctly because PIL searches system font paths. On other platforms the font folder path may need updating.

### Grey steps web GUI

`docs/index.html` is a self-contained JavaScript port of `src/greyStepsPatternMaker_v3.py` (canvas rendering, no server) intended for GitHub Pages. The bar values and bar edges must stay identical to the Python version — the JS uses a `pyRound` helper to mimic Python's round-half-to-even. Update both when changing the pattern.

## Known issues / TODOs in the code

- `# TODO: There is a bug here on the vertical offset that needs work.` — present in all three `raster_maker` variants at the top of the main raster-drawing function.
- `# TODO: Deduplicate some of this code` — the panel-drawing loop is largely copy-pasted across the three raster_maker files.
- `SgLedTestPattern_v9_1.py` is deprecated and will eventually be removed.
