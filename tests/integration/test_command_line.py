from pathlib import Path
from unittest import TestCase
import subprocess
import os

class Hoi42JsonTests(TestCase):

    def setUp(self):
        self.files_at_start = os.listdir(Path("tests/integration/files"))


    def tearDown(self):
        for f in os.listdir(Path("tests/integration/files")):
            if f not in self.files_at_start:
                os.remove(Path(f"tests/integration/files/{f}"))
    

    def test_can_convert_binary_hoi4_to_json(self):
        path = Path("tests/integration/files/Iraq.hoi4")
        out = Path("tests/integration/files/Iraq_out.hoi4")
        ref = Path("tests/integration/files/Iraq.ref.json")
        returncode = subprocess.call(f"python -m hoi4 hoi42json -i {path} -o {out}", shell=True)
        self.assertEqual(returncode, 0)
        with open(out) as f1:
            with open(ref) as f2:
                self.assertEqual(f1.read(), f2.read())


    def test_can_convert_plain_hoi4_to_json(self):
        path = Path("tests/integration/files/Iraq_plain.hoi4")
        out = Path("tests/integration/files/Iraq_plain_out.hoi4")
        ref = Path("tests/integration/files/Iraq_plain.ref.json")
        returncode = subprocess.call(f"python -m hoi4 hoi42json -i {path} -o {out}", shell=True)
        self.assertEqual(returncode, 0)
        with open(out) as f1:
            with open(ref) as f2:
                self.assertEqual(f1.read(), f2.read())