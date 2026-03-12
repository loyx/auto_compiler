import unittest
from typing import Dict, Any

# Relative import from the same package
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
        """Helper to create a parser state dict."""
        if tokens is None:
            tokens = []
        state = {
            "tokens": tokens,
            "filename": filename,
            "pos": pos
        }
        if error is not None:
            state["error"] = error
        return state

    def _create_token(
        self,
        token_type: str,
        value: str = "",
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

    def test_consume_token_success(self):
        """Happy path: token type matches expected type."""
        token = self._create_token("IDENT", "x")
        parser_state = self._create_parser_state(tokens=[token], pos=0)

        result = _consume_token(parser_state, "IDENT")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_consume_token_type_mismatch(self):
        """Error case: token type doesn't match expected type."""
        token = self._create_token("IDENT", "x")
        parser_state = self._create_parser_state(tokens=[token], pos=0)

        result = _consume_token(parser_state, "ASSIGN")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Expected ASSIGN, got IDENT")

    def test_consume_token_out_of_bounds(self):
        """Boundary case: pos is at or beyond end of tokens."""
        token = self._create_token("IDENT", "x")
        parser_state = self._create_parser_state(tokens=[token], pos=1)

        result = _consume_token(parser_state, "IDENT")

        self.assertEqual(result, {})
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_consume_token_empty_tokens(self):
        """Edge case: empty tokens list."""
        parser_state = self._create_parser_state(tokens=[], pos=0)

        result = _consume_token(parser_state, "IDENT")

        self.assertEqual(result, {})
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_consume_token_at_last_element(self):
        """Boundary case: pos at last token in list."""
        token1 = self._create_token("IDENT", "x")
        token2 = self._create_token("ASSIGN", "=")
        parser_state = self._create_parser_state(tokens=[token1, token2], pos=1)

        result = _consume_token(parser_state, "ASSIGN")

        self.assertEqual(result, token2)
        self.assertEqual(parser_state["pos"], 2)
        self.assertNotIn("error", parser_state)

    def test_consume_token_multiple_successive(self):
        """Test consuming multiple tokens in sequence."""
        token1 = self._create_token("IDENT", "x")
        token2 = self._create_token("ASSIGN", "=")
        token3 = self._create_token("NUMBER", "42")
        parser_state = self._create_parser_state(tokens=[token1, token2, token3], pos=0)

        result1 = _consume_token(parser_state, "IDENT")
        result2 = _consume_token(parser_state, "ASSIGN")
        result3 = _consume_token(parser_state, "NUMBER")

        self.assertEqual(result1, token1)
        self.assertEqual(result2, token2)
        self.assertEqual(result3, token3)
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_preserves_existing_error(self):
        """Test that function overwrites existing error field."""
        token = self._create_token("IDENT", "x")
        parser_state = self._create_parser_state(
            tokens=[token],
            pos=0,
            error="Previous error"
        )

        result = _consume_token(parser_state, "ASSIGN")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["error"], "Expected ASSIGN, got IDENT")

    def test_consume_token_different_token_types(self):
        """Test with various token types."""
        test_cases = [
            ("KEYWORD", "if"),
            ("LPAREN", "("),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("RBRACE", "}"),
            ("SEMICOLON", ";"),
            ("STRING", '"hello"'),
        ]

        for token_type, value in test_cases:
            with self.subTest(token_type=token_type):
                token = self._create_token(token_type, value)
                parser_state = self._create_parser_state(tokens=[token], pos=0)

                result = _consume_token(parser_state, token_type)

                self.assertEqual(result, token)
                self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
