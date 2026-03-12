# === std / third-party imports ===
import unittest

# === relative import of target module ===
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_valid_position(self):
        """Happy path: pos points to a valid token."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "OP", "value": "=", "line": 1, "column": 3})
        # Verify parser_state is not modified
        self.assertEqual(parser_state["pos"], 1)

    def test_peek_token_at_first_position(self):
        """Edge case: pos at the beginning (0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "IDENT", "value": "x", "line": 1, "column": 1})

    def test_peek_token_at_end_position(self):
        """Edge case: pos equals len(tokens), should return None."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_beyond_end_position(self):
        """Edge case: pos > len(tokens), should return None."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Edge case: empty tokens list, should return None."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Edge case: missing tokens key in parser_state, should use default empty list."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Edge case: missing pos key in parser_state, should use default 0."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "IDENT", "value": "x", "line": 1, "column": 1})

    def test_peek_token_no_modification_to_parser_state(self):
        """Verify parser_state is not modified after peek."""
        original_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        # Make a copy to compare
        import copy
        expected_state = copy.deepcopy(original_state)
        
        _peek_token(original_state)
        
        self.assertEqual(original_state, expected_state)

    def test_peek_token_single_token_at_pos_zero(self):
        """Edge case: single token list with pos at 0."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 5, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "while", "line": 5, "column": 1})

    def test_peek_token_single_token_beyond_pos(self):
        """Edge case: single token list with pos beyond it."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 5, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
