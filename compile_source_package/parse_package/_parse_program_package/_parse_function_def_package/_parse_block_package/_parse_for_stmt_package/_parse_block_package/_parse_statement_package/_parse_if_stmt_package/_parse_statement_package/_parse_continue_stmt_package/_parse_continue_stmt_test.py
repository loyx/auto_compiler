# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._parse_continue_stmt_src import _parse_continue_stmt

# === type aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === test helpers ===
def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

def create_parser_state(tokens: list, pos: int = 0, filename: str = "test.c") -> ParserState:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": None
    }

# === test cases ===
class TestParseContinueStmt(unittest.TestCase):
    """Test cases for _parse_continue_stmt function."""
    
    def test_happy_path_basic_continue(self):
        """Test parsing a basic continue statement with CONTINUE and SEMICOLON."""
        tokens = [
            create_token("CONTINUE", "continue", line=5, column=10),
            create_token("SEMICOLON", ";", line=5, column=19)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_continue_stmt(parser_state)
        
        # Verify AST structure
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["value"], "continue")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])
        
        # Verify side effect: pos should be updated to 2 (consumed 2 tokens)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_happy_path_with_surrounding_tokens(self):
        """Test parsing continue statement when there are tokens before and after."""
        tokens = [
            create_token("IF", "if", line=1, column=1),
            create_token("CONTINUE", "continue", line=2, column=5),
            create_token("SEMICOLON", ";", line=2, column=14),
            create_token("RETURN", "return", line=3, column=1)
        ]
        parser_state = create_parser_state(tokens, pos=1)
        
        result = _parse_continue_stmt(parser_state)
        
        # Verify AST structure
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["value"], "continue")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        
        # Verify side effect: pos should be updated to 3 (started at 1, consumed 2 tokens)
        self.assertEqual(parser_state["pos"], 3)
    
    def test_error_missing_semicolon(self):
        """Test that SyntaxError is raised when SEMICOLON is missing."""
        tokens = [
            create_token("CONTINUE", "continue", line=5, column=10)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError):
            _parse_continue_stmt(parser_state)
    
    def test_error_wrong_token_type_at_start(self):
        """Test that SyntaxError is raised when first token is not CONTINUE."""
        tokens = [
            create_token("BREAK", "break", line=5, column=10),
            create_token("SEMICOLON", ";", line=5, column=16)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError):
            _parse_continue_stmt(parser_state)
    
    def test_error_empty_tokens(self):
        """Test that SyntaxError is raised when tokens list is empty."""
        tokens = []
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError):
            _parse_continue_stmt(parser_state)
    
    def test_error_pos_at_end(self):
        """Test that SyntaxError is raised when pos is at end of tokens."""
        tokens = [
            create_token("CONTINUE", "continue", line=5, column=10)
        ]
        parser_state = create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError):
            _parse_continue_stmt(parser_state)
    
    def test_error_wrong_token_after_continue(self):
        """Test that SyntaxError is raised when token after CONTINUE is not SEMICOLON."""
        tokens = [
            create_token("CONTINUE", "continue", line=5, column=10),
            create_token("BREAK", "break", line=5, column=19)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError):
            _parse_continue_stmt(parser_state)
    
    def test_ast_preserves_token_location(self):
        """Test that AST node preserves the line and column from CONTINUE token."""
        tokens = [
            create_token("CONTINUE", "continue", line=100, column=250),
            create_token("SEMICOLON", ";", line=100, column=259)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_continue_stmt(parser_state)
        
        self.assertEqual(result["line"], 100)
        self.assertEqual(result["column"], 250)
    
    def test_pos_update_atomic_on_success(self):
        """Test that pos is only updated when parsing succeeds completely."""
        tokens = [
            create_token("CONTINUE", "continue", line=5, column=10),
            create_token("SEMICOLON", ";", line=5, column=19)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]
        
        result = _parse_continue_stmt(parser_state)
        
        # Should have advanced by exactly 2
        self.assertEqual(parser_state["pos"], original_pos + 2)
    
    def test_multiple_continue_statements_sequential(self):
        """Test parsing multiple continue statements sequentially."""
        tokens = [
            create_token("CONTINUE", "continue", line=1, column=1),
            create_token("SEMICOLON", ";", line=1, column=10),
            create_token("CONTINUE", "continue", line=2, column=1),
            create_token("SEMICOLON", ";", line=2, column=10)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Parse first continue
        result1 = _parse_continue_stmt(parser_state)
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(result1["line"], 1)
        
        # Parse second continue
        result2 = _parse_continue_stmt(parser_state)
        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(result2["line"], 2)


if __name__ == "__main__":
    unittest.main()
