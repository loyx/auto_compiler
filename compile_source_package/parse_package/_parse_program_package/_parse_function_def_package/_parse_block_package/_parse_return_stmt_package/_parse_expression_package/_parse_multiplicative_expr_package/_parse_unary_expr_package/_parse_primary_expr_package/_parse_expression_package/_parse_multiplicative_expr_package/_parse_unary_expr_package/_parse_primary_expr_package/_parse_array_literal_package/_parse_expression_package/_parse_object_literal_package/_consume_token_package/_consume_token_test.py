# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest

from ._consume_token_src import _consume_token, Token, ParserState


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> ParserState:
        """Helper to create a parser state dictionary."""
        state: ParserState = {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
        return state

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Token:
        """Helper to create a token dictionary."""
        token: Token = {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
        return token

    def test_consume_token_success(self):
        """Test successful token consumption with matching type."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("ASSIGN", "=", line=1, column=3),
            self._create_token("NUMBER", "42", line=1, column=5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_second_token(self):
        """Test consuming token at non-zero position."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("ASSIGN", "=", line=1, column=3),
            self._create_token("NUMBER", "42", line=1, column=5),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _consume_token(parser_state, "ASSIGN")

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_last_token(self):
        """Test consuming the last token in the list."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _consume_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_pos_out_of_bounds(self):
        """Test ValueError when pos is beyond token list length."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(ValueError) as context:
            _consume_token(parser_state, "IDENTIFIER")

        error_message = str(context.exception)
        self.assertIn("Unexpected end of input", error_message)
        self.assertIn("expected token type 'IDENTIFIER'", error_message)
        self.assertIn("but reached end of file", error_message)
        self.assertIn("test.py", error_message)

    def test_consume_token_empty_tokens(self):
        """Test ValueError when tokens list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(ValueError) as context:
            _consume_token(parser_state, "IDENTIFIER")

        error_message = str(context.exception)
        self.assertIn("Unexpected end of input", error_message)
        self.assertIn("expected token type 'IDENTIFIER'", error_message)

    def test_consume_token_type_mismatch(self):
        """Test ValueError when token type doesn't match expected."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=2, column=5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(ValueError) as context:
            _consume_token(parser_state, "NUMBER")

        error_message = str(context.exception)
        self.assertIn("Syntax error", error_message)
        self.assertIn("test.py:2:5", error_message)
        self.assertIn("expected token type 'NUMBER'", error_message)
        self.assertIn("but got 'IDENTIFIER'", error_message)

    def test_consume_token_type_mismatch_with_custom_filename(self):
        """Test error message includes custom filename."""
        tokens = [
            self._create_token("LEFT_PAREN", "(", line=10, column=20),
        ]
        parser_state = self._create_parser_state(
            tokens, pos=0, filename="my_script.js"
        )

        with self.assertRaises(ValueError) as context:
            _consume_token(parser_state, "RIGHT_PAREN")

        error_message = str(context.exception)
        self.assertIn("my_script.js:10:20", error_message)
        self.assertIn("expected token type 'RIGHT_PAREN'", error_message)
        self.assertIn("but got 'LEFT_PAREN'", error_message)

    def test_consume_token_missing_filename_uses_default(self):
        """Test that missing filename defaults to '<unknown>'."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0
        }

        with self.assertRaises(ValueError) as context:
            _consume_token(parser_state, "NUMBER")

        error_message = str(context.exception)
        self.assertIn("<unknown>", error_message)

    def test_consume_token_pos_not_modified_on_error(self):
        """Test that pos is not advanced when error occurs."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]

        with self.assertRaises(ValueError):
            _consume_token(parser_state, "NUMBER")

        self.assertEqual(parser_state["pos"], original_pos)

    def test_consume_token_with_special_token_types(self):
        """Test consuming tokens with various special type names."""
        special_types = [
            "LEFT_BRACE", "RIGHT_BRACE", "LEFT_PAREN", "RIGHT_PAREN",
            "COMMA", "SEMICOLON", "PLUS", "MINUS", "STAR", "SLASH",
            "KEYWORD_IF", "KEYWORD_WHILE", "KEYWORD_RETURN", "EOF"
        ]

        for token_type in special_types:
            with self.subTest(token_type=token_type):
                tokens = [
                    self._create_token(token_type, token_type.lower(), line=1, column=1),
                ]
                parser_state = self._create_parser_state(tokens, pos=0)

                result = _consume_token(parser_state, token_type)

                self.assertEqual(result["type"], token_type)
                self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_preserves_token_data(self):
        """Test that returned token preserves all original data."""
        original_token = {
            "type": "STRING_LITERAL",
            "value": "hello world",
            "line": 5,
            "column": 10,
            "extra_field": "should_be_preserved"
        }
        tokens = [original_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _consume_token(parser_state, "STRING_LITERAL")

        self.assertEqual(result["type"], "STRING_LITERAL")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result.get("extra_field"), "should_be_preserved")


if __name__ == "__main__":
    unittest.main()
