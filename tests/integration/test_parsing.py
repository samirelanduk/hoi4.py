import hoi4
import json
from pathlib import Path
from unittest import TestCase

class TextLoadingTests(TestCase):

    def test_can_load_binary_file_as_plain_text(self):
        text = hoi4.load_as_text(Path("tests/integration/files/Iraq.hoi4"))
        with open(Path("tests/integration/files/Iraq.ref.hoi4")) as f:
            self.assertEqual(text, f.read())
    

    def test_can_load_plain_file_as_plain_text(self):
        text = hoi4.load_as_text(Path("tests/integration/files/Iraq_plain.hoi4"))
        with open(Path("tests/integration/files/Iraq_plain.hoi4"), "rb") as f:
            self.assertEqual(text, f.read()[7:].decode("utf-8"))



class DictLoadingTests(TestCase):

    def test_can_load_plain_file_as_dict(self):
        text = hoi4.load_as_dict(Path("tests/integration/files/Iraq_plain.hoi4"))
        with open(Path("tests/integration/files/Iraq_plain.ref.json")) as f:
            self.assertEqual(text, json.load(f))