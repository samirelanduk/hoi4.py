"""Tools for parsing loading data from files."""

from hoi4.binary import parse_binary_hoi4
from hoi4.plain import filestring_to_dict

def load_as_text(path):
    """Gets a plain-text filestring from a HOI4 save file, regardless of whether
    the file is a binary save file or a plain text save file. The first 7 bytes
    are omitted."""

    with open(path, "rb") as f:
        if f.read(7) == b"HOI4bin":
            return parse_binary_hoi4(f)
        else:
            return f.read().decode("utf-8")


def load_as_dict(path):
    """Gets a Python dictionary representation of a HOI4 save file, regardless
    of whether the file is a binary save file or a plain text save file."""
    
    filestring = load_as_text(path)
    return filestring_to_dict(filestring)