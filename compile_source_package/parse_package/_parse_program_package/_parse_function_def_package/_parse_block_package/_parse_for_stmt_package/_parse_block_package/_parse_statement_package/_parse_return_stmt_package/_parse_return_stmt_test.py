# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === UUT imports ===
from ._parse_return_stmt_src import _parse_return_stmt


# === Test Helpers ===
def make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


# === Test Cases ===
class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""

    def test_return_without_expression(self):
        """Test return statement without expression: return;"""
        tokens = [
            make_token("RETURN", "return", 1, 1),
            make_token("SEMICOLON", ";", 1, 7)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)  # pos should be after semicolon

    def test_return_with_expression(self):
        """Test return statement with expression: return x;"""
        tokens = [
            make_token("RETURN", "return", 1, 1),
            make_token("IDENTIFIER", "x", 1, 8),
            make_token("SEMICOLON", ";", 1, 9)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 3)  # pos should be after semicolon

    def test_return_with_complex_expression(self):
        """Test return statement with complex expression: return a + b;"""
        tokens = [
            make_token("RETURN", "return", 2, 5),
            make_token("IDENTIFIER", "a", 2, 12),
            make_token("OPERATOR", "+", 2, 14),
            make_token("IDENTIFIER", "b", 2, 16),
            make_token("SEMICOLON", ";", 2, 17)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 5)  # pos should be after semicolon

    def test_missing_return_token(self):
        """Test error when first token is not RETURN."""
        tokens = [
            make_token("IDENTIFIER", "x", 1, 1),
            make_token("SEMICOLON", ";", 1, 2)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Expected RETURN token", str(context.exception))

    def test_unexpected_end_after_return(self):
        """Test error when input ends right after RETURN token."""
        tokens = [
            make_token("RETURN", "return", 1, 1)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Unexpected end of input after 'return'", str(context.exception))

    def test_unexpected_end_before_return(self):
        """Test error when input is empty (pos at end before RETURN)."""
        tokens = []
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Unexpected end of input, expected return statement", str(context.exception))

    def test_missing_semicolon_after_expression(self):
        """Test error when semicolon is missing after return expression."""
        tokens = [
            make_token("RETURN", "return", 1, 1),
            make_token("IDENTIFIER", "x", 1, 8)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Missing semicolon after return expression", str(context.exception))

    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated to after semicolon."""
        tokens = [
            make_token("RETURN", "return", 1, 1),
            make_token("IDENTIFIER", "x", 1, 8),
            make_token("SEMICOLON", ";", 1, 9),
            make_token("IDENTIFIER", "y", 1, 11)  # Extra token to verify pos
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        # pos should point to the token after semicolon (index 3)
        self.assertEqual(parser_state["pos"], 3)
        # Verify we can access the next token
        self.assertEqual(tokens[parser_state["pos"]]["value"], "y")

    def test_line_column_preserved(self):
        """Test that line and column from RETURN token are preserved in AST."""
        tokens = [
            make_token("RETURN", "return", 10, 25),
            make_token("SEMICOLON", ";", 10, 31)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    def test_return_with_number_literal(self):
        """Test return statement with number literal: return 42;"""
        tokens = [
            make_token("RETURN", "return", 1, 1),
            make_token("NUMBER", "42", 1, 8),
            make_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NUMBER")
        self.assertEqual(result["children"][0]["value"], "42")
        self.assertEqual(parser_state["pos"], 3)

    def test_return_with_string_literal(self):
        """Test return statement with string literal: return "hello";"""
        tokens = [
            make_token("RETURN", "return", 1, 1),
            make_token("STRING", '"hello"', 1, 8),
            make_token("SEMICOLON", ";", 1, 16)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "STRING")
        self.assertEqual(parser_state["pos"], 3)

    def test_return_at_end_of_tokens_list(self):
        """Test return statement at the very end of token list."""
        tokens = [
            make_token("IDENTIFIER", "x", 1, 1),
            make_token("RETURN", "return", 1, 3),
            make_token("SEMICOLON", ";", 1, 9)
        ]
        parser_state = make_parser_state(tokens, pos=1)  # Start at RETURN token
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(parser_state["pos"], 3)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
