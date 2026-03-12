# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_return_stmt_src import _parse_return_stmt

# === type aliases ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]
AST = Dict[str, Any]

# === test helpers ===
def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
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
class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""
    
    def test_return_without_expression(self):
        """Test return statement without expression (just 'return;')."""
        tokens = [
            create_token("RETURN", "return", 1, 1),
            create_token("SEMICOLON", ";", 1, 7)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)  # Should consume both RETURN and SEMICOLON
    
    def test_return_with_expression(self):
        """Test return statement with expression (e.g., 'return x + 1;')."""
        tokens = [
            create_token("RETURN", "return", 1, 1),
            create_token("IDENTIFIER", "x", 1, 8),
            create_token("PLUS", "+", 1, 10),
            create_token("LITERAL", "1", 1, 12),
            create_token("SEMICOLON", ";", 1, 13)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_expr_node = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "LITERAL", "value": "1"}
            ],
            "value": "+",
            "line": 1,
            "column": 8
        }
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_node
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 4}) or mock_expr_node
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BINARY_OP")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 5)  # Should consume all tokens including SEMICOLON
    
    def test_return_without_semicolon_before_rbrace(self):
        """Test return statement without semicolon before closing brace."""
        tokens = [
            create_token("RETURN", "return", 1, 1),
            create_token("IDENTIFIER", "x", 1, 8),
            create_token("RBRACE", "}", 1, 9)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_expr_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 8
        }
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_node
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_expr_node
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(parser_state["pos"], 2)  # Should not consume RBRACE
    
    def test_return_at_end_of_file_no_semicolon(self):
        """Test return statement at end of file without semicolon."""
        tokens = [
            create_token("RETURN", "return", 1, 1),
            create_token("IDENTIFIER", "x", 1, 8)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_expr_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 8
        }
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_node
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_expr_node
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_not_at_return_token(self):
        """Test error when parser is not at RETURN token."""
        tokens = [
            create_token("IDENTIFIER", "x", 1, 1),
            create_token("SEMICOLON", ";", 1, 2)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Expected RETURN token", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))
    
    def test_unexpected_end_of_input(self):
        """Test error when tokens list is empty or pos is beyond tokens."""
        tokens = []
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_pos_beyond_tokens_length(self):
        """Test error when pos is beyond tokens length."""
        tokens = [create_token("RETURN", "return", 1, 1)]
        parser_state = create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_return_expression_updates_position(self):
        """Test that parsing expression correctly updates parser position."""
        tokens = [
            create_token("RETURN", "return", 1, 1),
            create_token("IDENTIFIER", "x", 1, 8),
            create_token("PLUS", "+", 1, 10),
            create_token("LITERAL", "1", 1, 12),
            create_token("SEMICOLON", ";", 1, 13)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_expr_node = {
            "type": "BINARY_OP",
            "children": [],
            "value": "+",
            "line": 1,
            "column": 8
        }
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 4  # Expression parsing consumes 3 tokens (IDENTIFIER, PLUS, LITERAL)
            return mock_expr_node
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expr_side_effect
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(parser_state["pos"], 5)  # 4 from expression + 1 for SEMICOLON
    
    def test_return_with_complex_position(self):
        """Test return statement with specific line and column numbers."""
        tokens = [
            create_token("RETURN", "return", 10, 5),
            create_token("SEMICOLON", ";", 10, 11)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_multiple_return_statements_sequential(self):
        """Test parsing multiple return statements sequentially."""
        tokens = [
            create_token("RETURN", "return", 1, 1),
            create_token("SEMICOLON", ";", 1, 7),
            create_token("RETURN", "return", 2, 1),
            create_token("IDENTIFIER", "x", 2, 8),
            create_token("SEMICOLON", ";", 2, 9)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_expr_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 2,
            "column": 8
        }
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_node
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 4}) or mock_expr_node
            
            # Parse first return
            result1 = _parse_return_stmt(parser_state)
            self.assertEqual(result1["type"], "RETURN_STMT")
            self.assertEqual(result1["children"], [])
            self.assertEqual(parser_state["pos"], 2)
            
            # Parse second return
            result2 = _parse_return_stmt(parser_state)
            self.assertEqual(result2["type"], "RETURN_STMT")
            self.assertEqual(len(result2["children"]), 1)
            self.assertEqual(parser_state["pos"], 5)


# === test runner ===
if __name__ == "__main__":
    unittest.main()
