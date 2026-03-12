# -*- coding: utf-8 -*-
"""
Unit tests for _consume_token function.
Tests token consumption logic in parser state management.
"""

import unittest
from typing import Dict, Any

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py",
        error: str = None
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        state = {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename
        }
        if error is not None:
            state["error"] = error
        return state

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_consume_token_success(self):
        """Happy path: token type matches, pos advances by 1."""
        tokens = [
            self._create_token("BREAK", "break"),
            self._create_token("SEMICOLON", ";")
        ]
        state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(state, "BREAK")

        self.assertIs(result, state, "Should return the same dict object")
        self.assertEqual(result["pos"], 1, "Position should advance by 1")
        self.assertNotIn("error", result, "Should not have error on success")

    def test_consume_token_second_token(self):
        """Consume token when pos is not at start."""
        tokens = [
            self._create_token("IF", "if"),
            self._create_token("BREAK", "break"),
            self._create_token("SEMICOLON", ";")
        ]
        state = self._create_parser_state(tokens=tokens, pos=1)

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["pos"], 2, "Position should advance from 1 to 2")
        self.assertNotIn("error", result)

    def test_consume_token_type_mismatch(self):
        """Error case: token type does not match expected type."""
        tokens = [
            self._create_token("IF", "if"),
            self._create_token("BREAK", "break")
        ]
        state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["pos"], 0, "Position should not advance on mismatch")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Expected token type BREAK, got IF")

    def test_consume_token_empty_tokens(self):
        """Boundary: empty tokens list should set error."""
        state = self._create_parser_state(tokens=[], pos=0)

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["pos"], 0, "Position should not change")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Unexpected end of tokens, expected BREAK")

    def test_consume_token_pos_at_end(self):
        """Boundary: pos equals tokens length should set error."""
        tokens = [
            self._create_token("BREAK", "break"),
            self._create_token("SEMICOLON", ";")
        ]
        state = self._create_parser_state(tokens=tokens, pos=2)

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["pos"], 2, "Position should not change")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Unexpected end of tokens, expected BREAK")

    def test_consume_token_pos_beyond_end(self):
        """Boundary: pos beyond tokens length should set error."""
        tokens = [
            self._create_token("BREAK", "break")
        ]
        state = self._create_parser_state(tokens=tokens, pos=5)

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["pos"], 5, "Position should not change")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Unexpected end of tokens, expected BREAK")

    def test_consume_token_preserves_other_fields(self):
        """Verify other parser state fields are preserved."""
        tokens = [self._create_token("BREAK", "break")]
        state = self._create_parser_state(
            tokens=tokens,
            pos=0,
            filename="my_file.py"
        )

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["filename"], "my_file.py")
        self.assertEqual(result["tokens"], tokens)

    def test_consume_token_error_message_with_actual_type(self):
        """Verify error message includes actual token type on mismatch."""
        tokens = [self._create_token("CONTINUE", "continue")]
        state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["error"], "Expected token type BREAK, got CONTINUE")

    def test_consume_token_multiple_sequential(self):
        """Test consuming multiple tokens in sequence."""
        tokens = [
            self._create_token("BREAK", "break"),
            self._create_token("SEMICOLON", ";"),
            self._create_token("IF", "if")
        ]
        state = self._create_parser_state(tokens=tokens, pos=0)

        result1 = _consume_token(state, "BREAK")
        self.assertEqual(result1["pos"], 1)
        self.assertNotIn("error", result1)

        result2 = _consume_token(result1, "SEMICOLON")
        self.assertEqual(result2["pos"], 2)
        self.assertNotIn("error", result2)

        result3 = _consume_token(result2, "IF")
        self.assertEqual(result3["pos"], 3)
        self.assertNotIn("error", result3)

    def test_consume_token_with_existing_error(self):
        """Test behavior when parser state already has an error."""
        tokens = [self._create_token("BREAK", "break")]
        state = self._create_parser_state(
            tokens=tokens,
            pos=0,
            error="Previous error"
        )

        result = _consume_token(state, "BREAK")

        self.assertEqual(result["pos"], 1)
        self.assertNotIn("error", result, "Error should be cleared on successful consume")

    def test_consume_token_case_sensitive(self):
        """Verify token type matching is case sensitive."""
        tokens = [self._create_token("break", "break")]
        state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(state, "BREAK")

        self.assertIn("error", result)
        self.assertEqual(result["error"], "Expected token type BREAK, got break")


if __name__ == "__main__":
    unittest.main()
