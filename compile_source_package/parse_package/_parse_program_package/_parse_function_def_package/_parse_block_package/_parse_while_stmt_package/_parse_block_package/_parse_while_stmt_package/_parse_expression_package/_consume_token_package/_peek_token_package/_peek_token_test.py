# === std / third-party imports ===
import unittest
import copy

# === sub function imports ===
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_happy_path(self):
        """Test peeking at token when position is valid."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "OPERATOR", "value": "+", "line": 1, "column": 3})

    def test_peek_token_first_token(self):
        """Test peeking at the first token (pos=0)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 0,
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "KEYWORD", "value": "if", "line": 1, "column": 1})

    def test_peek_token_last_token(self):
        """Test peeking at the last token (pos=len(tokens)-1)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 5},
            ],
            "pos": 2,
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "NUMBER", "value": "10", "line": 1, "column": 5})

    def test_peek_token_pos_out_of_range(self):
        """Test when position is beyond tokens list length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_pos_equal_to_length(self):
        """Test when position equals tokens list length (boundary)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            ],
            "pos": 2,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_negative_pos(self):
        """Test when position is negative."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": -1,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_empty_tokens(self):
        """Test when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_tokens_not_list(self):
        """Test when tokens is not a list."""
        parser_state = {
            "tokens": "not a list",
            "pos": 0,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Test when 'tokens' key is missing from parser_state."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Test when 'pos' key is missing (should default to 0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})

    def test_peek_token_no_side_effects(self):
        """Test that _peek_token does not modify parser_state."""
        original_tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": original_tokens,
            "pos": 0,
        }
        
        # Make a copy to compare later
        state_before = copy.deepcopy(parser_state)
        
        _peek_token(parser_state)
        
        # Verify parser_state was not modified
        self.assertEqual(parser_state, state_before)
        self.assertIs(parser_state["tokens"], original_tokens)

    def test_peek_token_none_pos(self):
        """Test when pos is None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_tokens_none(self):
        """Test when tokens is None."""
        parser_state = {
            "tokens": None,
            "pos": 0,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
