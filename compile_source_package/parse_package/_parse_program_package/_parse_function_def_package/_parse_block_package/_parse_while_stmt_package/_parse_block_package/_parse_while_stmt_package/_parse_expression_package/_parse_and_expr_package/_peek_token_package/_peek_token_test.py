# === imports ===
import unittest
from typing import Any, Dict

# === relative import for UUT ===
from ._peek_token_src import _peek_token

# === type aliases (matching source) ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_returns_current_token(self):
        """Happy path: pos is valid, should return token at that position."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": "",
        }

        result = _peek_token(parser_state)

        self.assertEqual(result, tokens[1])
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")

    def test_peek_token_returns_first_token(self):
        """Boundary case: pos is 0, should return first token."""
        tokens: list[Token] = [
            {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }

        result = _peek_token(parser_state)

        self.assertEqual(result, tokens[0])
        self.assertEqual(result["type"], "KEYWORD")

    def test_peek_token_returns_none_when_pos_equals_length(self):
        """Boundary case: pos equals len(tokens), should return None."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": "",
        }

        result = _peek_token(parser_state)

        self.assertIsNone(result)

    def test_peek_token_returns_none_when_pos_exceeds_length(self):
        """Edge case: pos is beyond len(tokens), should return None."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 5,
            "filename": "test.py",
            "error": "",
        }

        result = _peek_token(parser_state)

        self.assertIsNone(result)

    def test_peek_token_returns_none_for_empty_tokens(self):
        """Edge case: empty tokens list, should return None."""
        tokens: list[Token] = []
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }

        result = _peek_token(parser_state)

        self.assertIsNone(result)

    def test_peek_token_no_side_effects(self):
        """Verify function has no side effects on parser_state."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }
        original_pos = parser_state["pos"]
        original_tokens_length = len(parser_state["tokens"])

        _peek_token(parser_state)

        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(len(parser_state["tokens"]), original_tokens_length)

    def test_peek_token_at_last_valid_position(self):
        """Boundary case: pos is at last valid index (len-1)."""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 2,
            "filename": "test.py",
            "error": "",
        }

        result = _peek_token(parser_state)

        self.assertEqual(result, tokens[2])
        self.assertEqual(result["value"], "1")


if __name__ == "__main__":
    unittest.main()
