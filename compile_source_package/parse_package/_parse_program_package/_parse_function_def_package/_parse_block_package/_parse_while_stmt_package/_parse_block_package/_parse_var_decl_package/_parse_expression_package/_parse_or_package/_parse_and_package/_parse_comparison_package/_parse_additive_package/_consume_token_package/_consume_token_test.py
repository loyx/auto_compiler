import unittest
from typing import Dict, Any, List

# Import the function under test using relative import
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: List[Dict[str, Any]],
        pos: int = 0,
        filename: str = "test.txt"
    ) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_consume_token_success(self):
        """Test successful token consumption advances position."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
        ]
        state = self._create_parser_state(tokens, pos=0)

        new_state = _consume_token(state, "IDENTIFIER")

        self.assertEqual(new_state["pos"], 1)
        self.assertEqual(new_state["tokens"], tokens)
        self.assertEqual(new_state["filename"], "test.txt")
        # Verify original state is unchanged (immutable pattern)
        self.assertEqual(state["pos"], 0)

    def test_consume_token_success_middle_position(self):
        """Test consuming token from middle position."""
        tokens = [
            self._create_token("KEYWORD", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
        ]
        state = self._create_parser_state(tokens, pos=1)

        new_state = _consume_token(state, "LPAREN")

        self.assertEqual(new_state["pos"], 2)

    def test_consume_token_eof_empty_tokens(self):
        """Test EOF error when tokens list is empty."""
        state = self._create_parser_state([], pos=0, filename="empty.txt")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "IDENTIFIER")

        self.assertIn("Syntax error at empty.txt:", str(context.exception))
        self.assertIn("expected IDENTIFIER, got EOF", str(context.exception))

    def test_consume_token_eof_at_end(self):
        """Test EOF error when pos is at end of tokens."""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        state = self._create_parser_state(tokens, pos=1, filename="end.txt")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "OPERATOR")

        self.assertIn("Syntax error at end.txt:", str(context.exception))
        self.assertIn("expected OPERATOR, got EOF", str(context.exception))

    def test_consume_token_eof_beyond_end(self):
        """Test EOF error when pos is beyond tokens length."""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        state = self._create_parser_state(tokens, pos=5, filename="beyond.txt")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "IDENTIFIER")

        self.assertIn("Syntax error at beyond.txt:", str(context.exception))
        self.assertIn("expected IDENTIFIER, got EOF", str(context.exception))

    def test_consume_token_mismatch(self):
        """Test SyntaxError on token type mismatch."""
        tokens = [self._create_token("IDENTIFIER", "x", 2, 5)]
        state = self._create_parser_state(tokens, pos=0, filename="mismatch.txt")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "KEYWORD")

        error_msg = str(context.exception)
        self.assertIn("Syntax error at mismatch.txt:2:5:", error_msg)
        self.assertIn("expected KEYWORD, got IDENTIFIER", error_msg)

    def test_consume_token_mismatch_with_default_location(self):
        """Test mismatch error when token lacks line/column info."""
        token = {"type": "NUMBER", "value": "42"}
        tokens = [token]
        state = self._create_parser_state(tokens, pos=0, filename="noloc.txt")

        with self.assertRaises(SyntaxError) as context:
            _consume_token(state, "STRING")

        error_msg = str(context.exception)
        self.assertIn("Syntax error at noloc.txt:0:0:", error_msg)
        self.assertIn("expected STRING, got NUMBER", error_msg)

    def test_consume_token_preserves_other_fields(self):
        """Test that other state fields are preserved in returned state."""
        tokens = [self._create_token("SEMICOLON", ";", 3, 10)]
        state = self._create_parser_state(tokens, pos=0, filename="preserve.txt")
        state["error"] = "previous error"
        state["custom_field"] = "custom value"

        new_state = _consume_token(state, "SEMICOLON")

        self.assertEqual(new_state["error"], "previous error")
        self.assertEqual(new_state["custom_field"], "custom value")
        self.assertEqual(new_state["filename"], "preserve.txt")

    def test_consume_token_returns_copy(self):
        """Test that function returns a copy, not the original state."""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        state = self._create_parser_state(tokens, pos=0)

        new_state = _consume_token(state, "IDENTIFIER")

        # Verify they are different objects
        self.assertIsNot(new_state, state)
        # Modifying new_state should not affect original
        new_state["pos"] = 999
        self.assertEqual(state["pos"], 0)

    def test_consume_token_case_sensitive(self):
        """Test that token type matching is case-sensitive."""
        tokens = [self._create_token("identifier", "x", 1, 1)]
        state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError):
            _consume_token(state, "IDENTIFIER")


if __name__ == "__main__":
    unittest.main()
