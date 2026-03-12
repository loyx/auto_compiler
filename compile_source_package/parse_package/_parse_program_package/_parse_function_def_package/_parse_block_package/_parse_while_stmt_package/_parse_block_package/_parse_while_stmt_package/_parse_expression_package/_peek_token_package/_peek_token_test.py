# === std / third-party imports ===
import unittest
from copy import deepcopy

# === relative import of target module ===
from ._peek_token_src import _peek_token, ParserState


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""

    def test_peek_token_at_valid_position(self):
        """Happy path: pos is within valid range, returns the token."""
        parser_state: ParserState = {
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

    def test_peek_token_at_first_position(self):
        """Edge case: pos is 0, returns first token."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "KEYWORD", "value": "while", "line": 1, "column": 1})

    def test_peek_token_at_last_valid_position(self):
        """Boundary: pos is at the last valid index."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "a", "line": 1, "column": 1},
                {"type": "IDENT", "value": "b", "line": 1, "column": 3},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENT", "value": "b", "line": 1, "column": 3})

    def test_peek_token_at_end_position(self):
        """Boundary: pos equals len(tokens), returns None."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_beyond_end_position(self):
        """Boundary: pos is beyond len(tokens), returns None."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_empty_tokens_list(self):
        """Edge case: empty tokens list, returns None."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_tokens_key(self):
        """Edge case: missing 'tokens' key, defaults to empty list, returns None."""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """Edge case: missing 'pos' key, defaults to 0."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result, {"type": "IDENT", "value": "x", "line": 1, "column": 1})

    def test_peek_token_does_not_modify_state(self):
        """Verify: parser_state is not modified by the function."""
        original_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        state_copy = deepcopy(original_state)
        
        _peek_token(original_state)
        
        self.assertEqual(original_state, state_copy)

    def test_peek_token_with_complex_token_structure(self):
        """Test with tokens containing additional fields."""
        parser_state: ParserState = {
            "tokens": [
                {
                    "type": "STRING",
                    "value": "hello",
                    "line": 5,
                    "column": 10,
                    "extra_field": "ignored",
                },
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
