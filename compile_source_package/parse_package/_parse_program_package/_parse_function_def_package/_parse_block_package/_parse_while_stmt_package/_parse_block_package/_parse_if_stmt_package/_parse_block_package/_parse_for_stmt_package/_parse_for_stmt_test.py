# -*- coding: utf-8 -*-
"""
Unit tests for _parse_for_stmt function.
Tests parsing of for statement: for 变量 in 表达式 语句块
"""

import unittest
from unittest.mock import patch

from ._parse_for_stmt_src import _parse_for_stmt


class TestParseForStmt(unittest.TestCase):
    """Test cases for _parse_for_stmt function."""

    def test_happy_path_basic_for_loop(self):
        """Test basic for loop parsing with all valid tokens."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 7}
        iterable_ast = {"type": "EXPR", "value": "range(10)", "line": 1, "column": 10}
        body_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 20}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(result["type"], "FOR")
                    self.assertEqual(result["variable"], "i")
                    self.assertEqual(result["iterable"], iterable_ast)
                    self.assertEqual(result["body"], body_ast)
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 1)
                    
                    self.assertEqual(mock_consume.call_count, 3)
                    mock_consume.assert_any_call(parser_state, "FOR")
                    mock_consume.assert_any_call(parser_state, "IDENTIFIER")
                    mock_consume.assert_any_call(parser_state, "IN")
                    mock_parse_expr.assert_called_once_with(parser_state)
                    mock_parse_block.assert_called_once_with(parser_state)

    def test_for_loop_with_complex_variable_name(self):
        """Test for loop with multi-character variable name."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 5, "column": 10}
        var_token = {"type": "IDENTIFIER", "value": "counter", "line": 5, "column": 14}
        in_token = {"type": "IN", "value": "in", "line": 5, "column": 22}
        iterable_ast = {"type": "EXPR", "value": "items"}
        body_ast = {"type": "BLOCK", "children": []}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(result["variable"], "counter")
                    self.assertEqual(result["line"], 5)
                    self.assertEqual(result["column"], 10)

    def test_for_loop_with_nested_expression(self):
        """Test for loop with complex iterable expression."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 7}
        iterable_ast = {
            "type": "EXPR",
            "value": "func(a, b)",
            "children": [
                {"type": "IDENT", "value": "func"},
                {"type": "ARGS", "value": ["a", "b"]}
            ]
        }
        body_ast = {"type": "BLOCK", "children": [{"type": "STMT"}]}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(result["iterable"], iterable_ast)
                    self.assertEqual(result["body"], body_ast)
                    mock_parse_expr.assert_called_once()
                    mock_parse_block.assert_called_once()

    def test_missing_for_token_raises_syntax_error(self):
        """Test that missing FOR token raises SyntaxError."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = SyntaxError("Expected FOR token")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
            
            self.assertIn("FOR", str(context.exception))
            mock_consume.assert_called_once_with(parser_state, "FOR")

    def test_missing_identifier_raises_syntax_error(self):
        """Test that missing IDENTIFIER token raises SyntaxError."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt"):
                with patch("._parse_block_package._parse_block_src._parse_block"):
                    mock_consume.side_effect = [for_token, SyntaxError("Expected IDENTIFIER token")]
                    
                    with self.assertRaises(SyntaxError) as context:
                        _parse_for_stmt(parser_state)
                    
                    self.assertIn("IDENTIFIER", str(context.exception))
                    self.assertEqual(mock_consume.call_count, 2)

    def test_missing_in_token_raises_syntax_error(self):
        """Test that missing IN token raises SyntaxError."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt"):
                with patch("._parse_block_package._parse_block_src._parse_block"):
                    mock_consume.side_effect = [for_token, var_token, SyntaxError("Expected IN token")]
                    
                    with self.assertRaises(SyntaxError) as context:
                        _parse_for_stmt(parser_state)
                    
                    self.assertIn("IN", str(context.exception))
                    self.assertEqual(mock_consume.call_count, 3)

    def test_parse_expr_stmt_error_propagates(self):
        """Test that _parse_expr_stmt errors propagate correctly."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 7}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.side_effect = SyntaxError("Invalid expression")
                    
                    with self.assertRaises(SyntaxError) as context:
                        _parse_for_stmt(parser_state)
                    
                    self.assertEqual(str(context.exception), "Invalid expression")
                    mock_parse_expr.assert_called_once_with(parser_state)
                    mock_parse_block.assert_not_called()

    def test_parse_block_error_propagates(self):
        """Test that _parse_block errors propagate correctly."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 7}
        iterable_ast = {"type": "EXPR", "value": "range(10)"}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.side_effect = SyntaxError("Invalid block")
                    
                    with self.assertRaises(SyntaxError) as context:
                        _parse_for_stmt(parser_state)
                    
                    self.assertEqual(str(context.exception), "Invalid block")
                    mock_parse_block.assert_called_once_with(parser_state)

    def test_parser_state_modified_in_place(self):
        """Test that parser_state is modified in place during parsing."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        original_state_id = id(parser_state)
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 7}
        iterable_ast = {"type": "EXPR", "value": "range(10)"}
        body_ast = {"type": "BLOCK", "children": []}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(id(parser_state), original_state_id)
                    self.assertEqual(mock_consume.call_count, 3)
                    for call in mock_consume.call_args_list:
                        self.assertIs(call[0][0], parser_state)

    def test_position_tracking_across_multiple_lines(self):
        """Test for loop spanning multiple lines."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 10, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "item", "line": 10, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 10, "column": 10}
        iterable_ast = {"type": "EXPR", "value": "collection", "line": 10, "column": 13}
        body_ast = {"type": "BLOCK", "children": [], "line": 11, "column": 5}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(result["line"], 10)
                    self.assertEqual(result["column"], 1)
                    self.assertEqual(result["variable"], "item")

    def test_empty_variable_name_handling(self):
        """Test handling of empty variable name from token."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 6}
        iterable_ast = {"type": "EXPR", "value": "x"}
        body_ast = {"type": "BLOCK", "children": []}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(result["variable"], "")
                    self.assertEqual(result["type"], "FOR")

    def test_nested_for_loop_structure(self):
        """Test for loop with nested block structure."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        for_token = {"type": "FOR", "value": "for", "line": 1, "column": 1}
        var_token = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5}
        in_token = {"type": "IN", "value": "in", "line": 1, "column": 7}
        iterable_ast = {"type": "EXPR", "value": "range(5)"}
        body_ast = {
            "type": "BLOCK",
            "children": [
                {
                    "type": "FOR",
                    "variable": "j",
                    "iterable": {"type": "EXPR", "value": "range(3)"},
                    "body": {"type": "BLOCK", "children": []}
                }
            ]
        }
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_consume.side_effect = [for_token, var_token, in_token]
                    mock_parse_expr.return_value = iterable_ast
                    mock_parse_block.return_value = body_ast
                    
                    result = _parse_for_stmt(parser_state)
                    
                    self.assertEqual(result["body"]["type"], "BLOCK")
                    self.assertEqual(len(result["body"]["children"]), 1)
                    self.assertEqual(result["body"]["children"][0]["type"], "FOR")


if __name__ == "__main__":
    unittest.main()
