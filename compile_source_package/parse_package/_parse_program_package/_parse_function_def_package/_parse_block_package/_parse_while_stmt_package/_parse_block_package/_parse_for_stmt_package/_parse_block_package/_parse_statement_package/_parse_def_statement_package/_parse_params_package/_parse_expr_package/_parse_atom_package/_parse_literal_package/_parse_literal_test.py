"""Unit tests for _parse_literal function."""

import unittest
from typing import Any, Dict

from ._parse_literal_src import _parse_literal

Token = Dict[str, Any]
ParserState = Dict[str, Any]
AST = Dict[str, Any]


class TestParseLiteral(unittest.TestCase):
    """Test cases for _parse_literal function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

    def test_parse_number_integer(self) -> None:
        """Test parsing integer NUMBER token."""
        token: Token = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 5
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_number_float(self) -> None:
        """Test parsing float NUMBER token."""
        token: Token = {
            "type": "NUMBER",
            "value": "3.14",
            "line": 2,
            "column": 10
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_string(self) -> None:
        """Test parsing STRING token."""
        token: Token = {
            "type": "STRING",
            "value": "hello world",
            "line": 3,
            "column": 1
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_true(self) -> None:
        """Test parsing TRUE token."""
        token: Token = {
            "type": "TRUE",
            "value": "true",
            "line": 4,
            "column": 7
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "TRUE")
        self.assertIs(result["value"], True)
        self.assertEqual(result["line"], 4)
        self.assertEqual(result["column"], 7)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_false(self) -> None:
        """Test parsing FALSE token."""
        token: Token = {
            "type": "FALSE",
            "value": "false",
            "line": 5,
            "column": 12
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "FALSE")
        self.assertIs(result["value"], False)
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_none(self) -> None:
        """Test parsing NONE token."""
        token: Token = {
            "type": "NONE",
            "value": "none",
            "line": 6,
            "column": 3
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "NONE")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 6)
        self.assertEqual(result["column"], 3)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_literal_without_line_column(self) -> None:
        """Test parsing token without line/column (defaults to 0)."""
        token: Token = {
            "type": "NUMBER",
            "value": "100"
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 100)
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(self.parser_state["pos"], 1)

    def test_parse_invalid_token_type(self) -> None:
        """Test that invalid token type raises ValueError."""
        token: Token = {
            "type": "INVALID",
            "value": "something",
            "line": 1,
            "column": 1
        }
        
        with self.assertRaises(ValueError) as context:
            _parse_literal(self.parser_state, token)
        
        self.assertIn("Unknown literal token type: INVALID", str(context.exception))
        self.assertEqual(self.parser_state["pos"], 0)

    def test_pos_increment_multiple_calls(self) -> None:
        """Test that pos is incremented correctly across multiple calls."""
        self.parser_state["pos"] = 5
        
        token1: Token = {"type": "NUMBER", "value": "1"}
        token2: Token = {"type": "STRING", "value": "test"}
        token3: Token = {"type": "TRUE", "value": "true"}
        
        _parse_literal(self.parser_state, token1)
        self.assertEqual(self.parser_state["pos"], 6)
        
        _parse_literal(self.parser_state, token2)
        self.assertEqual(self.parser_state["pos"], 7)
        
        _parse_literal(self.parser_state, token3)
        self.assertEqual(self.parser_state["pos"], 8)

    def test_parse_number_negative_integer(self) -> None:
        """Test parsing negative integer NUMBER token."""
        token: Token = {
            "type": "NUMBER",
            "value": "-42",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], -42)
        self.assertIsInstance(result["value"], int)

    def test_parse_number_negative_float(self) -> None:
        """Test parsing negative float NUMBER token."""
        token: Token = {
            "type": "NUMBER",
            "value": "-3.14",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], -3.14)
        self.assertIsInstance(result["value"], float)

    def test_parse_string_empty(self) -> None:
        """Test parsing empty STRING token."""
        token: Token = {
            "type": "STRING",
            "value": "",
            "line": 1,
            "column": 1
        }
        
        result = _parse_literal(self.parser_state, token)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "")


if __name__ == "__main__":
    unittest.main()
