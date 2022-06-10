from unittest import TestCase
from unittest.mock import Mock, patch
from hoi4.binary import *

class BinaryParseTests(TestCase):

    @patch("hoi4.binary.get_token")
    @patch("hoi4.binary.decorate")
    def test_can_parse_binary_hoi4(self, mock_decorate, mock_get):
        mock_get.side_effect = ["x", "=", "y", None]
        mock_decorate.return_value = "decorated"
        filestring = parse_binary_hoi4("FILE")
        self.assertEqual(filestring, "decorated")
        mock_get.assert_called_with("FILE")
        self.assertEqual(mock_get.call_count, 4)
        mock_decorate.assert_called_with("x = y")



class TextGetTests(TestCase):

    def setUp(self):
        self.file = Mock()


    def test_can_get_none(self):
        self.file.read.return_value = b""
        self.assertIsNone(get_token(self.file))
        self.file.read.return_value = b"1"
        self.assertIsNone(get_token(self.file))
        self.file.read.assert_any_call(2)
    

    def test_can_get_int(self):
        self.file.read.side_effect = [bytes([12, 0]), bytes([20, 40, 80, 160])]
        self.assertEqual(get_token(self.file), "-1605359596")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(4)
    

    def test_can_get_float(self):
        self.file.read.side_effect = [bytes([13, 0]), bytes([0, 1, 2, 3])]
        self.assertEqual(get_token(self.file), "50462.976")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(4)
    

    def test_can_get_boolean_no(self):
        self.file.read.side_effect = [bytes([14, 0]), bytes([0])]
        self.assertEqual(get_token(self.file), "no")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(1)
    

    def test_can_get_boolean_other(self):
        self.file.read.side_effect = [
            bytes([14, 0]), bytes([2]), bytes([6, 0]), b"isopol"
        ]
        self.assertEqual(get_token(self.file), "isopol")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(1)
        self.file.read.assert_any_call(6)
    

    def test_can_get_string_in_quotes(self):
        self.file.read.side_effect = [
            bytes([15, 0]), bytes([6, 0]), b"isopol"
        ]
        self.assertEqual(get_token(self.file), '"isopol"')
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(6)
    

    def test_can_get_uint(self):
        self.file.read.side_effect = [bytes([20, 0]), bytes([20, 40, 80, 160])]
        self.assertEqual(get_token(self.file), "2689607700")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(4)
    

    def test_can_get_string_without_quotes(self):
        self.file.read.side_effect = [
            bytes([23, 0]), bytes([6, 0]), b"isopol"
        ]
        self.assertEqual(get_token(self.file), "isopol")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(6)
    

    def test_can_get_uint(self):
        self.file.read.side_effect = [bytes([103, 1]), bytes([1, 2, 5, 10, 20, 40, 80, 160])]
        self.assertEqual(get_token(self.file), "-6894966962971672063")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(8)
    

    def test_can_get_uint(self):
        self.file.read.side_effect = [bytes([156, 2]), bytes([1, 2, 5, 10, 20, 40, 80, 160])]
        self.assertEqual(get_token(self.file), "11551777110737879553")
        self.file.read.assert_any_call(2)
        self.file.read.assert_any_call(8)
    

    def test_can_get_token(self):
        self.file.read.side_effect = [bytes([100, 0])]
        self.assertEqual(get_token(self.file), "panelType")
        self.file.read.assert_any_call(2)
    

    def test_can_get_unknown_token(self):
        self.file.read.side_effect = [bytes([23, 23])]
        self.assertEqual(get_token(self.file), "UNKNOWN_TOKEN_5911")
        self.file.read.assert_any_call(2)



class DecorationTests(TestCase):

    @patch("hoi4.binary.create_date")
    def test_can_convert_dates(self, mock_date):
        mock_date.side_effect = ["d1", "d2"]
        filestring = "x = 1 date = 60000000 start_date = 70000000 date = 4 y = 1"
        self.assertEqual(
            decorate(filestring),
            'x = 1 date = "d2" start_date = "d1" date = 4 y = 1'
        )
        mock_date.assert_any_call("70000000")
        mock_date.assert_any_call("60000000")
        self.assertEqual(mock_date.call_count, 2)
    

    def test_can_remove_quote_marks(self):
        filestring = 'a = b "ABC" = 12 id = "19" m = n'
        self.assertEqual(
            decorate(filestring), "a = b ABC = 12 id = 19 m = n"
        )



class DateCreationTests(TestCase):

    def test_can_get_date(self):
        self.assertEqual(create_date("60759371"), "1936.1.1.12")
        self.assertEqual(create_date("60760176"), "1936.2.4.1")
        self.assertEqual(create_date("60760584"), "1936.2.21.1")
        self.assertEqual(create_date("60760678"), "1936.2.24.23")
        self.assertEqual(create_date("60760730"), "1936.2.27.3")
        self.assertEqual(create_date("60760762"), "1936.2.28.11")
        self.assertEqual(create_date("60760777"), "1936.3.1.2")
        self.assertEqual(create_date("60761016"), "1936.3.11.1")
        self.assertEqual(create_date("60762020"), "1936.4.21.21")
        self.assertEqual(create_date("60762338"), "1936.5.5.3")
        self.assertEqual(create_date("60769657"), "1937.3.6.2")
        self.assertEqual(create_date("60794400"), "1940.1.1.1")
        self.assertEqual(create_date("60846971"), "1946.1.1.12")