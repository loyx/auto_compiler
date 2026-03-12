# === std / third-party imports ===
import unittest

# === UUT imports ===
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_valid_position_first_token(self):
        """Test peeking at the first token (pos=0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_peek_valid_position_middle_token(self):
        """Test peeking at a middle token."""
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
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "OP")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_peek_valid_position_last_token(self):
        """Test peeking at the last token."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)

    def test_peek_position_out_of_bounds(self):
        """Test peeking when pos equals len(tokens)."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_position_beyond_bounds(self):
        """Test peeking when pos is well beyond tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 100,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_negative_position(self):
        """Test peeking when pos is negative."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": -1,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_empty_tokens_list(self):
        """Test peeking when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_missing_tokens_key(self):
        """Test peeking when tokens key is missing (should default to [])."""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNone(result)

    def test_peek_missing_pos_key(self):
        """Test peeking when pos key is missing (should default to 0)."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")

    def test_peek_does_not_modify_state(self):
        """Test that peeking does not modify the parser_state."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        # Store original state
        original_pos = parser_state["pos"]
        original_tokens_len = len(parser_state["tokens"])
        
        # Peek multiple times
        _peek_token(parser_state)
        _peek_token(parser_state)
        _peek_token(parser_state)
        
        # Verify state is unchanged
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(len(parser_state["tokens"]), original_tokens_len)

    def test_peek_token_with_all_fields(self):
        """Test peeking returns token with all expected fields."""
        parser_state = {
            "tokens": [
                {
                    "type": "KEYWORD",
                    "value": "while",
                    "line": 5,
                    "column": 10,
                },
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNotNone(result)
        self.assertIn("type", result)
        self.assertIn("value", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "while")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_peek_single_token_list(self):
        """Test peeking with a single token in the list."""
        parser_state = {
            "tokens": [
                {"type": "EOF", "value": "", "line": 10, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _peek_token(parser_state)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")


if __name__ == "__main__":
    unittest.main()
