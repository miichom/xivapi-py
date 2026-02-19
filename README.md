# pyxivapi

[![PyPI - Version](https://img.shields.io/pypi/v/pyxivapi.svg)](https://pypi.org/project/pyxivapi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyxivapi.svg)](https://pypi.org/project/pyxivapi)

An asynchronous Python client library for working with [XIVAPI v2](https://v2.xivapi.com/), providing access to Final Fantasy XIV game data. It lets you fetch, search, and work with FFXIV data using a clean, modern Python interface.

If you need help or run into any issues, please [open an issue](https://github.com/xivapi/xivapi-py/issues) on GitHub or join the [XIVAPI Discord server](https://discord.gg/MFFVHWC) for support.

## Installation

```bash
pip install pyxivapi
```

```py
from pyxivapi import XIVAPI

# Basic instance
xiv = XIVAPI()

# With options
xiv_custom = XIVAPI(
    version="7.0",   # specify game version
    language="ja",   # ja, en, de, fr
    verbose=True     # enable debug logging
)
```

## Basic Usage

```py
xiv.items.get(1)
print(item["fields"]["Name"]) # "Gil" (or equivalent in your language)
```

```py
params = { "query": 'Name~"gil"', "sheets": "Item" }
results = xiv.search(params)
print(results[0])
"""
Example output:
{
  "score": 1,
  "sheet": "Item",
  "row_id": 1,
  "fields": {
    "Icon": {
      "id": 65002,
      "path": "ui/icon/065000/065002.tex",
      "path_hr1": "ui/icon/065000/065002_hr1.tex"
    },
    "Name": "Gil",
    "Singular": "gil"
  }
}
"""
```

## Contributing

Contributions of any kind are welcome - bug fixes, improvements, new features, or documentation updates.

### Getting Started

```bash
git clone https://github.com/miichom/pyxivapi.git
cd pyxivapi
hatch env create dev
```

### Run the checks:

```bash
hatch run dev:lint
hatch run dev:types
hatch run dev:test
```

### Before Opening a PR

Please make sure:

- All tests pass (`hatch run dev:test`)
- Type checking passes (`hatch run dev:types`)
- Linting passes (`hatch run dev:lint`)
- Your changes are clearly described in the PR
- Any relevant issues are referenced

If you want to discuss an idea before implementing it, feel free to open an issue.

## License

`pyxivapi` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
