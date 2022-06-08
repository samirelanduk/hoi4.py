"""Functions for parsing plain text .hoi4 files."""

import re

def filestring_to_dict(filestring):
    """Takes a plain text HOI4 filestring and creates a Python dictionary
    representation of it."""

    data = strip_down(filestring)
    tokens = tokenize(data)
    return parse_tokens(tokens)


def strip_down(text):
    """Removes line breaks, and reduces all consecutive spaces to a single
    space."""

    no_line_breaks = text.replace("\n", " ")
    padded_braces = no_line_breaks.replace("}", " } ").replace("{", " { ")
    padded_equals = padded_braces.replace("=", " = ")
    return " ".join(padded_equals.split()).strip()


def tokenize(text):
    """Takes a stripped-down plain-text HOI4 filestring and returns a list of
    tokens. Broadly, tokens are things separated by whitespace, but anything
    enclosed by double quotes is considered a single token."""

    strings = list(re.finditer(r'".*?"', text))
    tokens = []
    end = 0
    for string in strings:
        tokens += text[end:string.start()].strip().split()
        tokens.append(string[0][1:-1])
        end = string.end()
    tokens += text[end:].strip().split()
    return tokens


def find_closing_brace(tokens, start):
    """Given a list of tokens and the location of an opening '{' within it, this
    function will return the position of the corresponding closing '}'."""

    assert tokens[start] == "{"
    level = 1
    for index, token in enumerate(tokens[start + 1:]):
        if token == "{": level += 1
        if token == "}": level -= 1
        if level == 0:
            return start + index + 1
    raise ValueError("Brace section never ended")


def parse_tokens(tokens):
    """Takes a list of tokens representing all or part of a HOI4 save file, and
    turns it into a Python dictionary. When it encounters sections enclosed by
    curly braces, it will call itself recursively on that section. If the tokens
    represents an array of values rather than a mapping, it will return a list
    instead."""

    if "=" not in tokens: return tokens
    key, d, loc =  "", {}, 0
    while loc < len(tokens):
        token = tokens[loc]
        if token == "{":
            end = find_closing_brace(tokens, loc)
            brace_section = tokens[loc + 1:end]
            d[key] = parse_tokens(brace_section)
            loc, key = end, ""
        elif token != "=" and key:
            d[key] = token
            key = ""
        elif token != "=":
            key = token
        loc += 1
    return d