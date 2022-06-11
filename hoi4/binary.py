import re
from datetime import datetime, timedelta
from struct import unpack
from hoi4.data import TOKENS

def parse_binary_hoi4(f):
    """Takes an open file handler of a binary HOI4 (with the first 7 bytes
    already read) and returns a plain text representation of the contents in
    HOI4 format."""

    sections = []
    while True:
        text = get_token(f)
        if text is None: break
        sections.append(text)
    raw_filestring = " ".join(sections)
    return decorate(raw_filestring)


def get_token(f):
    """Gets a single token as a string from a binary file. It will read the
    first two bytes to determine what the current token type is, and then any
    additional tokens required to fully parse the token."""

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
    """Takes the algorithmically generated plain text HOI4 filestring and
    enhances it by creating string representations of dates and removing some
    unneeded quote marks."""

    for key in ["date", "expire", "trade", "next_weather_change"]:
        substitutions = []
        for m in re.finditer(f"([^\\s]*{key}[^\\s]*) = (\\d+)", filestring):
            if int(m[2]) < 43808760: continue
            date = f'"{create_date(m[2])}"'
            substitutions.append([m.start() + len(m[1]) + 3, m.end(), date])
        sections = []
        end = 0
        while substitutions:
            sub = substitutions.pop(0)
            sections.append(filestring[end:sub[0]])
            sections.append(sub[2])
            end = sub[1]
        sections.append(filestring[end:])
        filestring = "".join(sections)
    filestring = re.sub('"([a-zA-Z0-9_^]+)" =', r"\1 =", filestring)
    filestring = re.sub(' id = "(.+?)"', r" id = \1", filestring)
    return filestring


def create_date(hours):
    """Takes a HOI4 integer representation of a date and returns a HOI4 string
    representation of a date. Leap years are handled by ignoring them, as HOI4
    does."""

    delta = int(hours) - 60759371
    years = delta // (24 * 365)
    extra_hours = delta % (24 * 365)
    temp_dt = datetime(2002, 1, 1, 12, 0, 0) + timedelta(hours=extra_hours)
    dt = datetime(
        1936 + years + (temp_dt.year - 2002),
        temp_dt.month, temp_dt.day, temp_dt.hour
    )
    delta = timedelta(hours=int(hours) - 60759371)
    datestring = datetime.strftime(dt, "%Y.%-m.%-d.%-H")
    while datestring[0] == "0": datestring = datestring[1:]
    return datestring