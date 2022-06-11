# hoi4.py

[![](https://github.com/samirelanduk/hoi4.py/actions/workflows/main.yml/badge.svg)](https://github.com/samirelanduk/hoi4.py/actions/workflows/main.yml)
[![](https://img.shields.io/pypi/pyversions/hoi4.py.svg?color=3776AB&logo=python&logoColor=white)](https://pypi.org/project/hoi4.py/0.1.0/)
[![](https://img.shields.io/pypi/l/hoi4.py.svg?color=blue)](https://github.com/samirelanduk/hoi4.py/blob/master/LICENSE)

hoi4.py is a Python library for parsing HOI4 save files (whether binary or
plain text) and for plotting useful information from them.

## Installing

hoi4.py is available through PyPI:

```bash
pip install hoi4
```

## Overview

### Command Line

To convert a binary save file to plain text save file:

```bash
python -m hoi4 binary2plain -i my_save_file.hoi4 -o my_converted_save_file.hoi4
```

To convert any save file (binary or plain text) to a JSON representation:

```bash
python -m hoi4 hoi42json -i my_save_file.hoi4 -o my_save_file.json
```

### Within Python

You can import the hoi4.py library into your own Python scripts and programs:

```python
import hoi4
text = hoi4.load_as_text("my_save_file.hoi4")
dictionary = hoi4.load_as_dict("my_save_file.hoi4")
```

## Changelog

### 0.1

*11th June, 2022*

- Initial parsing of binary save files.
- Initial parsing of plain text save files.
- Basic command line interface.