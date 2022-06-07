from unittest import TestCase
from unittest.mock import patch
from hoi4.parse import load_as_text, load_as_dict

class LoadAsTextTests(TestCase):

    @patch("builtins.open")
    @patch("hoi4.parse.parse_binary_hoi4")
    def test_can_load_binary_file(self, mock_parse, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = b"HOI4bin"
        text = load_as_text("/path/to.hoi4")
        self.assertEqual(text, mock_parse.return_value)
        mock_open.assert_called_with("/path/to.hoi4", "rb")
        mock_parse.assert_called_with(mock_open.return_value.__enter__.return_value)
    

    @patch("builtins.open")
    def test_can_load_plain_text_file(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.side_effect = [
            b"HOI4txt", b"1234567"
        ]
        text = load_as_text("/path/to.hoi4")
        self.assertEqual(text, "1234567")
        mock_open.assert_called_with("/path/to.hoi4", "rb")



class LoadAsDictTests(TestCase):

    @patch("hoi4.parse.load_as_text")
    @patch("hoi4.parse.filestring_to_dict")
    def test_can_load_as_dict(self, mock_dict, mock_load):
        d = load_as_dict("/path/to.hoi4")
        self.assertEqual(d, mock_dict.return_value)
        mock_load.assert_called_with("/path/to.hoi4")
        mock_dict.assert_called_with(mock_load.return_value)