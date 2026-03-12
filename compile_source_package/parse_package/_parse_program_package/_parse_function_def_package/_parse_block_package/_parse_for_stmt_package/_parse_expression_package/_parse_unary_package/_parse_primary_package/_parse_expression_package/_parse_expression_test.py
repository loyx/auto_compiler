# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_parse_assignment(self):
        """Test that _parse_expression delegates to _parse_assignment."""
        mock_parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_unary_package._parse_primary_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            mock_parse_assignment.assert_called_once_with(mock_parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        mock_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {"type": "ERROR", "value": "Unexpected end of input"}
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_unary_package._parse_primary_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            mock_parse_assignment.assert_called_once()
            self.assertEqual(result["type"], "ERROR")

    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with a complex expression (a + b * c)."""
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "BINARY_OP",
            "op": "+",
            "left": {"type": "IDENTIFIER", "value": "a"},
            "right": {
                "type": "BINARY_OP",
                "op": "*",
                "left": {"type": "IDENTIFIER", "value": "b"},
                "right": {"type": "IDENTIFIER", "value": "c"}
            }
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_unary_package._parse_primary_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(mock_parser_state)
            
            mock_parse_assignment.assert_called_once()
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["op"], "+")

    def test_parse_expression_propagates_error(self):
        """Test that _parse_expression propagates errors from _parse_assignment."""
        mock_parser_state = {
            "tokens": [{"type": "INVALID", "value": "?", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        error_ast = {"type": "ERROR", "value": "Invalid token"}
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_unary_package._parse_primary_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = error_ast
            
            result = _parse_expression(mock_parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Invalid token")

    def test_parse_expression_updates_parser_state(self):
        """Test that _parse_expression updates parser_state through delegation."""
        mock_parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        def side_effect(state):
            state["pos"] = 1
            return {"type": "LITERAL", "value": 42}
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_unary_package._parse_primary_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.side_effect = side_effect
            
            result = _parse_expression(mock_parser_state)
            
            self.assertEqual(mock_parser_state["pos"], 1)
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)


if __name__ == "__main__":
    unittest.main()
