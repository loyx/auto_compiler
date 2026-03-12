import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import for the module under test
from ._parse_or_expr_src import _parse_or_expr


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""
    
    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def test_single_expression_no_or(self):
        """Test parsing a single expression without OR operator."""
        mock_ast = {"type": "LITERAL", "value": 42, "line": 1, "column": 1}
        
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ])
        
        with patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr", return_value=mock_ast) as mock_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_and.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_single_or_operator(self):
        """Test parsing expression with one OR operator."""
        mock_left = {"type": "LITERAL", "value": True, "line": 1, "column": 1}
        mock_right = {"type": "LITERAL", "value": False, "line": 1, "column": 10}
        
        parser_state = self._create_parser_state([
            {"type": "BOOLEAN", "value": "true", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 6},
            {"type": "BOOLEAN", "value": "false", "line": 1, "column": 10}
        ])
        
        call_count = [0]
        def side_effect(ps):
            result = mock_left if call_count[0] == 0 else mock_right
            call_count[0] += 1
            return result
        
        with patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=side_effect) as mock_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "||")
            self.assertEqual(result["left"], mock_left)
            self.assertEqual(result["right"], mock_right)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 6)
            self.assertEqual(mock_and.call_count, 2)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_multiple_or_operators_left_associative(self):
        """Test parsing expression with multiple OR operators (left-associative)."""
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        parser_state = self._create_parser_state([
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "OR", "value": "||", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ])
        
        call_results = [mock_a, mock_b, mock_c]
        call_count = [0]
        def side_effect(ps):
            result = call_results[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=side_effect) as mock_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "||")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            left_child = result["left"]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "||")
            self.assertEqual(left_child["left"], mock_a)
            self.assertEqual(left_child["right"], mock_b)
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 3)
            
            self.assertEqual(result["right"], mock_c)
            self.assertEqual(mock_and.call_count, 3)
            self.assertEqual(parser_state["pos"], 4)
    
    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens raises SyntaxError from _parse_and_expr."""
        parser_state = self._create_parser_state([], pos=0, filename="empty.src")
        
        with patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=SyntaxError("Unexpected end of input in empty.src")):
            with self.assertRaises(SyntaxError) as context:
                _parse_or_expr(parser_state)
            
            self.assertIn("empty.src", str(context.exception))
    
    def test_or_at_end_raises_syntax_error(self):
        """Test that OR operator at end of input raises SyntaxError."""
        parser_state = self._create_parser_state([
            {"type": "BOOLEAN", "value": "true", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 6}
        ])
        
        call_count = [0]
        def side_effect(ps):
            if call_count[0] == 0:
                call_count[0] += 1
                return {"type": "LITERAL", "value": True, "line": 1, "column": 1}
            else:
                raise SyntaxError("Unexpected end of input in test.src")
        
        with patch("projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=side_effect):
            with self.assertRaises(SyntaxError) as context:
                _parse_or_expr(parser_state)
            
            self.assertIn("test.src", str(context.exception))
            self.assertEqual(parser_state["pos"], 1)
    
    def test_position_tracking(self):
        """Test that parser position is correctly updated."""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
            {"type": "OR", "value": "||", "line": 1, "column": 8},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 11}
        ])
        
        call_count = [0]
        def side_effect(ps):
            call_count[0] += 1
            return {"type": "LITERAL", "value": call_count[0], "line": 1, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=side_effect) as mock_and:
            _parse_or_expr(parser_state)
            
            self.assertEqual(parser_state["pos"], 4)
            self.assertEqual(mock_and.call_count, 3)


if __name__ == "__main__":
    unittest.main()
