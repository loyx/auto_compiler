#!/usr/bin/env python3
"""
Unit tests for _parse_literal function.
Tests parsing of NUMBER, STRING, and BOOLEAN literal tokens into AST nodes.
"""

import unittest
from copy import deepcopy

from ._parse_literal_src import _parse_literal


class TestParseLiteralNumber(unittest.TestCase):
    """Test cases for NUMBER token parsing."""

    def test_integer_number(self):
        """Test parsing integer NUMBER token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 5
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_float_number(self):
        """Test parsing float NUMBER token (contains decimal point)."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "3.14",
            "line": 2,
            "column": 10
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_negative_integer(self):
        """Test parsing negative integer NUMBER token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "-100",
            "line": 3,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], -100)
        self.assertIsInstance(result["value"], int)

    def test_negative_float(self):
        """Test parsing negative float NUMBER token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "-2.5",
            "line": 1,
            "column": 8
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], -2.5)
        self.assertIsInstance(result["value"], float)

    def test_invalid_number_format(self):
        """Test NUMBER token with invalid format keeps original string."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "12abc",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "12abc")
        self.assertIsInstance(result["value"], str)

    def test_parser_state_pos_incremented(self):
        """Test that parser_state['pos'] is incremented after parsing."""
        parser_state = {"pos": 5, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "999",
            "line": 1,
            "column": 1
        }
        
        _parse_literal(parser_state, token)
        
        self.assertEqual(parser_state["pos"], 6)


class TestParseLiteralString(unittest.TestCase):
    """Test cases for STRING token parsing."""

    def test_double_quoted_string(self):
        """Test parsing double-quoted STRING token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": '"hello world"',
            "line": 1,
            "column": 3
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 1)

    def test_single_quoted_string(self):
        """Test parsing single-quoted STRING token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": "'hello world'",
            "line": 2,
            "column": 7
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")

    def test_empty_double_quoted_string(self):
        """Test parsing empty double-quoted STRING token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": '""',
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "")

    def test_empty_single_quoted_string(self):
        """Test parsing empty single-quoted STRING token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": "''",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "")

    def test_string_without_quotes(self):
        """Test STRING token without surrounding quotes keeps original value."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": "no_quotes",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "no_quotes")

    def test_string_with_mismatched_quotes(self):
        """Test STRING token with mismatched quotes keeps original value."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": '"mismatched\'',
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], '"mismatched\'')


class TestParseLiteralBoolean(unittest.TestCase):
    """Test cases for BOOLEAN token parsing."""

    def test_true_lowercase(self):
        """Test parsing 'true' (lowercase) BOOLEAN token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "BOOLEAN",
            "value": "true",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], True)
        self.assertIsInstance(result["value"], bool)
        self.assertEqual(parser_state["pos"], 1)

    def test_true_uppercase(self):
        """Test parsing 'TRUE' (uppercase) BOOLEAN token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "BOOLEAN",
            "value": "TRUE",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], True)

    def test_true_mixed_case(self):
        """Test parsing 'TrUe' (mixed case) BOOLEAN token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "BOOLEAN",
            "value": "TrUe",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], True)

    def test_false_lowercase(self):
        """Test parsing 'false' (lowercase) BOOLEAN token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "BOOLEAN",
            "value": "false",
            "line": 2,
            "column": 5
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], False)
        self.assertIsInstance(result["value"], bool)

    def test_false_uppercase(self):
        """Test parsing 'FALSE' (uppercase) BOOLEAN token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "BOOLEAN",
            "value": "FALSE",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], False)

    def test_false_mixed_case(self):
        """Test parsing 'FaLsE' (mixed case) BOOLEAN token."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "BOOLEAN",
            "value": "FaLsE",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], False)


class TestParseLiteralInvalid(unittest.TestCase):
    """Test cases for invalid token types."""

    def test_invalid_token_type_raises_valueerror(self):
        """Test that unexpected token type raises ValueError."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with self.assertRaises(ValueError) as context:
            _parse_literal(parser_state, token)
        
        self.assertIn("IDENTIFIER", str(context.exception))

    def test_invalid_token_type_error_message(self):
        """Test ValueError message contains token type."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "UNKNOWN",
            "value": "test",
            "line": 1,
            "column": 1
        }
        
        with self.assertRaises(ValueError) as context:
            _parse_literal(parser_state, token)
        
        self.assertEqual(str(context.exception), "Unexpected token type: UNKNOWN")


class TestParseLiteralEdgeCases(unittest.TestCase):
    """Edge case tests for _parse_literal."""

    def test_zero_integer(self):
        """Test parsing zero as integer."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "0",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["value"], 0)
        self.assertIsInstance(result["value"], int)

    def test_zero_float(self):
        """Test parsing 0.0 as float."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "0.0",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["value"], 0.0)
        self.assertIsInstance(result["value"], float)

    def test_large_integer(self):
        """Test parsing large integer."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "NUMBER",
            "value": "999999999999",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["value"], 999999999999)
        self.assertIsInstance(result["value"], int)

    def test_string_with_special_characters(self):
        """Test parsing string with special characters."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": '"hello\\nworld\\t!"',
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["value"], "hello\\nworld\\t!")

    def test_parser_state_not_mutated_other_fields(self):
        """Test that only 'pos' field is mutated in parser_state."""
        parser_state = {
            "pos": 3,
            "tokens": [{"type": "NUMBER", "value": "1"}],
            "filename": "test.txt",
            "error": None
        }
        original_state = deepcopy(parser_state)
        token = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 1
        }
        
        _parse_literal(parser_state, token)
        
        self.assertEqual(parser_state["tokens"], original_state["tokens"])
        self.assertEqual(parser_state["filename"], original_state["filename"])
        self.assertEqual(parser_state["error"], original_state["error"])
        self.assertEqual(parser_state["pos"], original_state["pos"] + 1)

    def test_metadata_preserved(self):
        """Test that line and column metadata are preserved correctly."""
        parser_state = {"pos": 0, "tokens": []}
        token = {
            "type": "STRING",
            "value": '"test"',
            "line": 100,
            "column": 250
        }
        
        result = _parse_literal(parser_state, token)
        
        self.assertEqual(result["line"], 100)
        self.assertEqual(result["column"], 250)


if __name__ == "__main__":
    unittest.main()
