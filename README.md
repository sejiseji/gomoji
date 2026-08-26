# Gomoji

Gomoji is a Pyxel project for ごもじンゴ, a short fake-dictionary game built around five-character hiragana words.

## Run

```sh
python3 run.py
```

or, after installing the package:

```sh
python3 -m pip install -e ".[dev]"
gomoji
```

## Controls

- `Space`: switch placeholder word
- `D`: toggle debug overlay
- `Esc`: quit

Current placeholder screen:

- Japanese display with the bundled `assets/umplus_j12r.bdf` font
- Portrait layout tuned for an iPhone 16-sized `396x696` Pyxel screen
- Larger 5-character slots backed by the generated reviewed content data
- `Space` still cycles placeholder words; the smartphone input UI starts in GMG002

## Content

The editable source corpus lives in `content/source/pack_001.json` through `pack_020.json`.

Current content state:

- `source`: 1000 entries
- `reviewed`: 40 entries
- `draft`: 960 entries
- `approved`: 0 entries
- runtime generated data: 40 reviewed entries in `src/gomoji/generated/content_data.py`

Validate the full source corpus:

```sh
.venv/bin/python scripts/validate_content.py
```

Build the runtime reviewed dataset:

```sh
.venv/bin/python scripts/build_content.py --output src/gomoji/generated/content_data.py
```

Check that the generated dataset is current:

```sh
.venv/bin/python scripts/build_content.py --check --output src/gomoji/generated/content_data.py
```

For development-only 1000-entry builds:

```sh
.venv/bin/python scripts/build_content.py --include-drafts --output src/gomoji/generated/content_data.py
```

Do not treat the 960 `draft` entries as release-quality content. `scripts/validate_content.py --release` is expected to fail until all 1000 entries are `approved`.

The fixed `んご/ンゴ` suffix is prohibited outside the product title `ごもじンゴ`.

## Test

```sh
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

## GitHub Pages

The repository includes a Pyxel web entry point and a GitHub Actions workflow for Pages.

1. In GitHub, open `Settings` -> `Pages`.
2. Set `Build and deployment` -> `Source` to `GitHub Actions`.
3. Push to `main`, or run the `Deploy Pages` workflow manually.

The published URL will be:

```text
https://sejiseji.github.io/gomoji/
```

Local static preview:

```sh
python3 -m http.server 8000
```

Then open `http://127.0.0.1:8000/`.

## Layout

- `run.py`: local development entry point
- `index.html`: GitHub Pages entry point
- `web_bootstrap.py`: browser entry point for Pyxel
- `src/gomoji/app.py`: Pyxel app loop
- `src/gomoji/config.py`: screen, timing, and palette constants
- `src/gomoji/content.py`: runtime content access helpers
- `src/gomoji/generated/content_data.py`: generated reviewed runtime content
- `content/`: editable source corpus, schemas, fixtures, and audit reports
- `scripts/`: content validation, build, and audit scripts
- `tests/`: low-risk tests for scaffold behavior
