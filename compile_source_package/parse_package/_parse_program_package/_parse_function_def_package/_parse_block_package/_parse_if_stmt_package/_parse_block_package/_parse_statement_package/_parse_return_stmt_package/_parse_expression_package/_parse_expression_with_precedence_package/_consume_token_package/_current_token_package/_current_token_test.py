# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._current_token_src import _current_token


class TestCurrentToken(unittest.TestCase):
    """Test cases for _current_token function."""

    def test_current_token_returns_token_at_position(self):
        """Happy path: pos is valid, returns tokens[pos]."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "OPERATOR", "value": "=", "line": 1, "column": 3})

    def test_current_token_returns_first_token(self):
        """Boundary: pos = 0 (first token)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "def", "line": 1, "column": 1})

    def test_current_token_returns_last_token(self):
        """Boundary: pos = len(tokens) - 1 (last token)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "1", "line": 1, "column": 5})

    def test_current_token_returns_none_when_pos_equals_length(self):
        """Edge case: pos == len(tokens), returns None."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_returns_none_when_pos_exceeds_length(self):
        """Edge case: pos > len(tokens), returns None."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_returns_none_for_empty_tokens(self):
        """Edge case: empty tokens list, returns None."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_does_not_modify_state(self):
        """Verify no side effects: parser_state remains unchanged."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        original_pos = parser_state["pos"]
        original_tokens = parser_state["tokens"].copy()
        
        _current_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)


if __name__ == "__main__":
    unittest.main()
