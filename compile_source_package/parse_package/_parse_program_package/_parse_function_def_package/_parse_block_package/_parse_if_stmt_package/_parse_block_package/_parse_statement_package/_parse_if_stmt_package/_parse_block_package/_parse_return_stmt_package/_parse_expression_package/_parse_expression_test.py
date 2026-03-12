# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0
        }

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = []
        parser_state["pos"] = 0
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("test.py:0:0: Unexpected end of expression", str(context.exception))

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond token length raises SyntaxError."""
        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = [{"type": "IDENT", "value": "x", "line": 1, "column": 1}]
        parser_state["pos"] = 5  # Beyond token length
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("test.py:0:0: Unexpected end of expression", str(context.exception))

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_simple_expression_no_function_call(self, mock_binary_op, mock_primary):
        """Test parsing simple expression without function call."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary_result = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        mock_primary.return_value = mock_primary_result
        
        mock_binary_result = {"type": "BINARY_OP", "value": "+", "line": 1, "column": 1}
        mock_binary_op.return_value = mock_binary_result
        
        # After _parse_primary, pos should be updated to 1 (past IDENT)
        def update_pos_primary(ps):
            ps["pos"] = 1
            return mock_primary_result
        mock_primary.side_effect = update_pos_primary
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, mock_primary_result, 0)
        self.assertEqual(result, mock_binary_result)
        self.assertEqual(parser_state["pos"], 1)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_function_call')
    def test_function_call_expression(self, mock_function_call, mock_primary):
        """Test parsing function call expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "func", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary_result = {"type": "IDENT", "value": "func", "line": 1, "column": 1}
        mock_primary.return_value = mock_primary_result
        
        mock_call_result = {"type": "CALL", "value": "func", "line": 1, "column": 1}
        mock_function_call.return_value = mock_call_result
        
        # After _parse_primary, pos should be updated to 1 (past IDENT, before LPAREN)
        def update_pos_primary(ps):
            ps["pos"] = 1
            return mock_primary_result
        mock_primary.side_effect = update_pos_primary
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_function_call.assert_called_once_with(parser_state, mock_primary_result)
        self.assertEqual(result, mock_call_result)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_expression_with_binary_op(self, mock_binary_op, mock_primary):
        """Test parsing expression with binary operation."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        mock_primary.return_value = mock_primary_result
        
        mock_binary_result = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [mock_primary_result, {"type": "NUMBER", "value": "3"}],
            "line": 1,
            "column": 1
        }
        mock_binary_op.return_value = mock_binary_result
        
        # After _parse_primary, pos should be updated to 1 (past NUMBER)
        def update_pos_primary(ps):
            ps["pos"] = 1
            return mock_primary_result
        mock_primary.side_effect = update_pos_primary
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, mock_primary_result, 0)
        self.assertEqual(result, mock_binary_result)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_single_literal_expression(self, mock_binary_op, mock_primary):
        """Test parsing single literal expression."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        mock_primary.return_value = mock_primary_result
        
        # After _parse_primary, pos should be updated to 1 (past NUMBER, end of tokens)
        def update_pos_primary(ps):
            ps["pos"] = 1
            return mock_primary_result
        mock_primary.side_effect = update_pos_primary
        
        # _parse_binary_op should return left as-is when no operators
        mock_binary_op.return_value = mock_primary_result
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, mock_primary_result, 0)
        self.assertEqual(result, mock_primary_result)

    @patch('_parse_expression_src._parse_primary')
    def test_unknown_filename_default(self, mock_primary):
        """Test that unknown filename defaults to <unknown>."""
        parser_state = {
            "tokens": [],
            "pos": 0
            # No filename key
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("<unknown>:0:0: Unexpected end of expression", str(context.exception))

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_pos_at_last_token(self, mock_binary_op, mock_primary):
        """Test parsing when pos is at the last token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary_result = {"type": "STRING", "value": "hello", "line": 1, "column": 1}
        mock_primary.return_value = mock_primary_result
        mock_binary_op.return_value = mock_primary_result
        
        def update_pos_primary(ps):
            ps["pos"] = 1
            return mock_primary_result
        mock_primary.side_effect = update_pos_primary
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result, mock_primary_result)
        self.assertEqual(parser_state["pos"], 1)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_function_call')
    @patch('_parse_expression_src._parse_binary_op')
    def test_operator_precedence_flow(self, mock_binary_op, mock_function_call, mock_primary):
        """Test that binary op is called with correct precedence."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "MUL", "value": "*", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary_result = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        mock_primary.return_value = mock_primary_result
        
        def update_pos_primary(ps):
            ps["pos"] = 1
            return mock_primary_result
        mock_primary.side_effect = update_pos_primary
        
        mock_binary_result = {"type": "BINARY_OP", "value": "+", "line": 1, "column": 1}
        mock_binary_op.return_value = mock_binary_result
        
        result = _parse_expression(parser_state)
        
        # Verify _parse_binary_op is called with min_precedence=0
        mock_binary_op.assert_called_once_with(parser_state, mock_primary_result, 0)
        self.assertEqual(result, mock_binary_result)

    @patch('_parse_expression_src._parse_primary')
    def test_primary_propagates_exception(self, mock_primary):
        """Test that exceptions from _parse_primary are propagated."""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "@", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_primary.side_effect = SyntaxError("test.py:1:1: Invalid token")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("test.py:1:1: Invalid token", str(context.exception))
        mock_primary.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()
