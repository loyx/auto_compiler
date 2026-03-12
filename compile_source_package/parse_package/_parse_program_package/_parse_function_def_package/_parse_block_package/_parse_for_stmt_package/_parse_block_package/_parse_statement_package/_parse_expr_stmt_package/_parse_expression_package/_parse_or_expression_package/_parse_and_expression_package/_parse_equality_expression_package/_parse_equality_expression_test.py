import unittest
from unittest.mock import patch

from ._parse_equality_expression_src import _parse_equality_expression


class TestParseEqualityExpression(unittest.TestCase):
    """Test cases for _parse_equality_expression function."""
    
    def test_simple_equality_operator(self):
        """Test parsing simple equality expression: a == b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.side_effect = [left_operand, right_operand]
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_simple_inequality_operator(self):
        """Test parsing simple inequality expression: a != b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
            {"type": "OPERATOR", "value": "!=", "line": 2, "column": 7},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 10},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 10}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.side_effect = [left_operand, right_operand]
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "!=")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 7)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_chained_equality_operators(self):
        """Test parsing chained equality expressions: a == b != c (left-associative)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            {"type": "OPERATOR", "value": "!=", "line": 1, "column": 8},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.side_effect = [operand_a, operand_b, operand_c]
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "!=")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)
            self.assertEqual(len(result["children"]), 2)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "==")
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 3)
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            self.assertEqual(result["children"][1], operand_c)
            self.assertEqual(parser_state["pos"], 5)
    
    def test_no_equality_operator(self):
        """Test parsing when there is no equality operator (just relational expression)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        single_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.return_value = single_operand
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result, single_operand)
            self.assertEqual(parser_state["pos"], 1)
            mock_relational.assert_called_once()
    
    def test_empty_tokens_after_relational(self):
        """Test parsing when tokens end immediately after relational expression"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        single_operand = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.return_value = single_operand
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result, single_operand)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_position_at_end_of_tokens(self):
        """Test parsing when position is already at end of tokens"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }
        
        single_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.return_value = single_operand
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result, single_operand)
            self.assertEqual(parser_state["pos"], 1)
            mock_relational.assert_called_once()
    
    def test_multiple_consecutive_equality_operators(self):
        """Test parsing multiple consecutive == operators: a == b == c"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 8},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.side_effect = [operand_a, operand_b, operand_c]
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")
            self.assertEqual(result["column"], 8)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "==")
            self.assertEqual(left_child["column"], 3)
            
            self.assertEqual(parser_state["pos"], 5)
    
    def test_operator_not_equality(self):
        """Test parsing stops at non-equality operator"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        single_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.return_value = single_operand
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result, single_operand)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_complex_ast_operands(self):
        """Test parsing with complex AST nodes as operands"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        complex_left = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "NUMBER", "value": 1, "line": 1, "column": 1},
                {"type": "NUMBER", "value": 2, "line": 1, "column": 3}
            ],
            "line": 1,
            "column": 2
        }
        complex_right = {
            "type": "CALL",
            "value": "func",
            "children": [],
            "line": 1,
            "column": 6
        }
        
        with patch("._parse_relational_expression_package._parse_relational_expression_src._parse_relational_expression") as mock_relational:
            mock_relational.side_effect = [complex_left, complex_right]
            
            result = _parse_equality_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")
            self.assertEqual(result["children"][0], complex_left)
            self.assertEqual(result["children"][1], complex_right)
            self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
