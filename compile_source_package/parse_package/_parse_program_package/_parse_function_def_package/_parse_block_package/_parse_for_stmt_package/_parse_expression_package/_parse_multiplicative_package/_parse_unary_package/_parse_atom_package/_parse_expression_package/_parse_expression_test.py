# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Mock the dependency before importing the module under test
import sys

# Create the mock module and function
mock_logical_or_module = MagicMock()
mock_logical_or_func = MagicMock()
mock_logical_or_module._parse_logical_or = mock_logical_or_func

# Register the mock in sys.modules
logical_or_src_path = (
    "main_package.compile_source_package.parse_package._parse_program_package."
    "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
    "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
    "_parse_atom_package._parse_expression_package._parse_logical_or_package."
    "_parse_logical_or_src"
)
logical_or_pkg_path = (
    "main_package.compile_source_package.parse_package._parse_program_package."
    "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
    "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
    "_parse_atom_package._parse_expression_package._parse_logical_or_package"
)

sys.modules[logical_or_src_path] = mock_logical_or_module
sys.modules[logical_or_pkg_path] = mock_logical_or_module

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def setUp(self):
        """Reset mock before each test."""
        mock_logical_or_func.reset_mock()

    def test_parse_expression_delegates_to_logical_or(self):
        """Test that _parse_expression correctly delegates to _parse_logical_or."""
        mock_ast: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "or",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "IDENTIFIER", "value": "b"}
            ],
            "line": 1,
            "column": 0
        }
        
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                {"type": "OR", "value": "or", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_logical_or_func.return_value = mock_ast
        
        result = _parse_expression(parser_state)
        
        mock_logical_or_func.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_ast)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        error_ast: Dict[str, Any] = {
            "type": "ERROR",
            "value": "Unexpected end of input",
            "line": 0,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.return_value = error_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_logical_or.assert_called_once_with(parser_state)
            self.assertEqual(result["type"], "ERROR")

    def test_parse_expression_propagates_error(self):
        """Test that _parse_expression propagates errors from _parse_logical_or."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "INVALID", "value": "!", "line": 1, "column": 0}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        error_ast: Dict[str, Any] = {
            "type": "ERROR",
            "value": "Invalid expression",
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.return_value = error_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_logical_or.assert_called_once_with(parser_state)
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("error", parser_state)

    def test_parse_expression_with_single_literal(self):
        """Test _parse_expression with a single literal value."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        literal_ast: Dict[str, Any] = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.return_value = literal_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_logical_or.assert_called_once_with(parser_state)
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)

    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with a complex expression."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
                {"type": "STAR", "value": "*", "line": 1, "column": 6},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 8}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        complex_ast: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "+",
            "children": [
                {"type": "LITERAL", "value": 1},
                {
                    "type": "BINARY_OP",
                    "operator": "*",
                    "children": [
                        {"type": "LITERAL", "value": 2},
                        {"type": "LITERAL", "value": 3}
                    ]
                }
            ],
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.return_value = complex_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_logical_or.assert_called_once_with(parser_state)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(len(result["children"]), 2)

    def test_parse_expression_updates_position(self):
        """Test that parser_state position is updated after parsing."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        identifier_ast: Dict[str, Any] = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        def mock_logical_or_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return identifier_ast
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.side_effect = mock_logical_or_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(result["type"], "IDENTIFIER")

    def test_parse_expression_with_parenthesized_expression(self):
        """Test _parse_expression with parenthesized expression."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 0},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        paren_ast: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "+",
            "children": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ],
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.return_value = paren_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_logical_or.assert_called_once_with(parser_state)
            self.assertEqual(result["type"], "BINARY_OP")

    def test_parse_expression_preserves_filename(self):
        """Test that filename is preserved in parser_state."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 0}
            ],
            "pos": 0,
            "filename": "source_module.py"
        }
        
        identifier_ast: Dict[str, Any] = {
            "type": "IDENTIFIER",
            "value": "foo",
            "line": 1,
            "column": 0
        }
        
        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package."
            "_parse_function_def_package._parse_block_package._parse_for_stmt_package."
            "_parse_expression_package._parse_multiplicative_package._parse_unary_package."
            "_parse_atom_package._parse_expression_package._parse_logical_or_package."
            "_parse_logical_or_src._parse_logical_or"
        ) as mock_parse_logical_or:
            mock_parse_logical_or.return_value = identifier_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(parser_state["filename"], "source_module.py")
            self.assertEqual(result["type"], "IDENTIFIER")


if __name__ == "__main__":
    unittest.main()
