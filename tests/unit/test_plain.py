from unittest import TestCase
from unittest.mock import patch
from hoi4.plain import *

class FilestringToDictTests(TestCase):

    @patch("hoi4.plain.strip_down")
    @patch("hoi4.plain.tokenize")
    @patch("hoi4.plain.parse_tokens")
    def test_can_get_dict_from_filestring(self, mock_parse, mock_token, mock_strip):
        d = filestring_to_dict("xyz")
        self.assertEqual(d, mock_parse.return_value)
        mock_strip.assert_called_with("xyz")
        mock_token.assert_called_with(mock_strip.return_value)
        mock_parse.assert_called_with(mock_token.return_value)



class StripDownTests(TestCase):

    def test_can_strip_down(self):
        text = "hoi4\na = b\n    c  = d e={  f g h}   "
        self.assertEqual(
            strip_down(text), "hoi4 a = b c = d e = { f g h }"
        )



class TokenizeTests(TestCase):

    def test_can_tokenize_single_token(self):
        self.assertEqual(tokenize("token1"), ["token1"])
    

    def test_can_tokenize_multiple_tokens(self):
        self.assertEqual(
            tokenize("token1 token2 token3"), ["token1", "token2", "token3"]
        )
    

    def test_can_tokenize_with_braces(self):
        self.assertEqual(
            tokenize("ideology = democratic session = 658 val3 = { 1 = 2 }"), [
                "ideology", "=", "democratic", "session", "=", "658", "val3",
                "=", "{", "1", "=", "2", "}"
            ]
        )
    

    def test_can_tokenize_with_strings(self):
        self.assertEqual(
            tokenize('ideology = "democratic state" x = "" session = "658" val3 = { 1 = 2 }'), [
                "ideology", "=", "democratic state", "x", "=", "", "session", "=", "658", "val3",
                "=", "{", "1", "=", "2", "}"
            ]
        )



class EndBraceFindingTests(TestCase):

    def test_can_get_end_brace(self):
        tokens = ["12345", "{", "xyz", "}", "67890"]
        self.assertEqual(find_closing_brace(tokens, 1), 3)
    

    def test_can_get_nested_end_brace(self):
        tokens = [
            "12345", "{", "xyz", "{", "a", "=", "b", "c", "=", "d", "e", "=",
            "{", "1234", "5678", "{", "}", "n", "}", "12", "}", "}", "67890"
        ]
        self.assertEqual(find_closing_brace(tokens, 1), 21)
        self.assertEqual(find_closing_brace(tokens, 3), 20)
        self.assertEqual(find_closing_brace(tokens, 12), 18)
        self.assertEqual(find_closing_brace(tokens, 15), 16)
    

    def test_start_must_be_brace(self):
        tokens = ["12345", "{", "xyz", "}", "67890"]
        with self.assertRaises(AssertionError):
            find_closing_brace(tokens, 0)
        with self.assertRaises(AssertionError):
           find_closing_brace(tokens, 4)



class TokenParsingTests(TestCase):

    def test_can_parse_flat_structure(self):
        tokens = ["player", "=", "ENG", "ideology", "=", "dem", "X", "=", "Y"]
        self.assertEqual(parse_tokens(tokens), {
            "player": "ENG", "ideology": "dem", "X": "Y"
        })
    

    def test_can_parse_lists_of_values_structure(self):
        tokens = ["xyz", "value1", "value2"]
        self.assertEqual(parse_tokens(tokens), ["xyz", "value1", "value2"])
    

    @patch("hoi4.plain.find_closing_brace")
    def test_can_parse_lists_of_dicts_structure(self, mock_find):
        mock_find.return_value = 5
        tokens = ["xyz", "{", "x", "=", "y", "}", "abc"]
        self.assertEqual(parse_tokens(tokens), ["xyz", {"x": "y"}, "abc"])
        mock_find.assert_called_with(tokens, 1)
    

    @patch("hoi4.plain.find_closing_brace")
    def test_can_parse_text_with_braces_section(self, mock_find):
        tokens = 'player = ENG values = { 1 = 2 3 = 4 } session = 658'.split()
        mock_find.return_value = 12
        self.assertEqual(parse_tokens(tokens), {
            "player": "ENG", "values": {"1": "2", "3": "4"}, "session": "658"
        })
        mock_find.assert_called_with(tokens, 5)