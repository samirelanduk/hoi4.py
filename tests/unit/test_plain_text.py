from unittest import TestCase
from unittest.mock import patch
from hoi4.plain import filestring_to_dict, find_closing_brace, parse_tokens, strip_down, tokenize

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



class EndBraceFindingTests(TestCase):

    def test_can_get_end_brace(self):
        tokens = "12345 { xyz } 67890".split()
        self.assertEqual(find_closing_brace(tokens, 1), 3)
    

    def test_can_get_nested_end_brace(self):
        tokens = "12345 { xyz { a = b c = d e = { 1234 5678 { } n }  12 } } 67890".split()
        self.assertEqual(find_closing_brace(tokens, 1), 21)
        self.assertEqual(find_closing_brace(tokens, 3), 20)
        self.assertEqual(find_closing_brace(tokens, 12), 18)
        self.assertEqual(find_closing_brace(tokens, 15), 16)
    

    def test_start_must_be_brace(self):
        tokens = "12345 { xyz } 67890".split()
        with self.assertRaises(AssertionError):
            find_closing_brace(tokens, 0)
        with self.assertRaises(AssertionError):
           find_closing_brace(tokens, 4)



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



class TokenParsingTests(TestCase):

    def test_can_parse_flat_structure(self):
        tokens = ["player", "=", "ENG", "ideology", "=", "dem", "X", "=", "Y"]
        self.assertEqual(parse_tokens(tokens), {
            "player": "ENG", "ideology": "dem", "X": "Y"
        })
    

    def test_can_parse_lists_of_values_structure(self):
        tokens = ["xyz", "value1", "value2"]
        self.assertEqual(parse_tokens(tokens), ["xyz", "value1", "value2"])


""" class TextParsingTests(TestCase):

    def test_can_parse_flat_structure(self):
        text = 'player = "ENG 1" ideology = democratic session = 658'
        self.assertEqual(parse_text(text), {
            "player": "ENG 1", "ideology": "democratic", "session": "658"
        }) """

'''








class TextParsingTests(TestCase):

    def test_can_parse_flat_structure(self):
        text = 'hoi4 player="ENG" ideology=democratic session=658'
        self.assertEqual(parse_text(text), {
            "player": "ENG", "ideology": "democratic", "session": "658"
        })
    

    @patch("hoi4.plain.find_closing_brace")
    def test_can_parse_text_with_braces_section(self, mock_find):
        text = 'hoi4 player="ENG" values={ 1=2 3=4 } session=658'
        mock_find.return_value = 35
        self.assertEqual(parse_text(text), {
            "player": "ENG", "values": {"1": "2", "3": "4"}, "session": "658"
        })
        mock_find.assert_called_with(text, 25)
    

    def test_can_parse_lists_of_values_structure(self):
        text = ' xyz value1 "value 2'
        self.assertEqual(parse_text(text), ["xyz", "value1", "value 2"])'''