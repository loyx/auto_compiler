import unittest
from unittest.mock import patch

from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """Test cases for _parse_unary_expr function."""
    
    def test_unary_minus_with_number(self):
        """Test parsing unary minus operator (-) with a number literal."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_operand = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 2
        }
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=mock_operand):
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_operand)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_unary_logical_not_with_identifier(self):
        """Test parsing logical NOT operator (!) with an identifier."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "!", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_operand = {
            "type": "IDENTIFIER",
            "value": "flag",
            "line": 2,
            "column": 6
        }
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=mock_operand):
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_operand)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_unary_bitwise_not(self):
        """Test parsing bitwise NOT operator (~)."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "~", "line": 3, "column": 10},
                {"type": "NUMBER", "value": "0", "line": 3, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_operand = {
            "type": "NUMBER",
            "value": "0",
            "line": 3,
            "column": 11
        }
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=mock_operand):
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "~")
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 10)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_operand)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_position_updated_correctly(self):
        """Test that parser_state position is updated after consuming operator."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_operand = {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=mock_operand):
            _parse_unary_expr(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
    
    def test_nested_unary_expressions(self):
        """Test that unary expression can contain another unary expression as operand."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        inner_unary = {
            "type": "UNARY_OP",
            "value": "-",
            "line": 1,
            "column": 2,
            "children": [{"type": "NUMBER", "value": "10", "line": 1, "column": 3}]
        }
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=inner_unary):
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], inner_unary)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_position_not_zero(self):
        """Test parsing when pos is not at the beginning of tokens."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4}
            ],
            "pos": 1,
            "filename": "test.c"
        }
        
        mock_operand = {"type": "NUMBER", "value": "2", "line": 1, "column": 4}
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=mock_operand):
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_complex_primary_expression(self):
        """Test unary operator with complex primary expression (e.g., parenthesized)."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_operand = {
            "type": "PAREN_EXPR",
            "value": None,
            "line": 1,
            "column": 2,
            "children": [
                {"type": "BINARY_OP", "value": "+", "children": [
                    {"type": "NUMBER", "value": "3", "line": 1, "column": 3},
                    {"type": "NUMBER", "value": "4", "line": 1, "column": 5}
                ]}
            ]
        }
        
        with patch('_parse_unary_expr_src._parse_primary', return_value=mock_operand):
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_operand)
            self.assertEqual(parser_state["pos"], 1)


if __name__ == '__main__':
    unittest.main()
