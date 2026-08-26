# Gomoji

Gomoji is a Pyxel project scaffold. The detailed game specification is intentionally left open so the project can absorb the next design pass without restructuring.

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

- `Space`: switch placeholder motif
- `D`: toggle debug overlay
- `Esc`: quit

## Test

```sh
PYTHONPATH=src python3 -m unittest discover -s tests
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
- `tests/`: low-risk tests for scaffold behavior
