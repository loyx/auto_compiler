#!/usr/bin/env python3
"""
Unit tests for _parse_expression function.
Tests the expression parsing entry point that delegates to _parse_logical_or.
"""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_delegates_to_parse_logical_or(self):
        """Test that _parse_expression delegates to _parse_logical_or."""
        mock_parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        
        expected_ast = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            mock_logical_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_returns_ast_node_from_logical_or(self):
        """Test that _parse_expression returns the AST node from _parse_logical_or."""
        mock_parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "42", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "INTEGER", "value": "8", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        expected_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "LITERAL", "children": [], "value": 42, "line": 1, "column": 1},
                {"type": "LITERAL", "children": [], "value": 8, "line": 1, "column": 5}
            ],
            "value": "+",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 2)

    def test_updates_parser_state_pos_via_delegation(self):
        """Test that parser_state pos is updated through delegation."""
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        def side_effect(state):
            state["pos"] = 2  # Simulate consuming tokens
            return {"type": "IDENTIFIER", "children": [], "value": "foo", "line": 1, "column": 1}
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.side_effect = side_effect
            
            result = _parse_expression(mock_parser_state)
            
            self.assertEqual(mock_parser_state["pos"], 2)
            mock_logical_or.assert_called_once_with(mock_parser_state)

    def test_propagates_syntax_error_from_logical_or(self):
        """Test that SyntaxError from _parse_logical_or is propagated."""
        mock_parser_state = {
            "tokens": [{"type": "INVALID", "value": "?", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.side_effect = SyntaxError("test.src:1:1: Invalid token")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expression(mock_parser_state)
            
            self.assertIn("Invalid token", str(context.exception))

    def test_handles_empty_token_list(self):
        """Test behavior with empty token list (delegated to _parse_logical_or)."""
        mock_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }
        
        expected_ast = {"type": "LITERAL", "children": [], "value": None, "line": 0, "column": 0}
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            mock_logical_or.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_handles_complex_expression_via_delegation(self):
        """Test complex expression parsing is delegated correctly."""
        mock_parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2},
                {"type": "OR", "value": "||", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        expected_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "children": [], "value": "a", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "children": [], "value": "b", "line": 1, "column": 7}
            ],
            "value": "||",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(len(result["children"]), 2)

    def test_preserves_parser_state_filename(self):
        """Test that parser_state filename is preserved through delegation."""
        mock_parser_state = {
            "tokens": [{"type": "STRING", "value": "hello", "line": 5, "column": 10}],
            "pos": 0,
            "filename": "/path/to/source.cc"
        }
        
        expected_ast = {"type": "LITERAL", "children": [], "value": "hello", "line": 5, "column": 10}
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = expected_ast
            
            _parse_expression(mock_parser_state)
            
            # Verify the parser_state was passed through (filename should be accessible)
            call_args = mock_logical_or.call_args[0][0]
            self.assertEqual(call_args["filename"], "/path/to/source.cc")

    def test_multiple_calls_independent(self):
        """Test that multiple calls to _parse_expression are independent."""
        parser_state_1 = {
            "tokens": [{"type": "INTEGER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test1.src"
        }
        
        parser_state_2 = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1}],
            "pos": 0,
            "filename": "test2.src"
        }
        
        ast_1 = {"type": "LITERAL", "children": [], "value": 1, "line": 1, "column": 1}
        ast_2 = {"type": "IDENTIFIER", "children": [], "value": "x", "line": 2, "column": 1}
        
        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.side_effect = [ast_1, ast_2]
            
            result_1 = _parse_expression(parser_state_1)
            result_2 = _parse_expression(parser_state_2)
            
            self.assertEqual(mock_logical_or.call_count, 2)
            self.assertEqual(result_1["value"], 1)
            self.assertEqual(result_2["value"], "x")


if __name__ == "__main__":
    unittest.main()
