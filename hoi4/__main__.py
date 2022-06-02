import os
import json
import argparse
from hoi4.plain import strip_down, parse_text

parser = argparse.ArgumentParser(description="Parse HoI4 save files.")

parser.add_argument("input", help="The file to process")

args = parser.parse_args()

with open(args.input) as f:
    data = f.read()
data = strip_down(data)
d = parse_text(data)
filename = os.path.basename(args.input)
if filename.endswith(".hoi4"): filename = filename[:-4]
filename += "json"
with open(filename, "w") as f:
    json.dump(d, f, indent=4)