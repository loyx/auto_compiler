import unittest
from typing import Any, Dict
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """Test cases for _peek_token function."""
    
    def test_peek_valid_position_first_token(self):
        """Test peeking at the first token (pos=0)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "while")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
    
    def test_peek_valid_position_middle_token(self):
        """Test peeking at a middle token."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(result["value"], "(")
    
    def test_peek_valid_position_last_token(self):
        """Test peeking at the last token."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
    
    def test_peek_eof_position_equals_length(self):
        """Test peeking when pos equals tokens length (EOF)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
    
    def test_peek_beyond_eof(self):
        """Test peeking when pos is beyond tokens length."""
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
    
    def test_peek_negative_position(self):
        """Test peeking when pos is negative."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": -1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
    
    def test_peek_empty_tokens(self):
        """Test peeking when tokens list is empty."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
    
    def test_peek_missing_tokens_key(self):
        """Test peeking when 'tokens' key is missing."""
        parser_state: Dict[str, Any] = {
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)
    
    def test_peek_missing_pos_key(self):
        """Test peeking when 'pos' key is missing (should default to 0)."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "filename": "test.py",
            "error": ""
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "while")
    
    def test_peek_does_not_modify_state(self):
        """Test that _peek_token does not modify parser_state."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        original_state = parser_state.copy()
        original_tokens = parser_state["tokens"].copy()
        
        _peek_token(parser_state)
        
        self.assertEqual(parser_state, original_state)
        self.assertEqual(parser_state["tokens"], original_tokens)
    
    def test_peek_multiple_calls_same_result(self):
        """Test that multiple peek calls return the same token."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result1 = _peek_token(parser_state)
        result2 = _peek_token(parser_state)
        result3 = _peek_token(parser_state)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertEqual(result1["type"], "KEYWORD")


if __name__ == "__main__":
    unittest.main()
