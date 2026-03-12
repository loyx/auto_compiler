import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_and_expression_src import _parse_and_expression


class TestParseAndExpression(unittest.TestCase):
    
    def test_single_equality_expression_no_and_operator(self):
        """Test parsing a single equality expression without && operator."""
        mock_equality_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.return_value = mock_equality_result
            
            result = _parse_and_expression(parser_state)
            
            self.assertEqual(result, mock_equality_result)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_single_and_operator(self):
        """Test parsing expression with single && operator."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        
        def side_effect(*args, **kwargs):
            result = left_operand if call_count[0] == 0 else right_operand
            call_count[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            expected = {
                "type": "BINARY_OP",
                "children": [left_operand, right_operand],
                "value": "&&",
                "line": 1,
                "column": 3
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_multiple_and_operators_left_associative(self):
        """Test parsing multiple && operators (left-associative)."""
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_sequence = [operand_a, operand_b, operand_c]
        call_index = [0]
        
        def side_effect(*args, **kwargs):
            result = call_sequence[call_index[0]]
            call_index[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            inner_and = {
                "type": "BINARY_OP",
                "children": [operand_a, operand_b],
                "value": "&&",
                "line": 1,
                "column": 3
            }
            expected = {
                "type": "BINARY_OP",
                "children": [inner_and, operand_c],
                "value": "&&",
                "line": 1,
                "column": 7
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 5)
    
    def test_and_operator_followed_by_non_and_token(self):
        """Test && followed by a non-&& operator stops parsing."""
        left_operand = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_sequence = [left_operand, right_operand]
        call_index = [0]
        
        def side_effect(*args, **kwargs):
            result = call_sequence[call_index[0]]
            call_index[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.side_effect = side_effect
            
            result = _parse_and_expression(parser_state)
            
            expected = {
                "type": "BINARY_OP",
                "children": [left_operand, right_operand],
                "value": "&&",
                "line": 1,
                "column": 3
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        mock_result = {"type": "EMPTY", "value": None, "line": 0, "column": 0}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.return_value = mock_result
            
            result = _parse_and_expression(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_at_end_of_tokens(self):
        """Test when pos is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c",
            "error": ""
        }
        
        mock_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.return_value = mock_result
            
            result = _parse_and_expression(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_syntax_error_from_equality_expression(self):
        """Test that SyntaxError from _parse_equality_expression is propagated."""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "@", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_equality_expression_package._parse_equality_expression_src._parse_equality_expression') as mock_parse_equality:
            mock_parse_equality.side_effect = SyntaxError("Invalid token")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_and_expression(parser_state)
            
            self.assertEqual(str(context.exception), "Invalid token")


if __name__ == '__main__':
    unittest.main()
