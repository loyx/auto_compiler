# === test file for _peek_token ===
import unittest
from typing import Any, Dict

# Import the function under test using relative import
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_first_position(self):
        """Test peeking at the first token (pos=0)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
                {"type": "OPERATOR", "value": ">", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "while", "line": 1, "column": 1})

    def test_peek_token_middle_position(self):
        """Test peeking at a token in the middle of the list."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
                {"type": "OPERATOR", "value": ">", "line": 1, "column": 9},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7})

    def test_peek_token_last_position(self):
        """Test peeking at the last token (pos=len(tokens)-1)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
                {"type": "OPERATOR", "value": ">", "line": 1, "column": 9},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "OPERATOR", "value": ">", "line": 1, "column": 9})

    def test_peek_token_at_end_returns_none(self):
        """Test peeking when pos equals len(tokens), should return None."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_beyond_end_returns_none(self):
        """Test peeking when pos > len(tokens), should return None."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Test peeking when tokens list is empty, should return None."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_does_not_modify_state(self):
        """Test that _peek_token is read-only and doesn't modify parser_state."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        # Create a copy to compare
        import copy
        original_state = copy.deepcopy(parser_state)
        
        _peek_token(parser_state)
        
        # State should remain unchanged
        self.assertEqual(parser_state, original_state)

    def test_peek_token_missing_pos_key_raises_keyerror(self):
        """Test that missing 'pos' key raises KeyError."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "error": ""
        }
        with self.assertRaises(KeyError):
            _peek_token(parser_state)

    def test_peek_token_missing_tokens_key_raises_keyerror(self):
        """Test that missing 'tokens' key raises KeyError."""
        parser_state: Dict[str, Any] = {
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        with self.assertRaises(KeyError):
            _peek_token(parser_state)

    def test_peek_token_single_token(self):
        """Test peeking with a single token in the list."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 5, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "42", "line": 5, "column": 10})


if __name__ == "__main__":
    unittest.main()
