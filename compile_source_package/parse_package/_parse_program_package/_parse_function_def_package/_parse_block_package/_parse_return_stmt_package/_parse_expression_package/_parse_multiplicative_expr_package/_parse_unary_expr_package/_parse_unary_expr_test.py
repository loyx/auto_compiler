import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """Tests for _parse_unary_expr function"""
    
    def test_parse_plus_unary_operator(self):
        """Test parsing unary plus operator"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_minus_unary_operator(self):
        """Test parsing unary minus operator"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": "5",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_not_unary_operator(self):
        """Test parsing NOT unary operator"""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_nested_unary_operators(self):
        """Test parsing nested unary operators (e.g., --x)"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary_expr(parser_state)
            
            # Outer UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Inner UNARY_OP (child)
            inner_op = result["children"][0]
            self.assertEqual(inner_op["type"], "UNARY_OP")
            self.assertEqual(inner_op["value"], "-")
            self.assertEqual(inner_op["line"], 1)
            self.assertEqual(inner_op["column"], 2)
            
            # Identifier (grandchild)
            self.assertEqual(inner_op["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_no_unary_operator_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary_expr"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_primary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = expected_primary_result
            
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_primary_result)
            self.assertEqual(parser_state["pos"], 0)  # pos should not change
    
    def test_parse_empty_tokens_raises_error(self):
        """Test that empty tokens list raises SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_parse_pos_at_end_raises_error(self):
        """Test that pos at end of tokens raises SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,  # pos at end
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_parse_unary_with_literal_operand(self):
        """Test unary operator with literal operand"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": "42",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(result["children"][0]["value"], "42")


if __name__ == "__main__":
    unittest.main()
