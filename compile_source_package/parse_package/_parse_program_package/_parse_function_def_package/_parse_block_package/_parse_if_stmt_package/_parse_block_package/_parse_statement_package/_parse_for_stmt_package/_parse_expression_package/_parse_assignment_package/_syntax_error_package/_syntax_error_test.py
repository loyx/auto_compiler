# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._syntax_error_src import _syntax_error

# === Test Cases ===
class TestSyntaxError(unittest.TestCase):
    """Test cases for _syntax_error function."""
    
    def test_basic_error_message(self):
        """Test basic error message setting without position info."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": ""
        }
        message = "unexpected token"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "unexpected token")
    
    def test_error_with_filename_no_tokens(self):
        """Test error message with filename but no tokens."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        message = "unexpected token"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "test.py: unexpected token")
    
    def test_error_with_tokens_and_position(self):
        """Test error message enriched with line/column from current token."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 10, "col": 5},
                {"type": "OP", "value": "=", "line": 10, "col": 7}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        message = "expected expression"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "test.py:10:7: expected expression")
    
    def test_error_with_tokens_no_filename(self):
        """Test error message with line/column but no filename."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 5, "col": 3}
            ],
            "pos": 0,
            "filename": ""
        }
        message = "invalid syntax"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "5:3: invalid syntax")
    
    def test_error_token_missing_line_col(self):
        """Test error message when token lacks line/col fields."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENT", "value": "x"}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        message = "unexpected identifier"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "test.py:?:?: unexpected identifier")
    
    def test_error_position_out_of_bounds(self):
        """Test error message when position is beyond tokens list."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "col": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        message = "end of file"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "test.py: end of file")
    
    def test_error_negative_position(self):
        """Test error message when position is negative."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "col": 1}
            ],
            "pos": -1,
            "filename": "test.py"
        }
        message = "invalid position"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "test.py: invalid position")
    
    def test_error_empty_parser_state(self):
        """Test error message with minimal/empty parser_state."""
        parser_state: Dict[str, Any] = {}
        message = "generic error"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "generic error")
    
    def test_error_overwrites_existing_error(self):
        """Test that error field is overwritten with new message."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "",
            "error": "old error"
        }
        message = "new error"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "new error")
    
    def test_error_with_partial_position_info(self):
        """Test error message when token has only line or only col."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 15}
            ],
            "pos": 0,
            "filename": ""
        }
        message = "missing column"
        
        result = _syntax_error(parser_state, message)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "15:?: missing column")


# === Main Entry ===
if __name__ == "__main__":
    unittest.main()
