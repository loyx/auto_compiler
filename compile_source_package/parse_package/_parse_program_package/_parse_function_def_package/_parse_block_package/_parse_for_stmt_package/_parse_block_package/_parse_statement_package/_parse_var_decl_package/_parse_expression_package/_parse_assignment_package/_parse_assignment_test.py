# -*- coding: utf-8 -*-
"""Unit tests for _parse_assignment function."""

import unittest
from unittest.mock import patch

from ._parse_assignment_src import _parse_assignment


class TestParseAssignment(unittest.TestCase):
    """Test cases for _parse_assignment function."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    @patch('_parse_assignment_package._parse_assignment_src._consume')
    def test_simple_assignment(self, mock_consume, mock_current_token, mock_parse_logical_or):
        """Test simple assignment: x = 5"""
        # Setup: left side is identifier 'x'
        left_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        mock_parse_logical_or.return_value = left_node
        
        # Setup: current token is '=' operator
        equals_token = {
            "type": "OPERATOR",
            "value": "=",
            "line": 1,
            "column": 2
        }
        mock_current_token.return_value = equals_token
        
        # Setup: right side is literal '5'
        right_node = {
            "type": "LITERAL",
            "value": 5,
            "line": 1,
            "column": 4
        }
        # For recursive call, return right_node then None
        mock_parse_logical_or.side_effect = [left_node, right_node]
        
        # Execute
        result = _parse_assignment(self.parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "=")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
        
        # Verify _consume was called with OPERATOR type
        mock_consume.assert_called_once_with(self.parser_state, "OPERATOR")

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    def test_no_assignment_expression_only(self, mock_current_token, mock_parse_logical_or):
        """Test expression without assignment (just returns left side)"""
        # Setup: left side is an expression
        expr_node = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                {"type": "LITERAL", "value": 1, "line": 1, "column": 2}
            ],
            "line": 1,
            "column": 0
        }
        mock_parse_logical_or.return_value = expr_node
        
        # Setup: current token is not '=' (e.g., semicolon or None)
        mock_current_token.return_value = None
        
        # Execute
        result = _parse_assignment(self.parser_state)
        
        # Verify: should return left side unchanged
        self.assertEqual(result, expr_node)
        mock_parse_logical_or.assert_called_once()

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    def test_invalid_assignment_target_literal(self, mock_current_token, mock_parse_logical_or):
        """Test error case: invalid assignment target (literal on left side)"""
        # Setup: left side is a literal (invalid for assignment)
        left_node = {
            "type": "LITERAL",
            "value": 5,
            "line": 1,
            "column": 0
        }
        mock_parse_logical_or.return_value = left_node
        
        # Setup: current token is '=' operator
        equals_token = {
            "type": "OPERATOR",
            "value": "=",
            "line": 1,
            "column": 2
        }
        mock_current_token.return_value = equals_token
        
        # Execute and verify exception
        with self.assertRaises(SyntaxError) as context:
            _parse_assignment(self.parser_state)
        
        self.assertIn("Invalid assignment target", str(context.exception))
        self.assertIn("1", str(context.exception))  # line number

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    def test_invalid_assignment_target_binary_op(self, mock_current_token, mock_parse_logical_or):
        """Test error case: invalid assignment target (binary op on left side)"""
        # Setup: left side is a binary operation (invalid for assignment)
        left_node = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 2}
            ],
            "line": 1,
            "column": 0
        }
        mock_parse_logical_or.return_value = left_node
        
        # Setup: current token is '=' operator
        equals_token = {
            "type": "OPERATOR",
            "value": "=",
            "line": 1,
            "column": 4
        }
        mock_current_token.return_value = equals_token
        
        # Execute and verify exception
        with self.assertRaises(SyntaxError) as context:
            _parse_assignment(self.parser_state)
        
        self.assertIn("Invalid assignment target", str(context.exception))

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    @patch('_parse_assignment_package._parse_assignment_src._consume')
    def test_nested_assignment(self, mock_consume, mock_current_token, mock_parse_logical_or):
        """Test nested assignment: x = y = 5"""
        # Setup tokens for nested assignment
        identifier_x = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        identifier_y = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 1,
            "column": 4
        }
        literal_5 = {
            "type": "LITERAL",
            "value": 5,
            "line": 1,
            "column": 8
        }
        
        # First call returns x, second call (recursive) returns y = 5
        mock_parse_logical_or.side_effect = [identifier_x, identifier_y, literal_5]
        
        # First '=' for x = ..., second '=' for y = ...
        equals_token = {
            "type": "OPERATOR",
            "value": "=",
            "line": 1,
            "column": 2
        }
        mock_current_token.side_effect = [equals_token, equals_token, None]
        
        # Execute
        result = _parse_assignment(self.parser_state)
        
        # Verify: should be x = (y = 5)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["children"][0], identifier_x)
        
        # Right side should be y = 5
        right_side = result["children"][1]
        self.assertEqual(right_side["type"], "BINARY_OP")
        self.assertEqual(right_side["value"], "=")
        self.assertEqual(right_side["children"][0], identifier_y)
        self.assertEqual(right_side["children"][1], literal_5)
        
        # Verify _consume was called twice
        self.assertEqual(mock_consume.call_count, 2)

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    def test_current_token_different_operator(self, mock_current_token, mock_parse_logical_or):
        """Test when current token is a different operator (not '=')"""
        # Setup: left side expression
        left_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        mock_parse_logical_or.return_value = left_node
        
        # Setup: current token is '+' operator (not '=')
        plus_token = {
            "type": "OPERATOR",
            "value": "+",
            "line": 1,
            "column": 2
        }
        mock_current_token.return_value = plus_token
        
        # Execute
        result = _parse_assignment(self.parser_state)
        
        # Verify: should return left side unchanged
        self.assertEqual(result, left_node)

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    def test_current_token_keyword(self, mock_current_token, mock_parse_logical_or):
        """Test when current token is a keyword (not an operator)"""
        # Setup: left side expression
        left_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        mock_parse_logical_or.return_value = left_node
        
        # Setup: current token is a keyword
        keyword_token = {
            "type": "KEYWORD",
            "value": "if",
            "line": 1,
            "column": 2
        }
        mock_current_token.return_value = keyword_token
        
        # Execute
        result = _parse_assignment(self.parser_state)
        
        # Verify: should return left side unchanged
        self.assertEqual(result, left_node)

    @patch('_parse_assignment_package._parse_assignment_src._parse_logical_or')
    @patch('_parse_assignment_package._parse_assignment_src._current_token')
    @patch('_parse_assignment_package._parse_assignment_src._consume')
    def test_assignment_with_call_expression(self, mock_consume, mock_current_token, mock_parse_logical_or):
        """Test assignment with function call on right side: x = foo()"""
        # Setup: left side identifier
        left_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        # Setup: right side call expression
        right_node = {
            "type": "CALL",
            "value": "foo",
            "children": [],
            "line": 1,
            "column": 4
        }
        
        mock_parse_logical_or.side_effect = [left_node, right_node]
        
        # Setup: current token is '='
        equals_token = {
            "type": "OPERATOR",
            "value": "=",
            "line": 1,
            "column": 2
        }
        mock_current_token.return_value = equals_token
        
        # Execute
        result = _parse_assignment(self.parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)


if __name__ == "__main__":
    unittest.main()
