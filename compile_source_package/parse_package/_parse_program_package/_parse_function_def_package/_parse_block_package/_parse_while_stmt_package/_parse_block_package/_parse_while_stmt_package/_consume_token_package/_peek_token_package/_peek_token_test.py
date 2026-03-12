# === test file for _peek_token ===
import unittest
import copy

# Relative import from the same package
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_first_position(self):
        """Test peeking token when pos is 0 (first token)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "while", "line": 1, "column": 1})

    def test_peek_token_at_middle_position(self):
        """Test peeking token when pos is in the middle of tokens list."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "LPAREN", "value": "(", "line": 1, "column": 7})

    def test_peek_token_at_last_position(self):
        """Test peeking token when pos is at the last valid index."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "LPAREN", "value": "(", "line": 1, "column": 7})

    def test_peek_token_pos_out_of_bounds(self):
        """Test peeking token when pos is beyond tokens list length."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_pos_equals_length(self):
        """Test peeking token when pos equals tokens list length (boundary)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Test peeking token when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_token_single_token(self):
        """Test peeking token with single token in list."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 3, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "42", "line": 3, "column": 5})

    def test_peek_token_missing_tokens_key(self):
        """Test that missing 'tokens' key raises KeyError."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        with self.assertRaises(KeyError):
            _peek_token(parser_state)

    def test_peek_token_missing_pos_key(self):
        """Test that missing 'pos' key raises KeyError."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        with self.assertRaises(KeyError):
            _peek_token(parser_state)

    def test_peek_token_does_not_modify_state(self):
        """Test that _peek_token is a pure read operation."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        # Make a copy to compare
        original_state = copy.deepcopy(parser_state)
        
        _peek_token(parser_state)
        
        # State should remain unchanged
        self.assertEqual(parser_state, original_state)

    def test_peek_token_with_complex_token_structure(self):
        """Test peeking token with additional fields in token structure."""
        parser_state = {
            "tokens": [
                {
                    "type": "STRING",
                    "value": "hello world",
                    "line": 10,
                    "column": 20,
                    "extra_field": "extra_value"
                },
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 20)
        self.assertEqual(result["extra_field"], "extra_value")

    def test_peek_token_negative_pos(self):
        """Test peeking token with negative pos value."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            ],
            "pos": -1,
            "filename": "test.py",
        }
        # Python allows negative indexing, but -1 < len(tokens), so it returns last token
        result = _peek_token(parser_state)
        self.assertEqual(result, {"type": "LPAREN", "value": "(", "line": 1, "column": 7})


if __name__ == "__main__":
    unittest.main()
