# === std / third-party imports ===
import unittest

# === relative import of the function under test ===
from ._get_current_token_src import _get_current_token


class TestGetCurrentToken(unittest.TestCase):
    """Test cases for _get_current_token function."""

    def test_get_current_token_valid_position(self):
        """Happy path: pos is within valid range, returns the token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "OPERATOR", "value": "=", "line": 1, "column": 3})

    def test_get_current_token_first_token(self):
        """Boundary: pos = 0, returns first token."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "if", "line": 1, "column": 1})

    def test_get_current_token_last_token(self):
        """Boundary: pos = len(tokens) - 1, returns last token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "1", "line": 1, "column": 5})

    def test_get_current_token_pos_out_of_bounds_high(self):
        """Edge case: pos >= len(tokens), returns None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_pos_out_of_bounds_low(self):
        """Edge case: pos < 0, returns None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": -1,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_empty_tokens(self):
        """Edge case: empty tokens list, returns None."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_missing_tokens_key(self):
        """Edge case: missing 'tokens' key, defaults to empty list, returns None."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_get_current_token_missing_pos_key(self):
        """Edge case: missing 'pos' key, defaults to 0."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})

    def test_get_current_token_no_side_effects(self):
        """Verify function does not modify parser_state."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        original_state = dict(parser_state)
        original_tokens = list(parser_state["tokens"])
        
        _get_current_token(parser_state)
        
        self.assertEqual(parser_state, original_state)
        self.assertEqual(parser_state["tokens"], original_tokens)


if __name__ == "__main__":
    unittest.main()
