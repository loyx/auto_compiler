# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._current_token_src import _current_token

# === type aliases ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]

# === test cases ===
class TestCurrentToken(unittest.TestCase):
    """Test cases for _current_token function."""
    
    def test_current_token_at_first_position(self):
        """Test getting token at position 0 (first token)."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
    
    def test_current_token_at_middle_position(self):
        """Test getting token at a middle position."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
    
    def test_current_token_at_last_position(self):
        """Test getting token at the last valid position (boundary)."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
    
    def test_current_token_beyond_range_returns_eof(self):
        """Test that pos beyond tokens length returns EOF token."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3}
            ],
            "pos": 5,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
    
    def test_current_token_at_exact_length_returns_eof(self):
        """Test that pos equal to tokens length returns EOF token (boundary)."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3}
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
    
    def test_current_token_empty_tokens_returns_eof(self):
        """Test that empty tokens list returns EOF token."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
    
    def test_current_token_does_not_modify_parser_state(self):
        """Test that _current_token does not modify the parser_state (no side effects)."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        # Make a copy to compare
        import copy
        original_state = copy.deepcopy(parser_state)
        
        _current_token(parser_state)
        
        # Verify parser_state was not modified
        self.assertEqual(parser_state, original_state)
    
    def test_current_token_with_complex_token_structure(self):
        """Test with tokens that have additional fields."""
        parser_state: ParserState = {
            "tokens": [
                {
                    "type": "STRING",
                    "value": "hello world",
                    "line": 5,
                    "column": 10,
                    "extra_field": "should_be_preserved"
                }
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        # Verify extra fields are preserved
        self.assertEqual(result.get("extra_field"), "should_be_preserved")


# === test runner ===
if __name__ == "__main__":
    unittest.main()
