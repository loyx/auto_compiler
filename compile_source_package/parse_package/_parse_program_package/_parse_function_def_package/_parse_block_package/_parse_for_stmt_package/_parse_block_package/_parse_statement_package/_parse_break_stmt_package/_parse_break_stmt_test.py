# === imports ===
import unittest
from typing import Any, Dict

# === relative import for UUT ===
from ._parse_break_stmt_src import _parse_break_stmt

# === test helpers ===
def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }

# === test cases ===
class TestParseBreakStmt(unittest.TestCase):
    """Test cases for _parse_break_stmt function."""
    
    def test_happy_path_basic_break(self):
        """Test parsing a basic break statement: break;"""
        tokens = [
            make_token("BREAK", "break", line=1, column=1),
            make_token("SEMICOLON", ";", line=1, column=6)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_break_stmt(parser_state)
        
        # Verify AST node structure
        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        
        # Verify side effect: pos updated to after semicolon
        self.assertEqual(parser_state["pos"], 2)
    
    def test_happy_path_break_with_surrounding_tokens(self):
        """Test parsing break statement when surrounded by other tokens."""
        tokens = [
            make_token("IF", "if", line=1, column=1),
            make_token("BREAK", "break", line=2, column=5),
            make_token("SEMICOLON", ";", line=2, column=10),
            make_token("RBRACE", "}", line=3, column=1)
        ]
        parser_state = make_parser_state(tokens, pos=1)
        
        result = _parse_break_stmt(parser_state)
        
        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        
        # Verify pos updated correctly (should point to RBRACE)
        self.assertEqual(parser_state["pos"], 3)
    
    def test_error_missing_semicolon_eof(self):
        """Test error when semicolon is missing (end of input)."""
        tokens = [
            make_token("BREAK", "break", line=1, column=1)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)
        
        self.assertIn("expected ';'", str(context.exception).lower())
        
        # Verify pos was not updated (error before consuming semicolon)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_error_missing_semicolon_unexpected_token(self):
        """Test error when semicolon is missing (unexpected token instead)."""
        tokens = [
            make_token("BREAK", "break", line=1, column=1),
            make_token("IDENTIFIER", "x", line=1, column=7)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)
        
        self.assertIn("expected ';'", str(context.exception).lower())
        self.assertIn("x", str(context.exception))
    
    def test_error_empty_input(self):
        """Test error when input is empty (no tokens)."""
        tokens = []
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)
        
        self.assertIn("expected 'break'", str(context.exception).lower())
    
    def test_error_wrong_token_type(self):
        """Test error when current token is not BREAK."""
        tokens = [
            make_token("CONTINUE", "continue", line=1, column=1),
            make_token("SEMICOLON", ";", line=1, column=9)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)
        
        self.assertIn("expected break", str(context.exception).lower())
        self.assertIn("CONTINUE", str(context.exception))
    
    def test_break_stmt_preserves_other_state_fields(self):
        """Test that other parser_state fields are preserved."""
        tokens = [
            make_token("BREAK", "break", line=1, column=1),
            make_token("SEMICOLON", ";", line=1, column=6)
        ]
        parser_state = make_parser_state(tokens, pos=0, filename="my_test.src")
        parser_state["error"] = None
        parser_state["custom_field"] = "custom_value"
        
        result = _parse_break_stmt(parser_state)
        
        # Verify other fields are preserved
        self.assertEqual(parser_state["filename"], "my_test.src")
        self.assertIsNone(parser_state["error"])
        self.assertEqual(parser_state["custom_field"], "custom_value")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_break_stmt_different_line_column(self):
        """Test that line and column are correctly captured from token."""
        tokens = [
            make_token("BREAK", "break", line=10, column=25),
            make_token("SEMICOLON", ";", line=10, column=30)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_break_stmt(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)


# === test runner ===
if __name__ == "__main__":
    unittest.main()
