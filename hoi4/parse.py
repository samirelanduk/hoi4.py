from hoi4.binary import parse_binary_hoi4
from hoi4.plain import filestring_to_dict

def load_as_text(path):
    with open(path, "rb") as f:
        if f.read(7) == b"HOI4bin":
            return parse_binary_hoi4(f)
        else:
            return f.read().decode("utf-8")


def load_as_dict(path):
    filestring = load_as_text(path)
    return filestring_to_dict(filestring)