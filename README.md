# mac_rep_town

This is a pixel map generator for creating custom .png images with pixel-accurate test patterns for LED walls and projection surfaces.


As of Jan 2022 the software is command line interface only and because it is python code, it requires python to be installed.

The program is writted in Python 3.9

There are four scripts:
1) TestPatternMakerX.py - this is the main script. Running this script allows you to enter the pixelspace and resolution information. This main script calls the 'raster_maker.py' script to generate the individual rasters.
2) raster_maker.py - meant to be called my the main script.
3) src/greyStepsPatternMaker_v3.py - creates a grey steps test pattern for identifying issues with limited vs full color space. Run `python src/greyStepsPatternMaker_v3.py 1920 1080` (or with no arguments to be prompted); add `--steps N` (a multiple of 4) to override the step count. Saves to `images/greyTestPattern_<w>x<h>.png`.
   - Web GUI: https://macswg.github.io/mac_test_patterner/ — a static, browser-only version (live preview + PNG download) served by GitHub Pages from `docs/index.html`. You can also open that file directly in a browser.
4) SgLedTestPattern_v9_1.py - this script is depreciated and will eventually be removed. The functionality is integrated into "TestPatternMakerX.py"

## Docker

The app can be run with Docker Compose. Generated images are saved to `./images/` on the host.

**First time setup (or after changing dependencies):**
```bash
docker compose build
```

**JSON-driven patterns** (reads from `JSON_test_pattern_configs/TestPatterConfig1.json`):
```bash
docker compose run json
```

**Google Sheets-driven patterns** (requires credentials file at `secret/credentials_python-int-2023-2e89fbfc8ab6.json`):
```bash
docker compose run gsheet
```
