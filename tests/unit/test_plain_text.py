from unittest import TestCase
from unittest.mock import patch
from hoi4.plain import find_closing_brace, load_as_dict, parse_text, strip_down

class LoadAsDictTests(TestCase):

    @patch("builtins.open")
    @patch("hoi4.plain.strip_down")
    @patch("hoi4.plain.parse_text")
    def test_can_load_as_dict(self, mock_parse, mock_strip, mock_open):
        d = load_as_dict("/path/to/file")
        mock_open.assert_called_with("/path/to/file")
        mock_strip.assert_called_with(mock_open.return_value.__enter__.return_value.read.return_value)
        mock_parse.assert_called_with(mock_strip.return_value)
        self.assertIs(d, mock_parse.return_value)



class StripDownTests(TestCase):

    def test_can_strip_down(self):
        text = "hoi4\na = b\n    c  = d e={  f g h}"
        self.assertEqual(strip_down(text), "hoi4 a = b c = d e={ f g h}")



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
        self.assertEqual(parse_text(text), ["xyz", "value1", "value 2"])