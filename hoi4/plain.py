"""Functions for parsing plain text .hoi4 files."""

def load_as_dict(path):
    """Opens a .hoi4 file and parses it as a Python dictionary."""

    with open(path) as f:
        data = f.read()
    data = strip_down(data)
    return parse_text(data)


def strip_down(text):
    """Removes line breaks, and reduces all consecutive spaces to a single
    space."""

    return  " ".join(text.replace("\n", " ").split()).strip()


def find_closing_brace(text, start):
    """Given a block of text and the location of an opening '{' within it, this
    function will return the position of the corresponding closing '}'."""

    assert text[start] == "{"
    level = 1
    for index, char in enumerate(text[start + 1:]):
        if char == "{": level += 1
        if char == "}": level -= 1
        if level == 0:
            return start + index + 1
    raise ValueError("Brace section never ended")


def parse_text(text):
    """Takes a block of text representing all or part of a HoI4 save file, and
    turns it into a Python dictionary. When it encounters sections enclosed by
    curly braces, it will call itself recursively on that section. If the text
    represents an array of values rather than a mapping, it will return a list
    instead."""

    loc, word, key, in_string, d, l = 0, "", "", False, {}, []
    list_mode = "=" not in text
    while loc < len(text):
        char = text[loc]
        if char == '"':
            in_string = not in_string
        elif char == "=" and not in_string:
            key = word
            word = ""
        elif char == " " and not in_string:
            if list_mode and word: l.append(word)
            if key and not list_mode: d[key] = word
            word = ""
        elif char == "{":
            end = find_closing_brace(text, loc)
            brace_section = text[loc + 1:end - 1]
            if not list_mode: d[key] = parse_text(brace_section)
            if list_mode: l.append(parse_text(brace_section))
            loc, key, word = end, "", ""
        else:
            word += char
        if loc == len(text) - 1 and (key or list_mode) and word:
            if list_mode: l.append(word)
            if not list_mode: d[key] = word
        loc += 1
    return l if list_mode else d