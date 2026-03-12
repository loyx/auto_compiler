import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List

# Relative import for the function under test
from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""
    
    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, error: str = None) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py",
            "error": error
        }
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_simple_comparison_gt(self, mock_arith):
        """Test simple greater than comparison: a > b"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "GT", "value": ">", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "a")
        self.assertEqual(result["children"][1]["value"], "b")
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_simple_comparison_eq(self, mock_arith):
        """Test equality comparison: a == b"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "EQ", "value": "==", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_simple_comparison_ne(self, mock_arith):
        """Test not equal comparison: a != b"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "NE", "value": "!=", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "!=")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_simple_comparison_lt(self, mock_arith):
        """Test less than comparison: a < b"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LT", "value": "<", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_simple_comparison_le(self, mock_arith):
        """Test less than or equal comparison: a <= b"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LE", "value": "<=", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<=")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_simple_comparison_ge(self, mock_arith):
        """Test greater than or equal comparison: a >= b"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "GE", "value": ">=", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">=")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_chained_comparison(self, mock_arith):
        """Test chained comparison: a > b > c (left-associative)"""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "GT", "value": ">", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "GT", "value": ">", "line": 1, "column": 7},
            {"type": "IDENT", "value": "c", "line": 1, "column": 9},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "IDENT", "value": "c", "line": 1, "column": 9},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        # Should create nested BINARY_OP: (a > b) > c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(len(result["children"]), 2)
        
        # Left child should be (a > b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], ">")
        self.assertEqual(len(left_child["children"]), 2)
        
        # Right child should be c
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "IDENT")
        self.assertEqual(right_child["value"], "c")
        
        self.assertEqual(parser_state["pos"], 5)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_no_comparison_operator(self, mock_arith):
        """Test expression without comparison operator (just arithmetic)."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
        ]
        
        mock_arith.return_value = {"type": "IDENT", "value": "a", "line": 1, "column": 1}
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        # Should return just the arithmetic expression result
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 1)
        mock_arith.assert_called_once()
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_left_side_error(self, mock_arith):
        """Test when left arithmetic expression returns error."""
        tokens = [
            {"type": "GT", "value": ">", "line": 1, "column": 1},
        ]
        
        error_node = {"type": "ERROR", "value": "Invalid expression", "line": 1, "column": 1}
        mock_arith.return_value = error_node
        
        parser_state = self._create_parser_state(tokens, error="Parse error")
        result = _parse_comparison(parser_state)
        
        # Should return error node immediately
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Invalid expression")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_right_side_error(self, mock_arith):
        """Test when right arithmetic expression returns error."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "GT", "value": ">", "line": 1, "column": 3},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "ERROR", "value": "Invalid right operand", "line": 1, "column": 3},
        ]
        
        parser_state = self._create_parser_state(tokens)
        parser_state["error"] = "Right side parse error"
        result = _parse_comparison(parser_state)
        
        # Should return error node from right side
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Invalid right operand")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_empty_tokens(self, mock_arith):
        """Test with empty tokens list."""
        parser_state = self._create_parser_state([])
        
        mock_arith.return_value = {"type": "ERROR", "value": "No expression", "line": 1, "column": 1}
        
        result = _parse_comparison(parser_state)
        
        # Should handle empty tokens gracefully
        self.assertEqual(result["type"], "ERROR")
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_mixed_comparison_operators(self, mock_arith):
        """Test chained comparison with different operators: a < b == c."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LT", "value": "<", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "EQ", "value": "==", "line": 1, "column": 7},
            {"type": "IDENT", "value": "c", "line": 1, "column": 9},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "IDENT", "value": "c", "line": 1, "column": 9},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        # Should create nested BINARY_OP
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")
        
        # Left should be (a < b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "<")
        
        self.assertEqual(parser_state["pos"], 5)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_comparison_then_non_comparison_token(self, mock_arith):
        """Test comparison followed by non-comparison token stops parsing."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "GT", "value": ">", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "PLUS", "value": "+", "line": 1, "column": 7},
            {"type": "IDENT", "value": "c", "line": 1, "column": 9},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        # Should only parse a > b, stop at PLUS
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_arith_expr_src._parse_arith_expr')
    def test_line_column_preservation(self, mock_arith):
        """Test that line and column information is preserved in AST."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 5, "column": 10},
            {"type": "LE", "value": "<=", "line": 5, "column": 12},
            {"type": "NUMBER", "value": "100", "line": 5, "column": 15},
        ]
        
        mock_arith.side_effect = [
            {"type": "IDENT", "value": "x", "line": 5, "column": 10},
            {"type": "NUMBER", "value": "100", "line": 5, "column": 15},
        ]
        
        parser_state = self._create_parser_state(tokens)
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<=")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
