from pathlib import Path
import hoi4
from unittest import TestCase

class BinaryLoadingTests(TestCase):

    def test_can_load_binary_file_as_plain_text(self):
        text = hoi4.load_as_text(Path("tests/integration/files/Iraq.hoi4"))
        with open(Path("tests/integration/files/Iraq.ref.hoi4")) as f:
            self.assertEqual(text, f.read())