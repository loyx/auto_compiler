"""Unit tests for _parse_additive_expr function."""

import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_additive_expr_src import _parse_additive_expr, _build_binary_op, _is_current_token, _consume_token


class TestParseAdditiveExpr(unittest.TestCase):
    """Test cases for _parse_additive_expr function."""
    
    def test_single_operand_no_operator(self):
        """Test parsing a single operand with no additive operators."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_operand = {"type": "LITERAL", "value": 5, "line": 1, "column": 1}
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.return_value = mock_operand
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result, mock_operand)
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_simple_addition(self):
        """Test parsing a simple addition expression: a + b"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_operand = {"type": "LITERAL", "value": 5, "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": 3, "line": 1, "column": 5}
        plus_token = {"type": "PLUS", "value": "+", "line": 1, "column": 3}
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.side_effect = [left_operand, right_operand]
            
            with patch('._parse_additive_expr_src._is_current_token') as mock_is_token:
                mock_is_token.side_effect = [True, False]
                
                with patch('._parse_additive_expr_src._consume_token') as mock_consume:
                    mock_consume.return_value = plus_token
                    
                    with patch('._parse_additive_expr_src._build_binary_op') as mock_build:
                        expected_result = {
                            "type": "BINARY_OP",
                            "value": "+",
                            "children": [left_operand, right_operand],
                            "line": 1,
                            "column": 3
                        }
                        mock_build.return_value = expected_result
                        
                        result = _parse_additive_expr(parser_state)
                        
                        self.assertEqual(result, expected_result)
                        self.assertEqual(mock_parse_mult.call_count, 2)
                        mock_build.assert_called_once()
    
    def test_simple_subtraction(self):
        """Test parsing a simple subtraction expression: a - b"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_operand = {"type": "LITERAL", "value": 10, "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": 4, "line": 1, "column": 6}
        minus_token = {"type": "MINUS", "value": "-", "line": 1, "column": 4}
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.side_effect = [left_operand, right_operand]
            
            with patch('._parse_additive_expr_src._is_current_token') as mock_is_token:
                mock_is_token.side_effect = [True, False]
                
                with patch('._parse_additive_expr_src._consume_token') as mock_consume:
                    mock_consume.return_value = minus_token
                    
                    with patch('._parse_additive_expr_src._build_binary_op') as mock_build:
                        expected_result = {
                            "type": "BINARY_OP",
                            "value": "-",
                            "children": [left_operand, right_operand],
                            "line": 1,
                            "column": 4
                        }
                        mock_build.return_value = expected_result
                        
                        result = _parse_additive_expr(parser_state)
                        
                        self.assertEqual(result, expected_result)
    
    def test_left_associativity(self):
        """Test that additive expressions are left-associative: a + b - c = (a + b) - c"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        operand1 = {"type": "LITERAL", "value": 1, "line": 1, "column": 1}
        operand2 = {"type": "LITERAL", "value": 2, "line": 1, "column": 5}
        operand3 = {"type": "LITERAL", "value": 3, "line": 1, "column": 9}
        
        plus_token = {"type": "PLUS", "value": "+", "line": 1, "column": 3}
        minus_token = {"type": "MINUS", "value": "-", "line": 1, "column": 7}
        
        first_binary_op = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [operand1, operand2],
            "line": 1,
            "column": 3
        }
        final_result = {
            "type": "BINARY_OP",
            "value": "-",
            "children": [first_binary_op, operand3],
            "line": 1,
            "column": 7
        }
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.side_effect = [operand1, operand2, operand3]
            
            with patch('._parse_additive_expr_src._is_current_token') as mock_is_token:
                mock_is_token.side_effect = [True, True, False]
                
                with patch('._parse_additive_expr_src._consume_token') as mock_consume:
                    mock_consume.side_effect = [plus_token, minus_token]
                    
                    with patch('._parse_additive_expr_src._build_binary_op') as mock_build:
                        mock_build.side_effect = [first_binary_op, final_result]
                        
                        result = _parse_additive_expr(parser_state)
                        
                        self.assertEqual(result, final_result)
                        self.assertEqual(mock_build.call_count, 2)
    
    def test_multiple_additions(self):
        """Test parsing multiple additions: a + b + c + d"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "PLUS", "value": "+", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "PLUS", "value": "+", "line": 1, "column": 11},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        operands = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        ]
        
        plus_tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "PLUS", "value": "+", "line": 1, "column": 7},
            {"type": "PLUS", "value": "+", "line": 1, "column": 11}
        ]
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.side_effect = operands
            
            with patch('._parse_additive_expr_src._is_current_token') as mock_is_token:
                mock_is_token.side_effect = [True, True, True, False]
                
                with patch('._parse_additive_expr_src._consume_token') as mock_consume:
                    mock_consume.side_effect = plus_tokens
                    
                    with patch('._parse_additive_expr_src._build_binary_op') as mock_build:
                        intermediate1 = {"type": "BINARY_OP", "value": "+", "children": [operands[0], operands[1]]}
                        intermediate2 = {"type": "BINARY_OP", "value": "+", "children": [intermediate1, operands[2]]}
                        final_result = {"type": "BINARY_OP", "value": "+", "children": [intermediate2, operands[3]]}
                        
                        mock_build.side_effect = [intermediate1, intermediate2, final_result]
                        
                        result = _parse_additive_expr(parser_state)
                        
                        self.assertEqual(result, final_result)
                        self.assertEqual(mock_build.call_count, 3)
    
    def test_mixed_addition_subtraction(self):
        """Test parsing mixed + and - operators: 10 - 5 + 3"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 6},
                {"type": "PLUS", "value": "+", "line": 1, "column": 8},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left = {"type": "LITERAL", "value": 10, "line": 1, "column": 1}
        middle = {"type": "LITERAL", "value": 5, "line": 1, "column": 6}
        right = {"type": "LITERAL", "value": 3, "line": 1, "column": 10}
        
        minus_token = {"type": "MINUS", "value": "-", "line": 1, "column": 4}
        plus_token = {"type": "PLUS", "value": "+", "line": 1, "column": 8}
        
        first_op = {"type": "BINARY_OP", "value": "-", "children": [left, middle]}
        final_result = {"type": "BINARY_OP", "value": "+", "children": [first_op, right]}
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.side_effect = [left, middle, right]
            
            with patch('._parse_additive_expr_src._is_current_token') as mock_is_token:
                mock_is_token.side_effect = [True, True, False]
                
                with patch('._parse_additive_expr_src._consume_token') as mock_consume:
                    mock_consume.side_effect = [minus_token, plus_token]
                    
                    with patch('._parse_additive_expr_src._build_binary_op') as mock_build:
                        mock_build.side_effect = [first_op, final_result]
                        
                        result = _parse_additive_expr(parser_state)
                        
                        self.assertEqual(result, final_result)
    
    def test_empty_tokens(self):
        """Test parsing when there are no tokens."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_operand = {"type": "LITERAL", "value": 0, "line": 0, "column": 0}
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.return_value = mock_operand
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result, mock_operand)
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_position_at_end(self):
        """Test parsing when position is already at the end of tokens."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.txt"
        }
        
        mock_operand = {"type": "LITERAL", "value": 5, "line": 1, "column": 1}
        
        with patch('._parse_additive_expr_src._parse_multiplicative_expr') as mock_parse_mult:
            mock_parse_mult.return_value = mock_operand
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result, mock_operand)
            mock_parse_mult.assert_called_once_with(parser_state)


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions."""
    
    def test_build_binary_op_structure(self):
        """Test that _build_binary_op creates correct AST structure."""
        op_token = {"type": "PLUS", "value": "+", "line": 2, "column": 5}
        left = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 3}
        right = {"type": "LITERAL", "value": 10, "line": 2, "column": 7}
        
        result = _build_binary_op(op_token, left, right)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
    
    def test_build_binary_op_with_minus(self):
        """Test _build_binary_op with minus operator."""
        op_token = {"type": "MINUS", "value": "-", "line": 3, "column": 10}
        left = {"type": "LITERAL", "value": 20, "line": 3, "column": 8}
        right = {"type": "LITERAL", "value": 5, "line": 3, "column": 12}
        
        result = _build_binary_op(op_token, left, right)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["children"], [left, right])
    
    def test_is_current_token_match(self):
        """Test _is_current_token correctly identifies matching token types."""
        parser_state = {
            "tokens": [{"type": "PLUS", "value": "+", "line": 1, "column": 1}],
            "pos": 0
        }
        
        self.assertTrue(_is_current_token(parser_state, ("PLUS", "MINUS")))
        self.assertFalse(_is_current_token(parser_state, ("MULTIPLY", "DIVIDE")))
    
    def test_is_current_token_no_match(self):
        """Test _is_current_token returns False for non-matching token."""
        parser_state = {
            "tokens": [{"type": "MULTIPLY", "value": "*", "line": 1, "column": 1}],
            "pos": 0
        }
        
        self.assertFalse(_is_current_token(parser_state, ("PLUS", "MINUS")))
    
    def test_is_current_token_out_of_bounds(self):
        """Test _is_current_token returns False when position is out of bounds."""
        parser_state = {
            "tokens": [{"type": "PLUS", "value": "+", "line": 1, "column": 1}],
            "pos": 5
        }
        
        self.assertFalse(_is_current_token(parser_state, ("PLUS", "MINUS")))
    
    def test_is_current_token_empty_tokens(self):
        """Test _is_current_token returns False when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        self.assertFalse(_is_current_token(parser_state, ("PLUS", "MINUS")))
    
    def test_consume_token_advances_position(self):
        """Test _consume_token returns current token and advances position."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2}
            ],
            "pos": 0
        }
        
        token = _consume_token(parser_state)
        
        self.assertEqual(token["type"], "PLUS")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_second_token(self):
        """Test _consume_token works for subsequent tokens."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2}
            ],
            "pos": 1
        }
        
        token = _consume_token(parser_state)
        
        self.assertEqual(token["type"], "MINUS")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
