# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.sample_token: Dict[str, Any] = {
            "type": "IDENTIFIER",
            "value": "i",
            "line": 1,
            "column": 0
        }
        self.sample_ast: Dict[str, Any] = {
            "type": "identifier",
            "value": "i",
            "line": 1,
            "column": 0,
            "children": []
        }

    def test_parse_expression_delegates_to_parse_assignment(self) -> None:
        """Test that _parse_expression delegates to _parse_assignment."""
        parser_state: Dict[str, Any] = {
            "tokens": [self.sample_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = self.sample_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_assignment.assert_called_once_with(parser_state)
            self.assertEqual(result, self.sample_ast)

    def test_parse_expression_returns_assignment_result(self) -> None:
        """Test that _parse_expression returns the result from _parse_assignment."""
        parser_state: Dict[str, Any] = {
            "tokens": [self.sample_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        expected_ast: Dict[str, Any] = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "i", "line": 1, "column": 0},
                {"type": "number", "value": "0", "line": 1, "column": 2}
            ],
            "value": None,
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, expected_ast)
            self.assertEqual(result["type"], "assignment")

    def test_parse_expression_with_empty_tokens(self) -> None:
        """Test _parse_expression with empty token list."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        empty_ast: Dict[str, Any] = {
            "type": "empty",
            "value": None,
            "line": 0,
            "column": 0,
            "children": []
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = empty_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_assignment.assert_called_once_with(parser_state)
            self.assertEqual(result, empty_ast)

    def test_parse_expression_with_multiple_tokens(self) -> None:
        """Test _parse_expression with multiple tokens (expression like i < 10)."""
        tokens: list = [
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 4}
        ]
        
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        comparison_ast: Dict[str, Any] = {
            "type": "comparison",
            "children": [
                {"type": "identifier", "value": "i", "line": 1, "column": 0},
                {"type": "operator", "value": "<", "line": 1, "column": 2},
                {"type": "number", "value": "10", "line": 1, "column": 4}
            ],
            "value": None,
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = comparison_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_assignment.assert_called_once_with(parser_state)
            self.assertEqual(result, comparison_ast)
            self.assertEqual(result["type"], "comparison")

    def test_parse_expression_with_assignment_operator(self) -> None:
        """Test _parse_expression with assignment operator (i = 0)."""
        tokens: list = [
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "0", "line": 1, "column": 4}
        ]
        
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        assignment_ast: Dict[str, Any] = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "i", "line": 1, "column": 0},
                {"type": "number", "value": "0", "line": 1, "column": 4}
            ],
            "value": "=",
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = assignment_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, assignment_ast)
            self.assertEqual(result["type"], "assignment")

    def test_parse_expression_with_increment_operator(self) -> None:
        """Test _parse_expression with increment operator (i++)."""
        tokens: list = [
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "++", "line": 1, "column": 1}
        ]
        
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        increment_ast: Dict[str, Any] = {
            "type": "unary_operation",
            "children": [
                {"type": "identifier", "value": "i", "line": 1, "column": 0}
            ],
            "value": "++",
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = increment_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, increment_ast)
            self.assertEqual(result["type"], "unary_operation")

    def test_parse_expression_propagates_exception(self) -> None:
        """Test that _parse_expression propagates exceptions from _parse_assignment."""
        parser_state: Dict[str, Any] = {
            "tokens": [self.sample_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.side_effect = ValueError("Invalid expression")
            
            with self.assertRaises(ValueError) as context:
                _parse_expression(parser_state)
            
            self.assertEqual(str(context.exception), "Invalid expression")

    def test_parse_expression_with_non_zero_position(self) -> None:
        """Test _parse_expression when pos is not at the beginning."""
        tokens: list = [
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 0},
            {"type": "PUNCTUATION", "value": "(", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 3},
            {"type": "OPERATOR", "value": "<", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 7}
        ]
        
        parser_state: Dict[str, Any] = {
            "tokens": tokens,
            "pos": 2,  # Start at the identifier 'i'
            "filename": "test.c"
        }
        
        expected_ast: Dict[str, Any] = {
            "type": "comparison",
            "children": [
                {"type": "identifier", "value": "i", "line": 1, "column": 3},
                {"type": "number", "value": "10", "line": 1, "column": 7}
            ],
            "value": "<",
            "line": 1,
            "column": 3
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_assignment.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_preserves_parser_state_structure(self) -> None:
        """Test that _parse_expression doesn't modify parser_state structure unexpectedly."""
        parser_state: Dict[str, Any] = {
            "tokens": [self.sample_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        original_keys = set(parser_state.keys())
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_if_stmt_package."
            "_parse_block_package._parse_statement_package._parse_for_stmt_package."
            "_parse_expression_package._parse_assignment_package._parse_assignment_src."
            "_parse_assignment"
        ) as mock_parse_assignment:
            mock_parse_assignment.return_value = self.sample_ast
            mock_parse_assignment.side_effect = lambda state: state.update({"pos": 1}) or self.sample_ast
            
            _parse_expression(parser_state)
            
            # Verify keys remain the same (pos may be updated but key should exist)
            self.assertEqual(set(parser_state.keys()), original_keys)


if __name__ == "__main__":
    unittest.main()
