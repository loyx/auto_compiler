# === std / third-party imports ===
import unittest

# === relative imports ===
from ._consume_token_src import _consume_token, Token, ParserState


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_happy_path(self):
        """Test consuming a token when tokens are available."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        token2: Token = {"type": "OP", "value": "+", "line": 1, "column": 3}
        parser_state: ParserState = {
            "tokens": [token1, token2],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertEqual(result, token1)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_second_token(self):
        """Test consuming second token after first was consumed."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        token2: Token = {"type": "OP", "value": "+", "line": 1, "column": 3}
        parser_state: ParserState = {
            "tokens": [token1, token2],
            "pos": 1,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertEqual(result, token2)
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_at_end(self):
        """Test consuming when pos is at end of tokens list."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [token1],
            "pos": 1,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_empty_tokens(self):
        """Test consuming when tokens list is empty."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_beyond_end(self):
        """Test consuming when pos is beyond tokens list length."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [token1],
            "pos": 5,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 5)

    def test_consume_token_negative_pos(self):
        """Test consuming when pos is negative."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [token1],
            "pos": -1,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], -1)

    def test_consume_token_multiple_times(self):
        """Test consuming multiple tokens in sequence."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        token2: Token = {"type": "OP", "value": "+", "line": 1, "column": 3}
        token3: Token = {"type": "NUM", "value": "5", "line": 1, "column": 5}
        parser_state: ParserState = {
            "tokens": [token1, token2, token3],
            "pos": 0,
            "filename": "test.py"
        }

        result1 = _consume_token(parser_state)
        result2 = _consume_token(parser_state)
        result3 = _consume_token(parser_state)
        result4 = _consume_token(parser_state)

        self.assertEqual(result1, token1)
        self.assertEqual(result2, token2)
        self.assertEqual(result3, token3)
        self.assertIsNone(result4)
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_preserves_token_data(self):
        """Test that returned token preserves all data fields."""
        token: Token = {
            "type": "KEYWORD",
            "value": "if",
            "line": 10,
            "column": 5
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "if")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)

    def test_consume_token_missing_tokens_key(self):
        """Test consuming when tokens key is missing from parser_state."""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_missing_pos_key(self):
        """Test consuming when pos key is missing from parser_state."""
        token1: Token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [token1],
            "filename": "test.py"
        }

        result = _consume_token(parser_state)

        self.assertEqual(result, token1)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
