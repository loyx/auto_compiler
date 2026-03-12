import unittest

from ._scan_number_src import _scan_number


class TestScanNumber(unittest.TestCase):
    """Test cases for _scan_number function."""
    
    def test_single_digit(self):
        """Test scanning a single digit."""
        source = "5"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "5")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)
    
    def test_multiple_digits(self):
        """Test scanning multiple digits."""
        source = "123"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "123")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)
    
    def test_number_in_middle_of_source(self):
        """Test scanning a number in the middle of source."""
        source = "abc123def"
        token, new_pos, new_column = _scan_number(source, 3, 1, 4, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "123")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 4)
        self.assertEqual(new_pos, 6)
        self.assertEqual(new_column, 7)
    
    def test_number_at_end_of_source(self):
        """Test scanning a number at the end of source."""
        source = "abc123"
        token, new_pos, new_column = _scan_number(source, 3, 1, 4, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "123")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 4)
        self.assertEqual(new_pos, 6)
        self.assertEqual(new_column, 7)
    
    def test_number_followed_by_non_digit(self):
        """Test scanning a number followed by a non-digit character."""
        source = "123abc"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "123")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)
    
    def test_zero(self):
        """Test scanning zero."""
        source = "0"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "0")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)
    
    def test_leading_zeros(self):
        """Test scanning a number with leading zeros."""
        source = "007"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "007")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)
    
    def test_large_number(self):
        """Test scanning a large number."""
        source = "9999999999"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "9999999999")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 10)
        self.assertEqual(new_column, 11)
    
    def test_different_line_number(self):
        """Test scanning with different line number."""
        source = "42"
        token, new_pos, new_column = _scan_number(source, 0, 5, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "42")
        self.assertEqual(token["line"], 5)
        self.assertEqual(token["column"], 1)
    
    def test_different_column_number(self):
        """Test scanning with different column number."""
        source = "42"
        token, new_pos, new_column = _scan_number(source, 0, 1, 10, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "42")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 10)
        self.assertEqual(new_column, 12)
    
    def test_pos_at_end_of_source(self):
        """Test when pos is at the end of source (no digits to scan)."""
        source = "abc"
        token, new_pos, new_column = _scan_number(source, 3, 1, 4, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 4)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)
    
    def test_pos_beyond_source(self):
        """Test when pos is beyond the source length."""
        source = "abc"
        token, new_pos, new_column = _scan_number(source, 10, 1, 4, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 4)
        self.assertEqual(new_pos, 10)
        self.assertEqual(new_column, 4)
    
    def test_pos_at_non_digit(self):
        """Test when pos points to a non-digit character."""
        source = "abc123"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 0)
        self.assertEqual(new_column, 1)
    
    def test_filename_in_token(self):
        """Test that filename is used for error reporting (not stored in token)."""
        source = "123"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "main.c")
        
        self.assertNotIn("filename", token)
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "123")
    
    def test_mixed_digits_and_letters(self):
        """Test that scanning stops at first non-digit."""
        source = "123abc456"
        token, new_pos, new_column = _scan_number(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["value"], "123")
        self.assertEqual(new_pos, 3)
    
    def test_digit_after_space(self):
        """Test scanning number after space (starting at digit)."""
        source = " 123"
        token, new_pos, new_column = _scan_number(source, 1, 1, 2, "test.c")
        
        self.assertEqual(token["type"], "INT_CONST")
        self.assertEqual(token["value"], "123")
        self.assertEqual(token["column"], 2)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)


if __name__ == "__main__":
    unittest.main()
