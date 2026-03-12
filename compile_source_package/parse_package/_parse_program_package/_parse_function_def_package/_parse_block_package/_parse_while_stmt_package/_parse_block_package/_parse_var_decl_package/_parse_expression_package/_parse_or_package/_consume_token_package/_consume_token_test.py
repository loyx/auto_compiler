# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest

from ._consume_token_src import _consume_token, Token, ParserState


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt", error: str = "") -> ParserState:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": error
        }

    def test_consume_token_happy_path_first_token(self):
        """Test consuming the first token successfully."""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("OPERATOR", "+"),
        ]
        state = self._create_parser_state(tokens, pos=0)

        token, new_state = _consume_token(state, "IDENTIFIER")

        self.assertEqual(token, tokens[0])
        self.assertEqual(new_state["pos"], 1)
        self.assertEqual(new_state["tokens"], tokens)
        self.assertEqual(new_state["filename"], "test.txt")
        self.assertEqual(new_state["error"], "")

    def test_consume_token_happy_path_middle_token(self):
        """Test consuming a token in the middle of the token stream."""
        tokens = [
            self._create_token("KEYWORD", "while"),
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "cond"),
            self._create_token("RPAREN", ")"),
        ]
        state = self._create_parser_state(tokens, pos=2)

        token, new_state = _consume_token(state, "IDENTIFIER")

        self.assertEqual(token, tokens[2])
        self.assertEqual(new_state["pos"], 3)

    def test_consume_token_happy_path_last_token(self):
        """Test consuming the last token in the stream."""
        tokens = [
            self._create_token("SEMICOLON", ";"),
        ]
        state = self._create_parser_state(tokens, pos=0)

        token, new_state = _consume_token(state, "SEMICOLON")

        self.assertEqual(token, tokens[0])
        self.assertEqual(new_state["pos"], 1)

    def test_consume_token_preserves_filename(self):
        """Test that filename is preserved in updated state."""
        tokens = [self._create_token("NUMBER", "42")]
        state = self._create_parser_state(tokens, pos=0, filename="custom_file.cc")

        _, new_state = _consume_token(state, "NUMBER")

        self.assertEqual(new_state["filename"], "custom_file.cc")

    def test_consume_token_preserves_error_field(self):
        """Test that error field is preserved in updated state."""
        tokens = [self._create_token("IDENTIFIER", "var")]
        state = self._create_parser_state(tokens, pos=0, error="previous error")

        _, new_state = _consume_token(state, "IDENTIFIER")

        self.assertEqual(new_state["error"], "previous error")

    def test_consume_token_preserves_missing_optional_fields(self):
        """Test that missing optional fields default to empty strings."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        state = {
            "tokens": tokens,
            "pos": 0
        }

        _, new_state = _consume_token(state, "IDENTIFIER")

        self.assertEqual(new_state.get("filename", ""), "")
        self.assertEqual(new_state.get("error", ""), "")

    def test_consume_token_end_of_input_raises_error(self):
        """Test that consuming past the end of tokens raises SyntaxError."""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
        ]
        state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_empty_tokens_list_raises_error(self):
        """Test that consuming from empty token list raises SyntaxError."""
        tokens = []
        state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_type_mismatch_raises_error(self):
        """Test that consuming wrong token type raises SyntaxError."""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
        ]
        state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "NUMBER")

        self.assertIn("Expected NUMBER, got IDENTIFIER", str(context.exception))

    def test_consume_token_type_mismatch_with_different_types(self):
        """Test type mismatch with various token types."""
        test_cases = [
            ("KEYWORD", "IDENTIFIER", "Expected IDENTIFIER, got KEYWORD"),
            ("LPAREN", "RPAREN", "Expected RPAREN, got LPAREN"),
            ("OPERATOR", "SEMICOLON", "Expected SEMICOLON, got OPERATOR"),
        ]

        for actual_type, expected_type, expected_msg in test_cases:
            with self.subTest(actual_type=actual_type, expected_type=expected_type):
                tokens = [self._create_token(actual_type, "val")]
                state = self._create_parser_state(tokens, pos=0)

                with self.assertRaises(SyntaxError) as context:
                    _consume_token(state, expected_type)

                self.assertIn(expected_msg, str(context.exception))

    def test_consume_token_returns_correct_token_value(self):
        """Test that the returned token has correct value and metadata."""
        tokens = [
            self._create_token("STRING", "hello world", line=5, column=10),
        ]
        state = self._create_parser_state(tokens, pos=0)

        token, _ = _consume_token(state, "STRING")

        self.assertEqual(token["type"], "STRING")
        self.assertEqual(token["value"], "hello world")
        self.assertEqual(token["line"], 5)
        self.assertEqual(token["column"], 10)

    def test_consume_token_does_not_modify_original_state(self):
        """Test that original parser state is not modified."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        state = self._create_parser_state(tokens, pos=0)
        original_pos = state["pos"]

        _, new_state = _consume_token(state, "IDENTIFIER")

        self.assertEqual(state["pos"], original_pos)
        self.assertEqual(new_state["pos"], original_pos + 1)
        self.assertIsNot(state, new_state)


if __name__ == "__main__":
    unittest.main()
