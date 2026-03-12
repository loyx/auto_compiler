# -*- coding: utf-8 -*-
"""Unit tests for _consume_token function."""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token parser utility function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create a parser state dict."""
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
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_consume_token_no_expectations(self):
        """Test consuming token without any expectations."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state)

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_matching_type(self):
        """Test consuming token with matching expected_type."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state, expected_type="IDENTIFIER")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_matching_value(self):
        """Test consuming token with matching expected_value."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        result = _consume_token(parser_state, expected_value="x")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_both_matching_expectations(self):
        """Test consuming token with both matching expected_type and expected_value."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        result = _consume_token(
            parser_state,
            expected_type="IDENTIFIER",
            expected_value="x"
        )

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_end_of_input(self):
        """Test consuming token when at end of input raises SyntaxError."""
        parser_state = self._create_parser_state([], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)  # pos should not change on error

    def test_consume_token_past_end_of_input(self):
        """Test consuming token when position is past end of input raises SyntaxError."""
        token = self._create_token("IDENTIFIER", "x")
        parser_state = self._create_parser_state([token], pos=1)

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)  # pos should not change on error

    def test_consume_token_type_mismatch(self):
        """Test consuming token with non-matching expected_type raises SyntaxError."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="NUMBER")

        self.assertIn("Expected token type 'NUMBER', got 'IDENTIFIER'", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)  # pos should not change on error

    def test_consume_token_value_mismatch(self):
        """Test consuming token with non-matching expected_value raises SyntaxError."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        parser_state = self._create_parser_state([token])

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_value="y")

        self.assertIn("Expected token value 'y', got 'x'", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)  # pos should not change on error

    def test_consume_token_type_mismatch_unknown_type(self):
        """Test consuming token when token has no type field."""
        token = {"value": "x", "line": 1, "column": 1}  # missing "type"
        parser_state = self._create_parser_state([token])

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="IDENTIFIER")

        self.assertIn("Expected token type 'IDENTIFIER', got '<unknown>'", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_value_mismatch_unknown_value(self):
        """Test consuming token when token has no value field."""
        token = {"type": "IDENTIFIER", "line": 1, "column": 1}  # missing "value"
        parser_state = self._create_parser_state([token])

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_value="x")

        self.assertIn("Expected token value 'x', got '<unknown>'", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_multiple_tokens_sequence(self):
        """Test consuming multiple tokens in sequence."""
        token1 = self._create_token("IDENTIFIER", "x", line=1, column=1)
        token2 = self._create_token("OPERATOR", "+", line=1, column=3)
        token3 = self._create_token("NUMBER", "5", line=1, column=5)
        parser_state = self._create_parser_state([token1, token2, token3])

        result1 = _consume_token(parser_state)
        self.assertEqual(result1, token1)
        self.assertEqual(parser_state["pos"], 1)

        result2 = _consume_token(parser_state)
        self.assertEqual(result2, token2)
        self.assertEqual(parser_state["pos"], 2)

        result3 = _consume_token(parser_state)
        self.assertEqual(result3, token3)
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_middle_of_token_list(self):
        """Test consuming token from middle of token list."""
        token1 = self._create_token("IDENTIFIER", "x", line=1, column=1)
        token2 = self._create_token("OPERATOR", "+", line=1, column=3)
        token3 = self._create_token("NUMBER", "5", line=1, column=5)
        parser_state = self._create_parser_state([token1, token2, token3], pos=1)

        result = _consume_token(parser_state)

        self.assertEqual(result, token2)
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_preserves_other_state_fields(self):
        """Test that consuming token doesn't modify other parser state fields."""
        token = self._create_token("IDENTIFIER", "x")
        parser_state = self._create_parser_state([token], filename="my_test.py")
        parser_state["error"] = "some error"
        parser_state["extra_field"] = "extra value"

        _consume_token(parser_state)

        self.assertEqual(parser_state["filename"], "my_test.py")
        self.assertEqual(parser_state["error"], "some error")
        self.assertEqual(parser_state["extra_field"], "extra value")
        self.assertEqual(parser_state["tokens"], [token])  # tokens list unchanged


if __name__ == "__main__":
    unittest.main()
