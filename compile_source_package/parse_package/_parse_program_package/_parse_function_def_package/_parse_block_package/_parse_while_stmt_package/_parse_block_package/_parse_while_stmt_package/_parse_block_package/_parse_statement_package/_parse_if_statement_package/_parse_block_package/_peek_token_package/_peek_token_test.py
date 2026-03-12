"""
Unit tests for _peek_token function.
"""
import unittest

from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_normal_case(self):
        """Test peeking at a token when pos is within range."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "OPERATOR", "value": "=", "line": 1, "column": 3})

    def test_peek_token_first_token(self):
        """Test peeking at the first token (pos=0)."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "KEYWORD", "value": "if", "line": 1, "column": 1})

    def test_peek_token_last_token(self):
        """Test peeking at the last token (pos=len(tokens)-1)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "NUMBER", "value": "1", "line": 1, "column": 5})

    def test_peek_token_eof_pos_equals_length(self):
        """Test peeking when pos equals len(tokens) (EOF)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_eof_pos_exceeds_length(self):
        """Test peeking when pos exceeds len(tokens) (EOF)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_empty_tokens(self):
        """Test peeking when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Test peeking when 'tokens' key is missing from parser_state."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Test peeking when 'pos' key is missing (should default to 0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "error": None,
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})

    def test_peek_token_no_mutation(self):
        """Test that _peek_token does not modify parser_state."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        
        # Store original state
        original_pos = parser_state["pos"]
        original_tokens = parser_state["tokens"].copy()
        
        # Call function
        _peek_token(parser_state)
        
        # Verify no mutation
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_peek_token_multiple_calls_same_result(self):
        """Test that multiple calls return the same token without advancing."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        
        result1 = _peek_token(parser_state)
        result2 = _peek_token(parser_state)
        result3 = _peek_token(parser_state)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()
