import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Import the function under test
from ._parse_expression_with_precedence_src import _parse_expression_with_precedence


class TestParseExpressionWithPrecedence(unittest.TestCase):
    """Test cases for _parse_expression_with_precedence function."""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0) -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.txt",
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, 
                         children: List = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dictionary."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_single_operand_no_operators(self, mock_consume, mock_current, mock_primary):
        """Test parsing a single operand with no binary operators."""
        parser_state = self._create_parser_state([])
        operand_ast = self._create_ast_node("IDENTIFIER", "x")
        
        mock_primary.return_value = operand_ast
        mock_current.return_value = None  # No more tokens
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        self.assertEqual(result, operand_ast)
        mock_primary.assert_called_once_with(parser_state)
        mock_current.assert_called_once_with(parser_state)
        mock_consume.assert_not_called()

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_simple_binary_expression(self, mock_consume, mock_current, mock_primary):
        """Test parsing a simple binary expression: a + b."""
        parser_state = self._create_parser_state([])
        
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        right_operand = self._create_ast_node("IDENTIFIER", "b")
        operator_token = self._create_token("OPERATOR", "+", 1, 3)
        
        # Set up call sequence
        mock_primary.side_effect = [left_operand, right_operand]
        mock_current.side_effect = [operator_token, None, None]
        mock_consume.return_value = operator_token
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_precedence_filtering(self, mock_consume, mock_current, mock_primary):
        """Test that operators below min_prec are not consumed."""
        parser_state = self._create_parser_state([])
        
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        operator_token = self._create_token("OPERATOR", "||", 1, 3)  # Precedence 1
        
        mock_primary.return_value = left_operand
        mock_current.return_value = operator_token
        # Don't consume - should exit due to precedence
        
        # With min_prec=5, operator with prec=1 should be ignored
        result = _parse_expression_with_precedence(parser_state, 5)
        
        self.assertEqual(result, left_operand)
        mock_primary.assert_called_once_with(parser_state)
        mock_current.assert_called_once_with(parser_state)
        mock_consume.assert_not_called()

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_non_operator_token(self, mock_consume, mock_current, mock_primary):
        """Test that non-operator tokens stop the loop."""
        parser_state = self._create_parser_state([])
        
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        non_operator_token = self._create_token("SEMICOLON", ";", 1, 3)
        
        mock_primary.return_value = left_operand
        mock_current.return_value = non_operator_token
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        self.assertEqual(result, left_operand)
        mock_primary.assert_called_once_with(parser_state)
        mock_current.assert_called_once_with(parser_state)
        mock_consume.assert_not_called()

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_left_associativity(self, mock_consume, mock_current, mock_primary):
        """Test left-associativity: a + b + c should parse as (a + b) + c."""
        parser_state = self._create_parser_state([])
        
        operand_a = self._create_ast_node("IDENTIFIER", "a")
        operand_b = self._create_ast_node("IDENTIFIER", "b")
        operand_c = self._create_ast_node("IDENTIFIER", "c")
        plus_token_1 = self._create_token("OPERATOR", "+", 1, 3)
        plus_token_2 = self._create_token("OPERATOR", "+", 1, 7)
        
        # Set up primary to return operands in sequence
        mock_primary.side_effect = [operand_a, operand_b, operand_c]
        
        # Set up current_token to return operators in sequence, then None
        mock_current.side_effect = [plus_token_1, plus_token_2, None, None]
        
        mock_consume.return_value = plus_token_1
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        # Should be left-associative: (a + b) + c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        
        # Left child should be (a + b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["line"], 1)
        self.assertEqual(left_child["column"], 3)
        self.assertEqual(left_child["children"][0], operand_a)
        self.assertEqual(left_child["children"][1], operand_b)
        
        # Right child should be c
        right_child = result["children"][1]
        self.assertEqual(right_child, operand_c)

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_operator_precedence_order(self, mock_consume, mock_current, mock_primary):
        """Test that higher precedence operators bind tighter: a + b * c."""
        parser_state = self._create_parser_state([])
        
        operand_a = self._create_ast_node("IDENTIFIER", "a")
        operand_b = self._create_ast_node("IDENTIFIER", "b")
        operand_c = self._create_ast_node("IDENTIFIER", "c")
        plus_token = self._create_token("OPERATOR", "+", 1, 3)
        mult_token = self._create_token("OPERATOR", "*", 1, 7)
        
        # Set up primary to return operands in sequence
        mock_primary.side_effect = [operand_a, operand_b, operand_c]
        
        # First call: returns +, second call (from recursive): returns *, third: None
        mock_current.side_effect = [plus_token, mult_token, None, None]
        
        mock_consume.side_effect = [plus_token, mult_token]
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        # Should parse as: a + (b * c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        
        # Left child should be a
        left_child = result["children"][0]
        self.assertEqual(left_child, operand_a)
        
        # Right child should be (b * c)
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "BINARY_OP")
        self.assertEqual(right_child["value"], "*")
        self.assertEqual(right_child["children"][0], operand_b)
        self.assertEqual(right_child["children"][1], operand_c)

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_mixed_precedence_expression(self, mock_consume, mock_current, mock_primary):
        """Test complex expression with multiple precedence levels: a || b && c + d."""
        parser_state = self._create_parser_state([])
        
        operand_a = self._create_ast_node("IDENTIFIER", "a")
        operand_b = self._create_ast_node("IDENTIFIER", "b")
        operand_c = self._create_ast_node("IDENTIFIER", "c")
        operand_d = self._create_ast_node("IDENTIFIER", "d")
        
        or_token = self._create_token("OPERATOR", "||", 1, 3)   # prec 1
        and_token = self._create_token("OPERATOR", "&&", 1, 7)  # prec 2
        plus_token = self._create_token("OPERATOR", "+", 1, 11) # prec 5
        
        mock_primary.side_effect = [operand_a, operand_b, operand_c, operand_d]
        mock_current.side_effect = [or_token, and_token, plus_token, None, None, None]
        mock_consume.side_effect = [or_token, and_token, plus_token]
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        # Should parse as: a || (b && (c + d))
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["children"][0], operand_a)
        
        # Right side: b && (c + d)
        right_side = result["children"][1]
        self.assertEqual(right_side["type"], "BINARY_OP")
        self.assertEqual(right_side["value"], "&&")
        self.assertEqual(right_side["children"][0], operand_b)
        
        # Inner right: c + d
        inner_right = right_side["children"][1]
        self.assertEqual(inner_right["type"], "BINARY_OP")
        self.assertEqual(inner_right["value"], "+")
        self.assertEqual(inner_right["children"][0], operand_c)
        self.assertEqual(inner_right["children"][1], operand_d)

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_all_binary_operators(self, mock_consume, mock_current, mock_primary):
        """Test all binary operators from the precedence table."""
        operators = ["||", "&&", "|", "^", "&", "==", "!=", "<", ">", "<=", ">=", "+", "-", "*", "/", "%"]
        
        for op in operators:
            with self.subTest(operator=op):
                parser_state = self._create_parser_state([])
                
                left_operand = self._create_ast_node("IDENTIFIER", "a")
                right_operand = self._create_ast_node("IDENTIFIER", "b")
                operator_token = self._create_token("OPERATOR", op, 1, 3)
                
                mock_primary.side_effect = [left_operand, right_operand]
                mock_current.side_effect = [operator_token, None, None]
                mock_consume.return_value = operator_token
                
                result = _parse_expression_with_precedence(parser_state, 0)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], op)
                self.assertEqual(result["children"][0], left_operand)
                self.assertEqual(result["children"][1], right_operand)

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_ast_node_contains_position_info(self, mock_consume, mock_current, mock_primary):
        """Test that the AST node contains line and column information from the operator token."""
        parser_state = self._create_parser_state([])
        
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        right_operand = self._create_ast_node("IDENTIFIER", "b")
        operator_token = self._create_token("OPERATOR", "+", 5, 12)
        
        mock_primary.side_effect = [left_operand, right_operand]
        mock_current.side_effect = [operator_token, None, None]
        mock_consume.return_value = operator_token
        
        result = _parse_expression_with_precedence(parser_state, 0)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)

    @patch('._parse_expression_with_precedence_src._parse_primary')
    @patch('._parse_expression_with_precedence_src._current_token')
    @patch('._parse_expression_with_precedence_src._consume_token')
    def test_recursive_call_with_increased_precedence(self, mock_consume, mock_current, mock_primary):
        """Test that recursive calls use prec + 1 for left-associativity."""
        parser_state = self._create_parser_state([])
        
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        right_operand = self._create_ast_node("IDENTIFIER", "b")
        operator_token = self._create_token("OPERATOR", "+", 1, 3)
        
        mock_primary.side_effect = [left_operand, right_operand]
        mock_current.side_effect = [operator_token, None, None]
        mock_consume.return_value = operator_token
        
        # Track calls to verify precedence parameter
        with patch('._parse_expression_with_precedence_src._parse_expression_with_precedence') as mock_recursive:
            mock_recursive.return_value = right_operand
            
            result = _parse_expression_with_precedence(parser_state, 0)
            
            # Verify recursive call was made with prec + 1
            # The precedence for "+" is 5, so recursive call should use 5 + 1 = 6
            mock_recursive.assert_called_once()
            call_args = mock_recursive.call_args
            self.assertEqual(call_args[0][0], parser_state)
            self.assertEqual(call_args[0][1], 6)  # prec(+) = 5, so 5 + 1 = 6


if __name__ == '__main__':
    unittest.main()
