# -*- coding: utf-8 -*-
"""
Unit tests for _expect_token function.
Tests token expectation, consumption, and error handling in parser state.
"""

import unittest
from typing import Any, Dict

from ._expect_token_src import _expect_token


Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""

    def test_expect_token_success_consumes_and_returns(self):
        """Happy path: token type matches, token is consumed and returned."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _expect_token(parser_state, "IF")

        self.assertEqual(result["type"], "IF")
        self.assertEqual(result["value"], "if")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_at_middle_position(self):
        """Token matches at middle position, pos advances correctly."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }

        result = _expect_token(parser_state, "LPAREN")

        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(result["value"], "(")
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_success_at_last_token(self):
        """Token matches at last position, pos advances beyond tokens."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        result = _expect_token(parser_state, "IF")

        self.assertEqual(result["type"], "IF")
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_raises_when_pos_beyond_tokens(self):
        """Raises SyntaxError when pos is beyond token list length."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "RPAREN")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("RPAREN", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_raises_when_tokens_empty(self):
        """Raises SyntaxError when tokens list is empty."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IF")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_expect_token_raises_when_type_mismatch(self):
        """Raises SyntaxError when token type doesn't match expected."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 2, "column": 5},
                {"type": "LPAREN", "value": "(", "line": 2, "column": 8},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "RPAREN")

        self.assertIn("Expected RPAREN", str(context.exception))
        self.assertIn("got IF", str(context.exception))
        self.assertIn("line 2", str(context.exception))
        self.assertIn("column 5", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_pos_not_advanced_on_mismatch(self):
        """pos is not advanced when token type doesn't match."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        try:
            _expect_token(parser_state, "RPAREN")
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_multiple_sequential_calls(self):
        """Multiple sequential calls consume tokens correctly."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        token1 = _expect_token(parser_state, "IF")
        token2 = _expect_token(parser_state, "LPAREN")
        token3 = _expect_token(parser_state, "RPAREN")

        self.assertEqual(token1["type"], "IF")
        self.assertEqual(token2["type"], "LPAREN")
        self.assertEqual(token3["type"], "RPAREN")
        self.assertEqual(parser_state["pos"], 3)

    def test_expect_token_with_various_token_types(self):
        """Test with various common token types."""
        test_cases = [
            ("LPAREN", "("),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("RBRACE", "}"),
            ("LBRACKET", "["),
            ("RBRACKET", "]"),
            ("COLON", ":"),
            ("SEMICOLON", ";"),
            ("COMMA", ","),
            ("ASSIGN", "="),
            ("PLUS", "+"),
            ("MINUS", "-"),
            ("STAR", "*"),
            ("SLASH", "/"),
        ]

        for token_type, token_value in test_cases:
            parser_state: ParserState = {
                "tokens": [
                    {"type": token_type, "value": token_value, "line": 1, "column": 1},
                ],
                "pos": 0,
                "filename": "test.py",
            }

            result = _expect_token(parser_state, token_type)

            self.assertEqual(result["type"], token_type)
            self.assertEqual(result["value"], token_value)
            self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
