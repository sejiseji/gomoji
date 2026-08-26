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

## Layout

- `run.py`: local development entry point
- `src/gomoji/app.py`: Pyxel app loop
- `src/gomoji/config.py`: screen, timing, and palette constants
- `tests/`: low-risk tests for scaffold behavior
