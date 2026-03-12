import unittest

# Relative import from the same package
from ._scan_char_const_src import _scan_char_const


class TestScanCharConst(unittest.TestCase):
    """Test cases for _scan_char_const function"""
    
    def test_simple_char_const(self):
        """Test scanning a simple character constant like 'a'"""
        source = "'a'"
        token, new_pos, new_column = _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'a'")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)
    
    def test_escape_sequence_newline(self):
        """Test scanning character constant with newline escape"""
        source = "'\\n'"
        token, new_pos, new_column = _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'\\n'")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)
    
    def test_escape_sequence_single_quote(self):
        """Test scanning character constant with escaped single quote"""
        source = "'\\''"
        token, new_pos, new_column = _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'\\''")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)
    
    def test_escape_sequence_backslash(self):
        """Test scanning character constant with escaped backslash"""
        source = "'\\\\'"
        token, new_pos, new_column = _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'\\\\'")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)
    
    def test_missing_opening_quote(self):
        """Test error when opening quote is missing"""
        source = "a'"
        with self.assertRaises(Exception) as context:
            _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertIn("expected opening quote", str(context.exception))
        self.assertIn("test.c:1:1", str(context.exception))
    
    def test_unterminated_char_const(self):
        """Test error when character constant is not terminated"""
        source = "'a"
        with self.assertRaises(Exception) as context:
            _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertIn("unterminated character constant", str(context.exception))
        self.assertIn("test.c:1:1", str(context.exception))
    
    def test_unterminated_escape_sequence(self):
        """Test error when escape sequence is not terminated"""
        source = "'\\"
        with self.assertRaises(Exception) as context:
            _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertIn("unterminated character constant", str(context.exception))
        self.assertIn("test.c:1:1", str(context.exception))
    
    def test_position_not_at_start(self):
        """Test scanning character constant at non-zero position"""
        source = "int x = 'a';"
        token, new_pos, new_column = _scan_char_const(source, 8, 1, 9, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'a'")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 9)
        self.assertEqual(new_pos, 11)
        self.assertEqual(new_column, 12)
    
    def test_different_line_and_column(self):
        """Test scanning with different starting line and column"""
        source = "'b'"
        token, new_pos, new_column = _scan_char_const(source, 0, 5, 10, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'b'")
        self.assertEqual(token["line"], 5)
        self.assertEqual(token["column"], 10)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 13)
    
    def test_all_valid_escapes(self):
        """Test all valid escape sequences"""
        valid_escapes = [
            ('\\n', 'n'),
            ('\\t', 't'),
            ('\\r', 'r'),
            ('\\\\', '\\'),
            ("\\'", "'"),
            ('\\"', '"'),
            ('\\0', '0'),
            ('\\a', 'a'),
            ('\\b', 'b'),
            ('\\v', 'v'),
            ('\\f', 'f'),
            ('\\?', '?'),
        ]
        
        for escape_str, escape_char in valid_escapes:
            source = f"'{escape_str}'"
            token, new_pos, new_column = _scan_char_const(source, 0, 1, 1, "test.c")
            
            self.assertEqual(token["type"], "CHAR_CONST", f"Failed for escape: {escape_str}")
            self.assertEqual(token["value"], source, f"Failed for escape: {escape_str}")
    
    def test_empty_source(self):
        """Test error when source is empty"""
        source = ""
        with self.assertRaises(Exception) as context:
            _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertIn("expected opening quote", str(context.exception))
    
    def test_position_beyond_source_length(self):
        """Test error when position is beyond source length"""
        source = "'a'"
        with self.assertRaises(Exception) as context:
            _scan_char_const(source, 10, 1, 1, "test.c")
        
        self.assertIn("expected opening quote", str(context.exception))
    
    def test_invalid_escape_still_accepted(self):
        """Test that invalid escape sequences are still accepted (per implementation)"""
        source = "'\\x'"  # \x is not in valid_escapes but still accepted
        token, new_pos, new_column = _scan_char_const(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "CHAR_CONST")
        self.assertEqual(token["value"], "'\\x'")
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)


if __name__ == "__main__":
    unittest.main()
