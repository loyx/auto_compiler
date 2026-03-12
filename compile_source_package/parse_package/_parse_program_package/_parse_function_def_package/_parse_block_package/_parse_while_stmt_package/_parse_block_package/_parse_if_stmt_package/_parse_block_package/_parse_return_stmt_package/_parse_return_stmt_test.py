# -*- coding: utf-8 -*-
"""
Unit tests for _parse_return_stmt function.
Tests parsing of return statements in the compiler.
"""

import unittest
from unittest.mock import patch, call

from ._parse_return_stmt_src import _parse_return_stmt


class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expr')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._consume_token')
    def test_return_with_expression(self, mock_consume_token, mock_parse_expr):
        """Test parsing return statement with expression: return 1;"""
        # Setup mock return values for _consume_token
        mock_consume_token.side_effect = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 8}
        ]
        # Setup mock return value for _parse_expr
        mock_parse_expr.return_value = {"type": "NUMBER", "value": "1", "line": 1, "column": 7}
        
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 7},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 8}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_return_stmt(parser_state)
        
        # Verify AST structure
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NUMBER")
        
        # Verify _consume_token was called correctly
        self.assertEqual(mock_consume_token.call_count, 2)
        mock_consume_token.assert_has_calls([
            call(parser_state, "RETURN"),
            call(parser_state, "SEMICOLON")
        ])
        
        # Verify _parse_expr was called
        mock_parse_expr.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expr')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._consume_token')
    def test_return_without_expression(self, mock_consume_token, mock_parse_expr):
        """Test parsing return statement without expression: return;"""
        # Setup mock return values for _consume_token
        mock_consume_token.side_effect = [
            {"type": "RETURN", "value": "return", "line": 2, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 11}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 2, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_return_stmt(parser_state)
        
        # Verify AST structure
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 1)
        self.assertIsNone(result["children"][0])
        
        # Verify _consume_token was called correctly
        self.assertEqual(mock_consume_token.call_count, 2)
        mock_consume_token.assert_has_calls([
            call(parser_state, "RETURN"),
            call(parser_state, "SEMICOLON")
        ])
        
        # Verify _parse_expr was NOT called
        mock_parse_expr.assert_not_called()

    def test_not_return_token(self):
        """Test error when current token is not RETURN"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Expected RETURN token", str(context.exception))
        self.assertIn("IF", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expr')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._consume_token')
    def test_return_with_complex_expression(self, mock_consume_token, mock_parse_expr):
        """Test parsing return statement with complex expression: return a + b;"""
        # Setup mock return values for _consume_token
        mock_consume_token.side_effect = [
            {"type": "RETURN", "value": "return", "line": 3, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 15}
        ]
        # Setup mock return value for _parse_expr (complex expression AST)
        mock_parse_expr.return_value = {
            "type": "BINARY_OP",
            "operator": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "IDENTIFIER", "value": "b"}
            ],
            "line": 3,
            "column": 8
        }
        
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 3, "column": 1},
                {"type": "IDENTIFIER", "value": "a", "line": 3, "column": 8},
                {"type": "PLUS", "value": "+", "line": 3, "column": 10},
                {"type": "IDENTIFIER", "value": "b", "line": 3, "column": 12},
                {"type": "SEMICOLON", "value": ";", "line": 3, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_return_stmt(parser_state)
        
        # Verify AST structure
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BINARY_OP")
        self.assertEqual(result["children"][0]["operator"], "+")
        
        # Verify _parse_expr was called
        mock_parse_expr.assert_called_once_with(parser_state)


if __name__ == '__main__':
    unittest.main()
