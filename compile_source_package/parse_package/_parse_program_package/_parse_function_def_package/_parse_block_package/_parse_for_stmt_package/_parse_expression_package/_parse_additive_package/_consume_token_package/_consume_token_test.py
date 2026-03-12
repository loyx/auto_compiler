"""
Unit tests for _consume_token function.
"""
import unittest

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_first_token(self):
        """Test consuming the first token (pos=0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_middle_token(self):
        """Test consuming a token in the middle of the list."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, {"type": "OPERATOR", "value": "+", "line": 1, "column": 3})
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_last_token(self):
        """Test consuming the last token (boundary case)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_when_pos_equals_length(self):
        """Test when pos equals tokens length (should return None)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)  # pos should not change

    def test_consume_when_pos_beyond_length(self):
        """Test when pos is beyond tokens length (should return None)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 5)  # pos should not change

    def test_consume_from_empty_tokens(self):
        """Test consuming from an empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_with_missing_tokens_key(self):
        """Test when 'tokens' key is missing (should use default [])."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state.get("pos"), 0)

    def test_consume_with_missing_pos_key(self):
        """Test when 'pos' key is missing (should use default 0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_multiple_times(self):
        """Test consuming multiple tokens in sequence."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        token1 = _consume_token(parser_state)
        token2 = _consume_token(parser_state)
        token3 = _consume_token(parser_state)
        token4 = _consume_token(parser_state)
        
        self.assertEqual(token1, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})
        self.assertEqual(token2, {"type": "OPERATOR", "value": "+", "line": 1, "column": 3})
        self.assertEqual(token3, {"type": "NUMBER", "value": "5", "line": 1, "column": 5})
        self.assertIsNone(token4)
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_preserves_parser_state_structure(self):
        """Test that other parser_state fields are preserved."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
        }
        
        _consume_token(parser_state)
        
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertIsNone(parser_state["error"])


if __name__ == "__main__":
    unittest.main()
