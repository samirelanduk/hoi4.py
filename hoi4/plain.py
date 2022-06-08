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
    """Given a block of text and the location of an opening '{' within it, this
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
    if "=" not in tokens: return tokens
    key = ""
    d = {}
    loc = 0
    while loc < len(tokens):
        token = tokens[loc]
        if token == "=":
            pass
        elif token == "{":
            end = find_closing_brace(tokens, loc)
            brace_section = tokens[loc + 1:end]
            d[key] = parse_tokens(brace_section)
            loc, key = end, ""
        else:
            if key:
                d[key] = token
                key = ""
            else:
                key = token
        loc += 1
    return d



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
            key = word.rstrip()
            word = ""
        elif char == " " and not in_string:
            '''if list_mode and word: l.append(word)
            if key and not list_mode: d[key] = word
            word = ""'''
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