import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_multiplicative_expr_src import (
    _parse_multiplicative_expr,
    _is_multiplicative_operator,
    _consume_current_token,
    _create_binary_op_node
)


class TestParseMultiplicativeExpr(unittest.TestCase):
    """Tests for _parse_multiplicative_expr function."""
    
    def test_single_unary_expr_no_operator(self):
        """Test when there's no multiplicative operator - should return unary expr as-is."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        unary_result = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.return_value = unary_result
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, unary_result)
            mock_unary.assert_called_once_with(parser_state)
    
    def test_simple_multiplication(self):
        """Test simple multiplication: a * b"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right_operand = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.side_effect = [left_operand, right_operand]
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_simple_division(self):
        """Test simple division: a / b"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "SLASH", "value": "/", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right_operand = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.side_effect = [left_operand, right_operand]
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
    
    def test_chain_multiplication_left_associative(self):
        """Test chain multiplication: a * b * c (should be left-associative: (a * b) * c)"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        operand_a = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        operand_b = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        operand_c = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "c",
            "line": 1,
            "column": 9
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.side_effect = [operand_a, operand_b, operand_c]
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should be left-associative: (a * b) * c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # Left child should be (a * b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            # Right child should be c
            right_child = result["children"][1]
            self.assertEqual(right_child, operand_c)
            
            self.assertEqual(parser_state["pos"], 5)
    
    def test_mixed_operators(self):
        """Test mixed operators: a * b / c"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        operand_a = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        operand_b = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        operand_c = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "c",
            "line": 1,
            "column": 9
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.side_effect = [operand_a, operand_b, operand_c]
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should be left-associative: (a * b) / c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # Left child should be (a * b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            # Right child should be c
            right_child = result["children"][1]
            self.assertEqual(right_child, operand_c)
    
    def test_empty_tokens(self):
        """Test with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        unary_result = {
            "type": "ERROR",
            "children": [],
            "value": None,
            "line": 0,
            "column": 0
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.return_value = unary_result
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, unary_result)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_position_at_end(self):
        """Test when pos is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c"
        }
        
        unary_result = {
            "type": "ERROR",
            "children": [],
            "value": None,
            "line": 0,
            "column": 0
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.return_value = unary_result
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, unary_result)
            self.assertEqual(parser_state["pos"], 1)


class TestIsMultiplicativeOperator(unittest.TestCase):
    """Tests for _is_multiplicative_operator helper function."""
    
    def test_star_operator(self):
        """Test STAR token is recognized as multiplicative operator."""
        parser_state = {
            "tokens": [
                {"type": "STAR", "value": "*", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _is_multiplicative_operator(parser_state)
        self.assertTrue(result)
    
    def test_slash_operator(self):
        """Test SLASH token is recognized as multiplicative operator."""
        parser_state = {
            "tokens": [
                {"type": "SLASH", "value": "/", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _is_multiplicative_operator(parser_state)
        self.assertTrue(result)
    
    def test_non_multiplicative_operator(self):
        """Test non-multiplicative operator is not recognized."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _is_multiplicative_operator(parser_state)
        self.assertFalse(result)
    
    def test_position_at_end(self):
        """Test when pos is at or beyond end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "STAR", "value": "*", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c"
        }
        
        result = _is_multiplicative_operator(parser_state)
        self.assertFalse(result)
    
    def test_empty_tokens(self):
        """Test with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _is_multiplicative_operator(parser_state)
        self.assertFalse(result)
    
    def test_missing_token_type(self):
        """Test token without type field."""
        parser_state = {
            "tokens": [
                {"value": "*", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _is_multiplicative_operator(parser_state)
        self.assertFalse(result)


class TestConsumeCurrentToken(unittest.TestCase):
    """Tests for _consume_current_token helper function."""
    
    def test_consume_token_success(self):
        """Test successfully consuming a token."""
        parser_state = {
            "tokens": [
                {"type": "STAR", "value": "*", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _consume_current_token(parser_state)
        
        self.assertEqual(result["type"], "STAR")
        self.assertEqual(result["value"], "*")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_at_end(self):
        """Test consuming token when at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "STAR", "value": "*", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c"
        }
        
        result = _consume_current_token(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_empty_list(self):
        """Test consuming token from empty list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _consume_current_token(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["pos"], 0)


class TestCreateBinaryOpNode(unittest.TestCase):
    """Tests for _create_binary_op_node helper function."""
    
    def test_create_node(self):
        """Test creating a binary op node."""
        left = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        op_token = {
            "type": "STAR",
            "value": "*",
            "line": 1,
            "column": 3
        }
        
        result = _create_binary_op_node(left, right, "*", op_token)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
    
    def test_create_node_missing_line_column(self):
        """Test creating node when token lacks line/column."""
        left = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        op_token = {
            "type": "STAR",
            "value": "*"
        }
        
        result = _create_binary_op_node(left, right, "*", op_token)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)


if __name__ == "__main__":
    unittest.main()
