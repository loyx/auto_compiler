# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_without_expected_type(self):
        """Test consuming a token without type constraint."""
        token: Token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_matching_expected_type(self):
        """Test consuming a token with matching expected type."""
        token: Token = {"type": "NUMBER", "value": "42", "line": 2, "column": 10}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state, expected_type="NUMBER")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_mismatched_expected_type_raises(self):
        """Test that mismatched expected type raises SyntaxError."""
        token: Token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="NUMBER")

        self.assertIn("Expected token type 'NUMBER'", str(context.exception))
        self.assertIn("got 'IDENTIFIER'", str(context.exception))
        # pos should NOT be incremented on error
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_advances_position(self):
        """Test that consuming a token advances the position counter."""
        tokens: list = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Consume first token
        result1 = _consume_token(parser_state)
        self.assertEqual(result1, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

        # Consume second token
        result2 = _consume_token(parser_state)
        self.assertEqual(result2, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

        # Consume third token
        result3 = _consume_token(parser_state)
        self.assertEqual(result3, tokens[2])
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_from_middle_position(self):
        """Test consuming a token starting from a middle position."""
        tokens: list = [
            {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }

        result = _consume_token(parser_state, expected_type="IDENTIFIER")

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_preserves_original_state_mutability(self):
        """Test that parser_state is mutated in place."""
        token: Token = {"type": "STRING", "value": "hello", "line": 3, "column": 1}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        original_state_id = id(parser_state)

        _consume_token(parser_state)

        # Verify same object is mutated
        self.assertEqual(id(parser_state), original_state_id)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_various_token_types(self):
        """Test consuming tokens of various types."""
        test_cases = [
            ("KEYWORD", "while"),
            ("OPERATOR", "+"),
            ("LPAREN", "("),
            ("RPAREN", ")"),
            ("LBRACKET", "["),
            ("RBRACKET", "]"),
            ("COLON", ":"),
            ("COMMA", ","),
            ("NEWLINE", "\n"),
            ("INDENT", "    "),
            ("DEDENT", ""),
        ]

        for token_type, token_value in test_cases:
            with self.subTest(token_type=token_type):
                token: Token = {
                    "type": token_type,
                    "value": token_value,
                    "line": 1,
                    "column": 1
                }
                parser_state: ParserState = {
                    "tokens": [token],
                    "pos": 0,
                    "filename": "test.py"
                }

                result = _consume_token(parser_state, expected_type=token_type)

                self.assertEqual(result, token)
                self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_empty_string_value(self):
        """Test consuming a token with empty string value."""
        token: Token = {"type": "DEDENT", "value": "", "line": 5, "column": 0}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertEqual(result, token)
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_special_characters_in_value(self):
        """Test consuming a token with special characters in value."""
        token: Token = {"type": "STRING", "value": "hello\nworld\t!", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertEqual(result, token)
        self.assertEqual(result["value"], "hello\nworld\t!")
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_case_sensitive_type_check(self):
        """Test that type checking is case-sensitive."""
        token: Token = {"type": "identifier", "value": "x", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        # Lowercase 'identifier' should not match uppercase 'IDENTIFIER'
        with self.assertRaises(SyntaxError):
            _consume_token(parser_state, expected_type="IDENTIFIER")

        # But lowercase should match
        parser_state["pos"] = 0
        result = _consume_token(parser_state, expected_type="identifier")
        self.assertEqual(result, token)


if __name__ == "__main__":
    unittest.main()
