# -*- coding: utf-8 -*-
"""
Unit tests for _scan_operator_or_punctuation function.
Tests operator and punctuation scanning with maximal munch principle.
"""

import unittest
from typing import Any, Dict

from ._scan_operator_or_punctuation_src import _scan_operator_or_punctuation


class TestScanOperatorOrPunctuation(unittest.TestCase):
    """Test cases for _scan_operator_or_punctuation scanner."""

    def _assert_token(
        self,
        token: Dict[str, Any],
        expected_type: str,
        expected_value: str,
        expected_line: int,
        expected_column: int
    ) -> None:
        """Helper to assert token structure and content."""
        self.assertEqual(token["type"], expected_type)
        self.assertEqual(token["value"], expected_value)
        self.assertEqual(token["line"], expected_line)
        self.assertEqual(token["column"], expected_column)

    # ========== Multi-character operators (maximal munch) ==========

    def test_scan_eq_operator(self):
        """Test == operator scanning."""
        source = "=="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_EQ", "==", 1, 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    def test_scan_ne_operator(self):
        """Test != operator scanning."""
        source = "!="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_NE", "!=", 1, 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    def test_scan_le_operator(self):
        """Test <= operator scanning."""
        source = "<="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_LE", "<=", 1, 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    def test_scan_ge_operator(self):
        """Test >= operator scanning."""
        source = ">="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_GE", ">=", 1, 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    def test_scan_and_operator(self):
        """Test && operator scanning."""
        source = "&&"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_AND", "&&", 1, 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    def test_scan_or_operator(self):
        """Test || operator scanning."""
        source = "||"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_OR", "||", 1, 1)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 3)

    # ========== Single-character operators ==========

    def test_scan_plus_operator(self):
        """Test + operator scanning."""
        source = "+"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_PLUS", "+", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_minus_operator(self):
        """Test - operator scanning."""
        source = "-"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_MINUS", "-", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_mul_operator(self):
        """Test * operator scanning."""
        source = "*"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_MUL", "*", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_div_operator(self):
        """Test / operator scanning."""
        source = "/"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_DIV", "/", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_mod_operator(self):
        """Test % operator scanning."""
        source = "%"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_MOD", "%", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_assign_operator(self):
        """Test = operator scanning (single char, not ==)."""
        source = "= "
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_ASSIGN", "=", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_lt_operator(self):
        """Test < operator scanning (single char, not <=)."""
        source = "< "
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_LT", "<", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_gt_operator(self):
        """Test > operator scanning (single char, not >=)."""
        source = "> "
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_GT", ">", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_not_operator(self):
        """Test ! operator scanning (single char, not !=)."""
        source = "! "
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "OP_NOT", "!", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    # ========== Punctuation symbols ==========

    def test_scan_semicolon(self):
        """Test ; punctuation scanning."""
        source = ";"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "SEP_SEMICOLON", ";", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_comma(self):
        """Test , punctuation scanning."""
        source = ","
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "SEP_COMMA", ",", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_lparen(self):
        """Test ( punctuation scanning."""
        source = "("
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "SEP_LPAREN", "(", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_rparen(self):
        """Test ) punctuation scanning."""
        source = ")"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "SEP_RPAREN", ")", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_lbrace(self):
        """Test { punctuation scanning."""
        source = "{"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "SEP_LBRACE", "{", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    def test_scan_rbrace(self):
        """Test } punctuation scanning."""
        source = "}"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self._assert_token(token, "SEP_RBRACE", "}", 1, 1)
        self.assertEqual(new_pos, 1)
        self.assertEqual(new_column, 2)

    # ========== Position tracking tests ==========

    def test_scan_with_custom_line_column(self):
        """Test scanning with non-default line and column."""
        source = "=="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 5, 10, "test.c")
        self._assert_token(token, "OP_EQ", "==", 5, 10)
        self.assertEqual(new_pos, 2)
        self.assertEqual(new_column, 12)

    def test_scan_at_middle_position(self):
        """Test scanning operator at middle of source string."""
        source = "a == b"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 2, 1, 3, "test.c")
        self._assert_token(token, "OP_EQ", "==", 1, 3)
        self.assertEqual(new_pos, 4)
        self.assertEqual(new_column, 5)

    # ========== Error handling tests ==========

    def test_scan_at_eof_raises_error(self):
        """Test that scanning at EOF raises ValueError."""
        source = ""
        with self.assertRaises(ValueError) as context:
            _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("test.c:1:1", str(context.exception))

    def test_scan_beyond_eof_raises_error(self):
        """Test that scanning beyond EOF raises ValueError."""
        source = "+"
        with self.assertRaises(ValueError) as context:
            _scan_operator_or_punctuation(source, 5, 1, 1, "test.c")
        self.assertIn("Unexpected end of file", str(context.exception))

    def test_scan_invalid_character_raises_error(self):
        """Test that invalid character raises ValueError."""
        source = "@"
        with self.assertRaises(ValueError) as context:
            _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertIn("Unexpected character '@'", str(context.exception))
        self.assertIn("test.c:1:1", str(context.exception))

    def test_scan_invalid_character_with_custom_position(self):
        """Test invalid character error includes correct position info."""
        source = "#"
        with self.assertRaises(ValueError) as context:
            _scan_operator_or_punctuation(source, 0, 10, 25, "main.c")
        self.assertIn("Unexpected character '#'", str(context.exception))
        self.assertIn("main.c:10:25", str(context.exception))

    # ========== Maximal munch edge cases ==========

    def test_maximal_munch_eq_not_single_assign(self):
        """Test that == is preferred over = when both chars available."""
        source = "=="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertEqual(token["type"], "OP_EQ")
        self.assertEqual(token["value"], "==")

    def test_maximal_munch_ne_not_single_not(self):
        """Test that != is preferred over ! when both chars available."""
        source = "!="
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertEqual(token["type"], "OP_NE")
        self.assertEqual(token["value"], "!=")

    def test_single_assign_when_next_char_not_eq(self):
        """Test single = when next char doesn't form ==."""
        source = "=x"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertEqual(token["type"], "OP_ASSIGN")
        self.assertEqual(token["value"], "=")
        self.assertEqual(new_pos, 1)

    def test_single_lt_when_next_char_not_eq(self):
        """Test single < when next char doesn't form <=."""
        source = "<x"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertEqual(token["type"], "OP_LT")
        self.assertEqual(token["value"], "<")
        self.assertEqual(new_pos, 1)

    def test_single_gt_when_next_char_not_eq(self):
        """Test single > when next char doesn't form >=."""
        source = ">x"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertEqual(token["type"], "OP_GT")
        self.assertEqual(token["value"], ">")
        self.assertEqual(new_pos, 1)

    def test_single_not_when_next_char_not_eq(self):
        """Test single ! when next char doesn't form !=."""
        source = "!x"
        token, new_pos, new_column = _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertEqual(token["type"], "OP_NOT")
        self.assertEqual(token["value"], "!")
        self.assertEqual(new_pos, 1)

    def test_single_and_when_next_char_not_and(self):
        """Test single & behavior (not implemented, should raise error)."""
        source = "&x"
        with self.assertRaises(ValueError) as context:
            _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertIn("Unexpected character '&'", str(context.exception))

    def test_single_or_when_next_char_not_or(self):
        """Test single | behavior (not implemented, should raise error)."""
        source = "|x"
        with self.assertRaises(ValueError) as context:
            _scan_operator_or_punctuation(source, 0, 1, 1, "test.c")
        self.assertIn("Unexpected character '|'", str(context.exception))


if __name__ == "__main__":
    unittest.main()
