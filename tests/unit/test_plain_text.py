from unittest import TestCase

from plain import find_closing_brace

class EndBraceFindingTests(TestCase):

    def test_can_get_end_brace(self):
        text = "12345 { xyz } 67890"
        self.assertEqual(find_closing_brace(text, 6), 12)
    

    def test_can_get_nested_end_brace(self):
        text = "12345 { xyz { a=b c=d e={1234 5678 {} n}  12}} 67890"
        self.assertEqual(find_closing_brace(text, 6), 45)
    

    def test_start_must_be_brace(self):
        text = "12345 { xyz } 67890"
        with self.assertRaises(AssertionError):
            find_closing_brace(text, 5)
        with self.assertRaises(AssertionError):
           find_closing_brace(text, 11)