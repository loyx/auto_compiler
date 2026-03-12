import unittest
from unittest.mock import patch
import sys
import os

# Ensure the current package can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """Test cases for _parse_unary_expr function."""
    
    def test_parse_not_operator(self):
        """Test parsing NOT unary operator."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "!")
            self.assertEqual(result["operand"]["type"], "IDENTIFIER")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_minus_operator(self):
        """Test parsing MINUS unary operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "LITERAL", "value": "5", "line": 1, "column": 2}
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"]["type"], "LITERAL")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_nested_unary_operators(self):
        """Test parsing nested unary operators (e.g., --x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            
            result = _parse_unary_expr(parser_state)
            
            # Should create nested UNARY_OP nodes
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"]["type"], "UNARY_OP")
            self.assertEqual(result["operand"]["operator"], "-")
            self.assertEqual(result["operand"]["operand"]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_non_unary_token_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary_expr."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = expected_result
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result, expected_result)
            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)  # pos should not change
    
    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond tokens length raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,  # Beyond tokens length
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_double_not_operator(self):
        """Test parsing double NOT operators (!!)."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "NOT", "value": "!", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            
            result = _parse_unary_expr(parser_state)
            
            # Should create nested UNARY_OP nodes
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "!")
            self.assertEqual(result["operand"]["type"], "UNARY_OP")
            self.assertEqual(result["operand"]["operator"], "!")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_mixed_unary_operators(self):
        """Test parsing mixed unary operators (-!x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NOT", "value": "!", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            
            result = _parse_unary_expr(parser_state)
            
            # Should create nested UNARY_OP nodes
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"]["type"], "UNARY_OP")
            self.assertEqual(result["operand"]["operator"], "!")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_line_and_column_preserved(self):
        """Test that line and column information is preserved in AST."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 5, "column": 10},
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 14}
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_triple_unary_operators(self):
        """Test parsing triple unary operators (---x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('_parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
            
            result = _parse_unary_expr(parser_state)
            
            # Should create three levels of nested UNARY_OP nodes
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"]["type"], "UNARY_OP")
            self.assertEqual(result["operand"]["operand"]["type"], "UNARY_OP")
            self.assertEqual(result["operand"]["operand"]["operand"]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 4)


if __name__ == '__main__':
    unittest.main()