import re
from datetime import datetime, timedelta
from struct import unpack
from hoi4.data import TOKENS

def parse_binary_hoi4(f):
    depth = 0
    sections = []
    while True:
        text = get_text(f)
        if text is None: break
        if text == 1:
            depth += 1
            sections.append("{\n" + depth * "  ")
        elif text == -1:
            depth -= 1
            sections.append("\n" + depth * "  " + "}\n" + depth * "  ")
        else:
            sections.append(text)
    raw_filestring = " ".join(sections)
    return decorate(raw_filestring)


def get_text(f):
    bytes2 = f.read(2)
    if len(bytes2) != 2: return None
    number = unpack("<H", bytes2)[0]
    if number == 12:
        text = str(unpack("<i", f.read(4))[0])
    elif number == 13:
        text = f"{unpack('<i', f.read(4))[0] / 1000:.3f}"
    elif number == 14:
        bytes1 = unpack("B", f.read(1))[0]
        if bytes1 in [0, 1]:
            text = ["no", "yes"][bytes1]
        else:
            length = unpack("<H", f.read(2))[0]
            text = f.read(length).decode("utf-8")
    elif number == 15:
        length = unpack("<H", f.read(2))[0]
        text = f'"{f.read(length).decode("utf-8")}"'
    elif number == 20:
        text = str(unpack("<I", f.read(4))[0])
    elif number == 23:
        length = unpack("<H", f.read(2))[0]
        text = f.read(length).decode("utf-8")
    elif number == 359:
        text = str(unpack("<q", f.read(8))[0])
    elif number == 668:
        text = str(unpack("<Q", f.read(8))[0])
    else:
        text = TOKENS.get(number, f"UNKNOWN_TOKEN_{number}")
    return text


def decorate(filestring):
    for key in ["start_date", "date"]:
        substitutions = []
        for m in re.finditer(f"{key} = (\\d+)", filestring):
            if int(m[1]) < 60000000: continue
            date = f'"{create_date(m[1])}"'
            substitutions.append([m.start() + len(key) + 3, m.end(), date])
        sections = []
        end = 0
        while substitutions:
            sub = substitutions.pop(0)
            sections.append(filestring[end:sub[0]])
            sections.append(sub[2])
            end = sub[1]
        filestring = "".join(sections)

    filestring = re.sub('"([a-zA-Z0-9_^]+)" =', r"\1 =", filestring)
    filestring = re.sub(' id = "(.+?)"', r" id = \1", filestring)
    return filestring


def create_date(hours):
    delta = int(hours) - 60759371
    years = delta // (24 * 365)
    extra_hours = delta % (24 * 365)
    temp_dt = datetime(2002, 1, 1, 12, 0, 0) + timedelta(hours=extra_hours)
    dt = datetime(
        1936 + years + (temp_dt.year - 2002),
        temp_dt.month, temp_dt.day, temp_dt.hour
    )
    delta = timedelta(hours=int(hours) - 60759371)
    return datetime.strftime(dt, "%Y.%-m.%-d.%-H")