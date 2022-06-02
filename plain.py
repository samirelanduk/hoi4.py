def strip_down(text):
    return  " ".join(text.replace("\n", " ").split()).strip()


def find_closing_brace(text, start):
    assert text[start] == "{"
    level = 1
    for index, char in enumerate(text[start + 1:]):
        if char == "{": level += 1
        if char == "}": level -= 1
        if level == 0:
            return start + index
    raise Exception("Brace section never ended")

def parse_text(text):
    loc = 0
    word = ""
    key = ""
    in_string = False
    d = {}
    while loc < len(text):
        char = text[loc]
        #print("Character is", char)

        if char == '"':
            in_string = not in_string

        elif char == "=" and not in_string:
            key = word
            word = ""


        elif char == " " and not in_string:
            if key: d[key] = word
            word = ""

        elif char == "{":
            end = find_closing_brace(text, loc)
            brace_section = text[loc + 1:end - 1]
            d[key] = len(brace_section)
            loc = end
            key = ""
            word = ""

        else:
            word += char

        loc += 1
    return d



with open("autosave_plain.hoi4") as f:
    data = f.read()

data = strip_down(data)
d = parse_text(data)
print(d)

