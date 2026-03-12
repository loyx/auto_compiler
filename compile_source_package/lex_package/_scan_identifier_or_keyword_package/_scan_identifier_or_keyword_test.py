"""
Unit tests for _scan_identifier_or_keyword function.
Tests scanning of C identifiers and keywords from source code.
"""
import unittest
from typing import Any, Dict

from ._scan_identifier_or_keyword_src import _scan_identifier_or_keyword

Token = Dict[str, Any]


class TestScanIdentifierOrKeyword(unittest.TestCase):
    """Test cases for _scan_identifier_or_keyword function."""

    def test_keyword_int(self):
        """Test scanning the 'int' keyword."""
        source = "int x;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_INT")
        self.assertEqual(token["value"], "int")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)

    def test_keyword_char(self):
        """Test scanning the 'char' keyword."""
        source = "char c;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_CHAR")
        self.assertEqual(token["value"], "char")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)

    def test_keyword_if(self):
        """Test scanning the 'if' keyword."""
        source = "if (x)"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_IF")
        self.assertEqual(token["value"], "if")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    def test_keyword_else(self):
        """Test scanning the 'else' keyword."""
        source = "else {}"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_ELSE")
        self.assertEqual(token["value"], "else")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)

    def test_keyword_while(self):
        """Test scanning the 'while' keyword."""
        source = "while (1)"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_WHILE")
        self.assertEqual(token["value"], "while")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 5)
        self.assertEqual(new_column, 6)

    def test_keyword_for(self):
        """Test scanning the 'for' keyword."""
        source = "for (;;)"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_FOR")
        self.assertEqual(token["value"], "for")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)

    def test_keyword_return(self):
        """Test scanning the 'return' keyword."""
        source = "return 0;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_RETURN")
        self.assertEqual(token["value"], "return")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 6)
        self.assertEqual(new_column, 7)

    def test_keyword_break(self):
        """Test scanning the 'break' keyword."""
        source = "break;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_BREAK")
        self.assertEqual(token["value"], "break")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 5)
        self.assertEqual(new_column, 6)

    def test_keyword_continue(self):
        """Test scanning the 'continue' keyword."""
        source = "continue;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "KEYWORD_CONTINUE")
        self.assertEqual(token["value"], "continue")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 8)
        self.assertEqual(new_column, 9)

    def test_simple_identifier(self):
        """Test scanning a simple identifier."""
        source = "variable"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "variable")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 8)
        self.assertEqual(new_column, 9)

    def test_identifier_with_underscore(self):
        """Test scanning identifier with underscores."""
        source = "_my_var_123"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "_my_var_123")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 11)
        self.assertEqual(new_column, 12)

    def test_identifier_stops_at_non_alnum(self):
        """Test that scanning stops at non-identifier characters."""
        source = "count = 5"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "count")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 5)
        self.assertEqual(new_column, 6)

    def test_identifier_stops_at_space(self):
        """Test that scanning stops at whitespace."""
        source = "x y"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "x")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_identifier_stops_at_operator(self):
        """Test that scanning stops at operators."""
        source = "result+a"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "result")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 6)
        self.assertEqual(new_column, 7)

    def test_identifier_stops_at_semicolon(self):
        """Test that scanning stops at semicolon."""
        source = "done;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "done")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)

    def test_mid_source_position(self):
        """Test scanning from a middle position in source."""
        source = "int x = 5;"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 4, 1, 5, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "x")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 5)
        self.assertEqual(new_pos, 5)
        self.assertEqual(new_column, 6)

    def test_custom_line_column(self):
        """Test with custom line and column numbers."""
        source = "func"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 10, 25, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "func")
        self.assertEqual(token["line"], 10)
        self.assertEqual(token["column"], 25)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 29)

    def test_single_char_identifier(self):
        """Test scanning single character identifier."""
        source = "i"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "i")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_single_char_keyword(self):
        """Test that single char that's not a keyword is identifier."""
        # Note: C has no single-letter keywords in our set
        source = "a"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "a")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_pos_at_end_of_source(self):
        """Test when pos is at the end of source (empty scan)."""
        source = "test"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 4, 1, 5, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 5)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)

    def test_pos_beyond_source_length(self):
        """Test when pos is beyond source length."""
        source = "test"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 10, 1, 5, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 5)
        self.assertEqual(new_pos, 10)
        self.assertEqual(new_column, 5)

    def test_empty_source(self):
        """Test with empty source string."""
        source = ""
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 0)
        self.assertEqual(new_column, 1)

    def test_identifier_with_leading_underscore(self):
        """Test identifier starting with underscore."""
        source = "_private"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "_private")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 8)
        self.assertEqual(new_column, 9)

    def test_identifier_all_underscores(self):
        """Test identifier with only underscores."""
        source = "___"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "___")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)

    def test_identifier_with_digits(self):
        """Test identifier containing digits (not at start)."""
        source = "var123test"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "var123test")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 10)
        self.assertEqual(new_column, 11)

    def test_keyword_case_sensitive(self):
        """Test that keywords are case-sensitive."""
        source = "INT"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        # INT is not a keyword (only lowercase 'int' is)
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "INT")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)

    def test_mixed_case_identifier(self):
        """Test mixed case identifier."""
        source = "MyVariable"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "MyVariable")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(new_pos, 10)
        self.assertEqual(new_column, 11)

    def test_filename_preserved_in_token(self):
        """Test that filename parameter is available (though not stored in token)."""
        source = "test"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "myfile.c")
        
        # Filename is not stored in token per implementation
        self.assertNotIn("filename", token)
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "test")

    def test_consecutive_scanning(self):
        """Test scanning multiple identifiers consecutively."""
        source = "int x"
        
        # Scan 'int'
        token1, pos1, col1 = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        self.assertEqual(token1["type"], "KEYWORD_INT")
        self.assertEqual(token1["value"], "int")
        self.assertEqual(pos1, 3)
        self.assertEqual(col1, 4)
        
        # Skip space and scan 'x'
        token2, pos2, col2 = _scan_identifier_or_keyword(source, pos1 + 1, 1, col1 + 1, "test.c")
        self.assertEqual(token2["type"], "IDENTIFIER")
        self.assertEqual(token2["value"], "x")
        self.assertEqual(pos2, 5)
        self.assertEqual(col2, 6)


class TestScanIdentifierOrKeywordEdgeCases(unittest.TestCase):
    """Edge case tests for _scan_identifier_or_keyword."""

    def test_underscore_only_identifier(self):
        """Test single underscore as identifier."""
        source = "_"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "_")
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_long_identifier(self):
        """Test very long identifier."""
        source = "a" * 1000
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(len(token["value"]), 1000)
        self.assertEqual(new_pos, 1000)
        self.assertEqual(new_column, 1001)

    def test_keyword_followed_by_identifier_chars(self):
        """Test that 'int' followed by more chars becomes identifier."""
        source = "integer"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        # 'integer' is not a keyword, it's an identifier
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "integer")
        self.assertEqual(new_pos, 7)
        self.assertEqual(new_column, 8)

    def test_keyword_as_substring(self):
        """Test identifier containing keyword as substring."""
        source = "myintvar"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "myintvar")
        self.assertEqual(new_pos, 8)
        self.assertEqual(new_column, 9)

    def test_newline_stops_scan(self):
        """Test that newline character stops identifier scan."""
        source = "var\nnext"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "var")
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)

    def test_tab_stops_scan(self):
        """Test that tab character stops identifier scan."""
        source = "var\tnext"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "var")
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)

    def test_special_chars_stop_scan(self):
        """Test various special characters stop identifier scan."""
        special_chars = ["+", "-", "*", "/", "%", "&", "|", "^", "~", "!", "=", "<", ">", "?", ":", ".", ",", ";"]
        
        for ch in special_chars:
            with self.subTest(char=ch):
                source = f"var{ch}rest"
                token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
                
                self.assertEqual(token["type"], "IDENTIFIER")
                self.assertEqual(token["value"], "var")
                self.assertEqual(new_pos, 3)
                self.assertEqual(new_column, 4)

    def test_parenthesis_stops_scan(self):
        """Test that parenthesis stops identifier scan."""
        source = "func(args)"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "func")
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)

    def test_bracket_stops_scan(self):
        """Test that brackets stop identifier scan."""
        source = "arr[index]"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "arr")
        self.assertEqual(new_pos, 3)
        self.assertEqual(new_column, 4)

    def test_brace_stops_scan(self):
        """Test that braces stop identifier scan."""
        source = "block{}"
        token, new_pos, new_column = _scan_identifier_or_keyword(source, 0, 1, 1, "test.c")
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "block")
        self.assertEqual(new_pos, 5)
        self.assertEqual(new_column, 6)


if __name__ == "__main__":
    unittest.main()
