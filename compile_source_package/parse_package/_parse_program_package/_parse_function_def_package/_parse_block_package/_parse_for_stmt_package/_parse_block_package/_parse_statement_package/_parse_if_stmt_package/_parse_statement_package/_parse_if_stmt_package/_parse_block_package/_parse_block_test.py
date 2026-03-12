# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# === UUT import (relative) ===
from ._parse_block_src import _parse_block

# === Test Helpers ===
def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

def make_parser_state(tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }

# === Test Cases ===
class TestParseBlock(unittest.TestCase):
    """Test cases for _parse_block function."""

    def test_empty_block(self):
        """Test parsing an empty block {}."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1),
            make_token("RBRACE", "}", line=1, column=2)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)  # pos should be after RBRACE

    def test_block_with_single_statement(self):
        """Test parsing a block with one statement."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1),
            make_token("IDENT", "x", line=1, column=3),
            make_token("RBRACE", "}", line=1, column=5)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        mock_stmt_ast = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 1, "column": 3}
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = mock_stmt_ast
            mock_parse_stmt.side_effect = lambda state: state.update({"pos": 2}) or mock_stmt_ast
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "EXPR_STMT")
        self.assertEqual(parser_state["pos"], 3)  # pos should be after RBRACE

    def test_block_with_multiple_statements(self):
        """Test parsing a block with multiple statements."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1),
            make_token("IDENT", "x", line=1, column=3),
            make_token("IDENT", "y", line=2, column=1),
            make_token("IDENT", "z", line=3, column=1),
            make_token("RBRACE", "}", line=3, column=3)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        def parse_statement_side_effect(state):
            pos = state["pos"]
            stmt_ast = {
                "type": "EXPR_STMT",
                "children": [],
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"]
            }
            state["pos"] = pos + 1
            return stmt_ast
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = parse_statement_side_effect
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["children"][1]["value"], "y")
        self.assertEqual(result["children"][2]["value"], "z")
        self.assertEqual(parser_state["pos"], 5)  # pos should be after RBRACE

    def test_no_lbrace_raises_syntax_error(self):
        """Test that missing LBRACE raises SyntaxError."""
        tokens = [
            make_token("IDENT", "x", line=1, column=1)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))

    def test_unexpected_end_of_input_no_lbrace(self):
        """Test that empty tokens list raises SyntaxError."""
        tokens = []
        parser_state = make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unexpected_end_of_input_no_rbrace(self):
        """Test that missing RBRACE raises SyntaxError."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1),
            make_token("IDENT", "x", line=1, column=3)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        def parse_statement_side_effect(state):
            pos = state["pos"]
            stmt_ast = {
                "type": "EXPR_STMT",
                "children": [],
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"]
            }
            state["pos"] = pos + 1
            return stmt_ast
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = parse_statement_side_effect
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected '}'", str(context.exception))

    def test_pos_out_of_bounds(self):
        """Test that pos beyond tokens length raises SyntaxError."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1)
        ]
        parser_state = make_parser_state(tokens, pos=5)  # pos out of bounds
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_block_preserves_line_column_info(self):
        """Test that BLOCK AST preserves line and column from LBRACE."""
        tokens = [
            make_token("LBRACE", "{", line=10, column=20),
            make_token("RBRACE", "}", line=15, column=5)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 20)

    def test_parse_statement_called_correctly(self):
        """Test that _parse_statement is called with correct parser_state."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1),
            make_token("IDENT", "x", line=1, column=3),
            make_token("RBRACE", "}", line=1, column=5)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        mock_stmt_ast = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 1, "column": 3}
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = mock_stmt_ast
            mock_parse_stmt.side_effect = lambda state: state.update({"pos": 2}) or mock_stmt_ast
            
            _parse_block(parser_state)
            
            mock_parse_stmt.assert_called_once()
            # Verify parser_state was passed (not a copy)
            call_args = mock_parse_stmt.call_args[0][0]
            self.assertIs(call_args, parser_state)

    def test_block_with_semicolons(self):
        """Test parsing block with statements separated by semicolons."""
        tokens = [
            make_token("LBRACE", "{", line=1, column=1),
            make_token("IDENT", "x", line=1, column=3),
            make_token("SEMICOLON", ";", line=1, column=4),
            make_token("IDENT", "y", line=1, column=6),
            make_token("SEMICOLON", ";", line=1, column=7),
            make_token("RBRACE", "}", line=1, column=9)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        call_count = [0]
        def parse_statement_side_effect(state):
            pos = state["pos"]
            stmt_ast = {
                "type": "EXPR_STMT",
                "children": [],
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"]
            }
            # Skip IDENT and SEMICOLON
            state["pos"] = pos + 2
            call_count[0] += 1
            return stmt_ast
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = parse_statement_side_effect
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(call_count[0], 2)
        self.assertEqual(parser_state["pos"], 6)  # pos should be after RBRACE


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
