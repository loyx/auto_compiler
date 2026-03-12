# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token

Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestConsumeTokenHappyPath(unittest.TestCase):
    """Test happy path scenarios for _consume_token."""

    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_at_middle_position(self):
        """Test token consumption from middle of token list."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 5},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
            ],
            "filename": "test.py",
            "pos": 1,
            "error": "",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "func")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_last_token(self):
        """Test consuming the last token in the list."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 2, "column": 10},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        result = _consume_token(parser_state, "NUMBER")
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(parser_state["pos"], 1)


class TestConsumeTokenBoundaryConditions(unittest.TestCase):
    """Test boundary conditions for _consume_token."""

    def test_consume_token_empty_tokens_list(self):
        """Test consumption when tokens list is empty."""
        parser_state: ParserState = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected IDENTIFIER", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_pos_at_end(self):
        """Test consumption when pos equals tokens length."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 1,
            "error": "",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_pos_beyond_end(self):
        """Test consumption when pos exceeds tokens length."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "pos": 5,
            "error": "",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 5)


class TestConsumeTokenInvalidInput(unittest.TestCase):
    """Test invalid input scenarios for _consume_token."""

    def test_consume_token_type_mismatch(self):
        """Test consumption when token type doesn't match expected."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 15},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")
        
        self.assertIn("Syntax error", str(context.exception))
        self.assertIn("expected NUMBER", str(context.exception))
        self.assertIn("got IDENTIFIER", str(context.exception))
        self.assertIn("line 3", str(context.exception))
        self.assertIn("column 15", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_none_token(self):
        """Test consumption when current token is None."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                None,
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "filename": "test.py",
            "pos": 1,
            "error": "",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected None token", str(context.exception))
        self.assertIn("position 1", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_type_mismatch_missing_line_column(self):
        """Test type mismatch when token lacks line/column info."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")
        
        self.assertIn("Syntax error", str(context.exception))
        self.assertIn("line ?", str(context.exception))
        self.assertIn("column ?", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)


class TestConsumeTokenSideEffects(unittest.TestCase):
    """Test side effects of _consume_token."""

    def test_consume_token_pos_incremented(self):
        """Test that pos is correctly incremented after consumption."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "A", "value": "a", "line": 1, "column": 1},
                {"type": "B", "value": "b", "line": 1, "column": 2},
                {"type": "C", "value": "c", "line": 1, "column": 3},
            ],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        _consume_token(parser_state, "A")
        self.assertEqual(parser_state["pos"], 1)
        
        _consume_token(parser_state, "B")
        self.assertEqual(parser_state["pos"], 2)
        
        _consume_token(parser_state, "C")
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_returns_correct_token(self):
        """Test that the returned token is the one at current position."""
        token1 = {"type": "FIRST", "value": "one", "line": 1, "column": 1}
        token2 = {"type": "SECOND", "value": "two", "line": 1, "column": 2}
        
        parser_state: ParserState = {
            "tokens": [token1, token2],
            "filename": "test.py",
            "pos": 0,
            "error": "",
        }
        
        result = _consume_token(parser_state, "FIRST")
        self.assertIs(result, token1)
        
        result = _consume_token(parser_state, "SECOND")
        self.assertIs(result, token2)

    def test_consume_token_other_state_unchanged(self):
        """Test that other parser state fields remain unchanged."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test_module.py",
            "pos": 0,
            "error": "some previous error",
            "extra_field": "should not change",
        }
        
        _consume_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(parser_state["filename"], "test_module.py")
        self.assertEqual(parser_state["error"], "some previous error")
        self.assertEqual(parser_state["extra_field"], "should not change")
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
