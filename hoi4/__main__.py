import os
import json
import argparse
from hoi4.plain import load_as_dict

parser = argparse.ArgumentParser(description="Parse HoI4 save files.")

parser.add_argument("input", help="The file to process")

args = parser.parse_args()

d = load_as_dict(args.input)
filename = os.path.basename(args.input)
if filename.endswith(".hoi4"): filename = filename[:-4]
filename += "json"
with open(filename, "w") as f:
    json.dump(d, f, indent=4)