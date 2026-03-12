# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        if tokens is None:
            tokens = []
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_consume_token_no_validation(self):
        """Test consuming a token without any validation."""
        token = self._create_token("IDENTIFIER", "x", 1, 5)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(parser_state)

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_expected_type_match(self):
        """Test consuming a token with matching expected_type."""
        token = self._create_token("NUMBER", "42", 2, 10)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(parser_state, expected_type="NUMBER")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_expected_value_match(self):
        """Test consuming a token with matching expected_value."""
        token = self._create_token("STRING", "hello", 3, 15)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(parser_state, expected_value="hello")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_both_validations_match(self):
        """Test consuming a token with both expected_type and expected_value matching."""
        token = self._create_token("OPERATOR", "+", 1, 20)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(
            parser_state,
            expected_type="OPERATOR",
            expected_value="+"
        )

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_end_of_input(self):
        """Test that SyntaxError is raised when at end of input."""
        parser_state = self._create_parser_state([], 0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_consume_token_end_of_input_with_position(self):
        """Test that SyntaxError is raised when position is beyond tokens."""
        token = self._create_token("IDENTIFIER", "x")
        parser_state = self._create_parser_state([token], 1)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_type_mismatch(self):
        """Test that SyntaxError is raised when token type doesn't match."""
        token = self._create_token("IDENTIFIER", "x", 5, 12)
        parser_state = self._create_parser_state([token], 0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="NUMBER")

        self.assertIn("Expected token type 'NUMBER'", str(context.exception))
        self.assertIn("but got 'IDENTIFIER'", str(context.exception))
        self.assertIn("5:12", str(context.exception))

    def test_consume_token_value_mismatch(self):
        """Test that SyntaxError is raised when token value doesn't match."""
        token = self._create_token("IDENTIFIER", "x", 7, 8)
        parser_state = self._create_parser_state([token], 0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_value="y")

        self.assertIn("Expected token value 'y'", str(context.exception))
        self.assertIn("but got 'x'", str(context.exception))
        self.assertIn("7:8", str(context.exception))

    def test_consume_token_type_and_value_mismatch(self):
        """Test that SyntaxError is raised for type mismatch before value check."""
        token = self._create_token("IDENTIFIER", "x", 1, 1)
        parser_state = self._create_parser_state([token], 0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(
                parser_state,
                expected_type="NUMBER",
                expected_value="42"
            )

        self.assertIn("Expected token type 'NUMBER'", str(context.exception))

    def test_consume_token_multiple_tokens_sequence(self):
        """Test consuming multiple tokens in sequence."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        token1 = _consume_token(parser_state)
        self.assertEqual(token1["type"], "IDENTIFIER")
        self.assertEqual(token1["value"], "x")
        self.assertEqual(parser_state["pos"], 1)

        token2 = _consume_token(parser_state)
        self.assertEqual(token2["type"], "OPERATOR")
        self.assertEqual(token2["value"], "=")
        self.assertEqual(parser_state["pos"], 2)

        token3 = _consume_token(parser_state)
        self.assertEqual(token3["type"], "NUMBER")
        self.assertEqual(token3["value"], "42")
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_middle_of_list(self):
        """Test consuming a token from the middle of the token list."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("IDENTIFIER", "b", 1, 3),
            self._create_token("IDENTIFIER", "c", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 1)

        result = _consume_token(parser_state)

        self.assertEqual(result["value"], "b")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_preserves_original_token(self):
        """Test that the returned token is the same object from the list."""
        token = self._create_token("KEYWORD", "if", 10, 25)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(parser_state)

        self.assertIs(result, token)

    def test_consume_token_with_custom_filename(self):
        """Test error messages include custom filename."""
        parser_state = self._create_parser_state([], 0, "my_module.py")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("my_module.py", str(context.exception))

    def test_consume_token_only_type_validation(self):
        """Test that only type is validated when only expected_type is provided."""
        token = self._create_token("STRING", "any_value", 1, 1)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(parser_state, expected_type="STRING")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_only_value_validation(self):
        """Test that only value is validated when only expected_value is provided."""
        token = self._create_token("ANY_TYPE", "specific", 1, 1)
        parser_state = self._create_parser_state([token], 0)

        result = _consume_token(parser_state, expected_value="specific")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
