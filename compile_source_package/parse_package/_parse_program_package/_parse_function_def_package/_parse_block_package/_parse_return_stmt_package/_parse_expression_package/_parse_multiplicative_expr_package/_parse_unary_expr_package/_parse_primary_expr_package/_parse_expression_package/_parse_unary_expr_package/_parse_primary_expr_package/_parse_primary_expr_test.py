# === imports ===
from typing import Any, Dict
import unittest
from unittest.mock import patch

# === import UUT ===
from ._parse_primary_expr_src import _parse_primary_expr


# === test code ===
class TestParsePrimaryExpr(unittest.TestCase):
    
    def _create_token(self, token_type: str, value: Any, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def test_parse_identifier(self):
        """Test parsing an identifier."""
        token = self._create_token("IDENTIFIER", "x", 1, 5)
        parser_state = self._create_parser_state([token], 0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_number(self):
        """Test parsing a number literal."""
        token = self._create_token("NUMBER", "42", 2, 10)
        parser_state = self._create_parser_state([token], 0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_string(self):
        """Test parsing a string literal."""
        token = self._create_token("STRING", '"hello"', 3, 15)
        parser_state = self._create_parser_state([token], 0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 15)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_boolean_true(self):
        """Test parsing boolean true."""
        token = self._create_token("KEYWORD", "true", 1, 1)
        parser_state = self._create_parser_state([token], 0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], "true")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_boolean_false(self):
        """Test parsing boolean false."""
        token = self._create_token("KEYWORD", "false", 2, 5)
        parser_state = self._create_parser_state([token], 0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], "false")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_other_keyword_not_boolean(self):
        """Test that non-boolean keywords raise SyntaxError."""
        token = self._create_token("KEYWORD", "if", 1, 1)
        parser_state = self._create_parser_state([token], 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected token", str(context.exception))
    
    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        lparen = self._create_token("LPAREN", "(", 1, 1)
        rparen = self._create_token("RPAREN", ")", 1, 3)
        parser_state = self._create_parser_state([lparen, rparen], 0)
        
        mock_expr_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        
        def mock_parse_expression(state):
            state["pos"] = 1
            return mock_expr_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression) as mock_parse_expr:
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result, mock_expr_ast)
            self.assertEqual(parser_state["pos"], 2)
            mock_parse_expr.assert_called_once()
            self.assertEqual(mock_parse_expr.call_args[0][0], parser_state)
    
    def test_unexpected_end_of_input(self):
        """Test error when input ends unexpectedly."""
        parser_state = self._create_parser_state([], 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_missing_closing_paren(self):
        """Test error when closing parenthesis is missing."""
        lparen = self._create_token("LPAREN", "(", 1, 1)
        parser_state = self._create_parser_state([lparen], 0)
        
        mock_expr_ast = {"type": "IDENTIFIER", "value": "x"}
        
        def mock_parse_expression(state):
            state["pos"] = 1
            return mock_expr_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression):
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))
    
    def test_wrong_closing_token(self):
        """Test error when wrong token closes the parenthesis."""
        lparen = self._create_token("LPAREN", "(", 1, 1)
        wrong_token = self._create_token("IDENTIFIER", "x", 1, 2)
        parser_state = self._create_parser_state([lparen, wrong_token], 0)
        
        mock_expr_ast = {"type": "IDENTIFIER", "value": "x"}
        
        def mock_parse_expression(state):
            state["pos"] = 1
            return mock_expr_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression):
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))
    
    def test_unexpected_token(self):
        """Test error when encountering an unexpected token type."""
        token = self._create_token("OPERATOR", "+", 1, 1)
        parser_state = self._create_parser_state([token], 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected token", str(context.exception))
    
    def test_parse_identifier_preserves_position_info(self):
        """Test that position information is preserved in AST."""
        token = self._create_token("IDENTIFIER", "myVar", 10, 25)
        parser_state = self._create_parser_state([token], 0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)
    
    def test_parse_from_non_zero_position(self):
        """Test parsing from a non-zero position."""
        token1 = self._create_token("OPERATOR", "+", 1, 1)
        token2 = self._create_token("IDENTIFIER", "x", 1, 3)
        parser_state = self._create_parser_state([token1, token2], 1)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
