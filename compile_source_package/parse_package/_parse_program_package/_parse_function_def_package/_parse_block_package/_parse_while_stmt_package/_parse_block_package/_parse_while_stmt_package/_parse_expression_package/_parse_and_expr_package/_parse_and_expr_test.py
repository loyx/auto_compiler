import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""
    
    def test_single_comparison_no_and(self):
        """Test parsing a single comparison expression without 'and' operator."""
        mock_comparison_ast = {"type": "COMPARISON", "value": "a > b", "line": 1, "column": 0}
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 5}],
            "pos": 1,
            "filename": "test.py"
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek:
            
            mock_parse_comp.return_value = (mock_comparison_ast, mock_parser_state)
            mock_peek.return_value = None
            
            result_ast, result_state = _parse_and_expr(mock_parser_state)
            
            self.assertEqual(result_ast, mock_comparison_ast)
            mock_parse_comp.assert_called_once_with(mock_parser_state)
            mock_peek.assert_called_once()
    
    def test_one_and_expression(self):
        """Test parsing 'expr and expr' with one AND operator."""
        left_ast = {"type": "COMPARISON", "value": "a > b", "line": 1, "column": 0}
        right_ast = {"type": "COMPARISON", "value": "c < d", "line": 1, "column": 10}
        and_token = {"type": "AND", "value": "and", "line": 1, "column": 5}
        
        initial_state = {"tokens": [and_token], "pos": 0, "filename": "test.py"}
        after_left_state = {"tokens": [and_token], "pos": 0, "filename": "test.py"}
        after_consume_state = {"tokens": [and_token], "pos": 1, "filename": "test.py"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_parse_comp.side_effect = [(left_ast, after_left_state), (right_ast, after_consume_state)]
            mock_peek.side_effect = [and_token, None]
            mock_consume.return_value = (and_token, after_consume_state)
            
            result_ast, result_state = _parse_and_expr(initial_state)
            
            self.assertEqual(result_ast["type"], "BINARY_OP")
            self.assertEqual(result_ast["operator"], "and")
            self.assertEqual(len(result_ast["children"]), 2)
            self.assertEqual(result_ast["children"][0], left_ast)
            self.assertEqual(result_ast["children"][1], right_ast)
            self.assertEqual(result_ast["line"], 1)
            self.assertEqual(result_ast["column"], 0)
            
            self.assertEqual(mock_parse_comp.call_count, 2)
            self.assertEqual(mock_peek.call_count, 2)
            mock_consume.assert_called_once_with(after_left_state, "AND")
    
    def test_multiple_and_left_associative(self):
        """Test parsing 'expr and expr and expr' with left associativity."""
        ast1 = {"type": "COMPARISON", "value": "a", "line": 1, "column": 0}
        ast2 = {"type": "COMPARISON", "value": "b", "line": 1, "column": 5}
        ast3 = {"type": "COMPARISON", "value": "c", "line": 1, "column": 10}
        and_token = {"type": "AND", "value": "and", "line": 1, "column": 3}
        
        state1 = {"tokens": [], "pos": 0, "filename": "test.py"}
        state2 = {"tokens": [], "pos": 1, "filename": "test.py"}
        state3 = {"tokens": [], "pos": 2, "filename": "test.py"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_parse_comp.side_effect = [(ast1, state1), (ast2, state2), (ast3, state3)]
            mock_peek.side_effect = [and_token, and_token, None]
            mock_consume.return_value = (and_token, state2)
            
            result_ast, result_state = _parse_and_expr(state1)
            
            self.assertEqual(result_ast["type"], "BINARY_OP")
            self.assertEqual(result_ast["operator"], "and")
            self.assertEqual(len(result_ast["children"]), 2)
            self.assertEqual(result_ast["children"][0]["type"], "BINARY_OP")
            self.assertEqual(result_ast["children"][0]["children"][0], ast1)
            self.assertEqual(result_ast["children"][0]["children"][1], ast2)
            self.assertEqual(result_ast["children"][1], ast3)
            
            self.assertEqual(mock_parse_comp.call_count, 3)
            self.assertEqual(mock_consume.call_count, 2)
    
    def test_peek_returns_none_ends_loop(self):
        """Test that when _peek_token returns None, the loop terminates."""
        mock_ast = {"type": "COMPARISON", "value": "x", "line": 1, "column": 0}
        mock_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek:
            
            mock_parse_comp.return_value = (mock_ast, mock_state)
            mock_peek.return_value = None
            
            result_ast, result_state = _parse_and_expr(mock_state)
            
            self.assertEqual(result_ast, mock_ast)
            mock_peek.assert_called_once()
    
    def test_peek_returns_non_and_token_ends_loop(self):
        """Test that when _peek_token returns non-AND token, the loop terminates."""
        mock_ast = {"type": "COMPARISON", "value": "x", "line": 1, "column": 0}
        mock_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        other_token = {"type": "OR", "value": "or", "line": 1, "column": 5}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek:
            
            mock_parse_comp.return_value = (mock_ast, mock_state)
            mock_peek.return_value = other_token
            
            result_ast, result_state = _parse_and_expr(mock_state)
            
            self.assertEqual(result_ast, mock_ast)
            mock_peek.assert_called_once()
    
    def test_preserves_line_column_from_left_ast(self):
        """Test that BINARY_OP node preserves line/column from left AST."""
        left_ast = {"type": "COMPARISON", "value": "a", "line": 5, "column": 10}
        right_ast = {"type": "COMPARISON", "value": "b", "line": 6, "column": 20}
        and_token = {"type": "AND", "value": "and", "line": 5, "column": 15}
        
        state1 = {"tokens": [], "pos": 0, "filename": "test.py"}
        state2 = {"tokens": [], "pos": 1, "filename": "test.py"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_parse_comp.side_effect = [(left_ast, state1), (right_ast, state2)]
            mock_peek.side_effect = [and_token, None]
            mock_consume.return_value = (and_token, state2)
            
            result_ast, _ = _parse_and_expr(state1)
            
            self.assertEqual(result_ast["line"], 5)
            self.assertEqual(result_ast["column"], 10)
    
    def test_preserves_line_column_from_token_when_left_missing(self):
        """Test that BINARY_OP node uses token line/column when left AST lacks them."""
        left_ast = {"type": "COMPARISON", "value": "a"}
        right_ast = {"type": "COMPARISON", "value": "b"}
        and_token = {"type": "AND", "value": "and", "line": 3, "column": 7}
        
        state1 = {"tokens": [], "pos": 0, "filename": "test.py"}
        state2 = {"tokens": [], "pos": 1, "filename": "test.py"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison') as mock_parse_comp, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_and_expr_package._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_parse_comp.side_effect = [(left_ast, state1), (right_ast, state2)]
            mock_peek.side_effect = [and_token, None]
            mock_consume.return_value = (and_token, state2)
            
            result_ast, _ = _parse_and_expr(state1)
            
            self.assertEqual(result_ast["line"], 3)
            self.assertEqual(result_ast["column"], 7)


if __name__ == "__main__":
    unittest.main()
