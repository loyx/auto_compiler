import unittest
from unittest.mock import patch

from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """Test cases for _parse_unary_expr function."""
    
    def test_parse_unary_minus(self):
        """Test parsing unary minus operator."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
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
            self.assertEqual(result["operator"], "-")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_primary.assert_called_once()
    
    def test_parse_unary_not(self):
        """Test parsing logical not operator."""
        tokens = [
            {"type": "KEYWORD", "value": "not", "line": 2, "column": 5},
            {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 9}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 2,
                "column": 9
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_non_unary_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary_expr."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        expected_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = expected_ast
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result, expected_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_primary.assert_called_once_with(parser_state)
    
    def test_nested_unary_operators(self):
        """Test parsing nested unary operators like --x."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        inner_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 3
        }
        
        def primary_side_effect(state):
            if state["pos"] == 2:
                return inner_operand
            return _parse_unary_expr(state)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            
            inner_unary = result["children"][0]
            self.assertEqual(inner_unary["type"], "UNARY_OP")
            self.assertEqual(inner_unary["operator"], "-")
            self.assertEqual(inner_unary["line"], 1)
            self.assertEqual(inner_unary["column"], 2)
            self.assertEqual(len(inner_unary["children"]), 1)
            self.assertEqual(inner_unary["children"][0], inner_operand)
            
            self.assertEqual(parser_state["pos"], 2)
    
    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_position_at_end_raises_syntax_error(self):
        """Test that position at end of tokens raises SyntaxError."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_unary_with_number_literal(self):
        """Test parsing unary minus with number literal."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 3, "column": 10},
            {"type": "NUMBER", "value": "42", "line": 3, "column": 11}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 3,
                "column": 11
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 10)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "NUMBER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_not_not_expression(self):
        """Test parsing double not expression."""
        tokens = [
            {"type": "KEYWORD", "value": "not", "line": 1, "column": 1},
            {"type": "KEYWORD", "value": "not", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 9}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        def primary_side_effect(state):
            if state["pos"] == 2:
                return {
                    "type": "IDENTIFIER",
                    "value": "x",
                    "line": 1,
                    "column": 9
                }
            return _parse_unary_expr(state)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = primary_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["operator"], "not")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 5)
            
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(inner["children"][0]["value"], "x")
            
            self.assertEqual(parser_state["pos"], 2)
    
    def test_other_operator_delegates_to_primary(self):
        """Test that other operators like + delegate to primary."""
        tokens = [
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        expected = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = expected
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 0)
            mock_primary.assert_called_once()
    
    def test_keyword_other_than_not_delegates_to_primary(self):
        """Test that keywords other than 'not' delegate to primary."""
        tokens = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        expected = {
            "type": "KEYWORD",
            "value": "if",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = expected
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result, expected)
            mock_primary.assert_called_once()


if __name__ == "__main__":
    unittest.main()
