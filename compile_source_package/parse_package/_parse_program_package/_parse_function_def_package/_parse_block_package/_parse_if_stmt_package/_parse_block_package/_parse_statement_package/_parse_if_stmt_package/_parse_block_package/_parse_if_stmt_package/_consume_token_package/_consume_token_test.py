#!/usr/bin/env python3
"""Unit tests for _consume_token function."""

import unittest

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_success(self):
        """Test successful token consumption when types match."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        token = _consume_token(parser_state, "IF")
        
        self.assertEqual(token["type"], "IF")
        self.assertEqual(token["value"], "if")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_multiple_tokens(self):
        """Test consumption from middle of token list."""
        parser_state = {
            "tokens": [
                {"type": "DEF", "value": "def", "line": 1, "column": 1},
                {"type": "NAME", "value": "foo", "line": 1, "column": 5},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 8}
            ],
            "filename": "test.py",
            "pos": 1
        }
        
        token = _consume_token(parser_state, "NAME")
        
        self.assertEqual(token["type"], "NAME")
        self.assertEqual(token["value"], "foo")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_end_of_input_raises_syntax_error(self):
        """Test SyntaxError when position exceeds token list."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 1
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:1:1", str(context.exception))
    
    def test_empty_tokens_list_raises_syntax_error(self):
        """Test SyntaxError with empty token list."""
        parser_state = {
            "tokens": [],
            "filename": "empty.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ANY")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("empty.py:1:1", str(context.exception))
    
    def test_type_mismatch_raises_syntax_error(self):
        """Test SyntaxError when token type doesn't match expected."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 5, "column": 10}
            ],
            "filename": "error.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "ELSE")
        
        self.assertIn("Expected ELSE, got IF", str(context.exception))
        self.assertIn("error.py:5:10", str(context.exception))
    
    def test_pos_not_modified_on_error(self):
        """Test that pos remains unchanged when error occurs."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        try:
            _consume_token(parser_state, "ELSE")
        except SyntaxError:
            pass
        
        self.assertEqual(parser_state["pos"], 0)
    
    def test_consume_token_at_last_position(self):
        """Test consumption when at the last token position."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "NAME", "value": "x", "line": 1, "column": 4}
            ],
            "filename": "test.py",
            "pos": 1
        }
        
        token = _consume_token(parser_state, "NAME")
        
        self.assertEqual(token["type"], "NAME")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_consume_token_preserves_original_token(self):
        """Test that returned token is the actual token from list."""
        original_token = {"type": "NUMBER", "value": "42", "line": 3, "column": 7}
        parser_state = {
            "tokens": [original_token],
            "filename": "test.py",
            "pos": 0
        }
        
        token = _consume_token(parser_state, "NUMBER")
        
        self.assertIs(token, original_token)


if __name__ == "__main__":
    unittest.main()
