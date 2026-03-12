# -*- coding: utf-8 -*-
"""
Unit tests for _parse_expression function.
Tests expression parsing entry point behavior.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Mock _parse_or before importing _parse_expression_src to avoid import errors
# This is necessary because _parse_or_src has dependencies that may not exist
import sys
from unittest.mock import MagicMock

# Create a mock module for _parse_or to avoid import chain issues
mock_parse_or_module = MagicMock()
mock_parse_or_module._parse_or = MagicMock(return_value={"type": "IDENTIFIER", "value": "mocked"})
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_or_src'] = mock_parse_or_module

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_empty_input_raises_syntax_error(self):
        """Test that empty input (pos >= len(tokens)) raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input in expression", str(context.exception))

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond token list raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,  # pos equals len(tokens)
            "filename": "test.ccp"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input in expression", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or')
    def test_delegates_to_parse_or(self, mock_parse_or: MagicMock):
        """Test that _parse_expression delegates to _parse_or."""
        expected_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        mock_parse_or.return_value = expected_ast
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        result = _parse_expression(parser_state)
        
        mock_parse_or.assert_called_once_with(parser_state)
        self.assertEqual(result, expected_ast)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or')
    def test_returns_ast_from_parse_or(self, mock_parse_or: MagicMock):
        """Test that result from _parse_or is returned."""
        # Test with BINARY_OP node
        binary_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            "right": {"type": "LITERAL", "value": 5, "line": 1, "column": 5},
            "line": 1,
            "column": 1
        }
        mock_parse_or.return_value = binary_ast
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or')
    def test_parse_or_can_modify_parser_state(self, mock_parse_or: MagicMock):
        """Test that _parse_or may modify parser_state (pos update)."""
        def side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 3  # Simulate consuming 3 tokens
            return {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "IDENTIFIER", "value": "a"},
                "right": {"type": "LITERAL", "value": 5}
            }
        
        mock_parse_or.side_effect = side_effect
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        result = _parse_expression(parser_state)
        
        # Verify parser_state was modified
        self.assertEqual(parser_state["pos"], 3)
        self.assertIsNotNone(result)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or')
    def test_with_unary_expression(self, mock_parse_or: MagicMock):
        """Test parsing unary expression (delegated to _parse_or)."""
        unary_ast = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 10, "line": 1, "column": 2},
            "line": 1,
            "column": 1
        }
        mock_parse_or.return_value = unary_ast
        
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "-")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or')
    def test_with_literal_value(self, mock_parse_or: MagicMock):
        """Test parsing literal value (delegated to _parse_or)."""
        literal_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }
        mock_parse_or.return_value = literal_ast
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or')
    def test_with_complex_expression(self, mock_parse_or: MagicMock):
        """Test parsing complex expression with multiple operators."""
        complex_ast = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": {
                "type": "BINARY_OP",
                "operator": "&&",
                "left": {"type": "IDENTIFIER", "value": "a"},
                "right": {"type": "IDENTIFIER", "value": "b"}
            },
            "right": {"type": "IDENTIFIER", "value": "c"},
            "line": 1,
            "column": 1
        }
        mock_parse_or.return_value = complex_ast
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "||")

    def test_parser_state_filename_preserved(self):
        """Test that filename in parser_state is preserved during parsing."""
        expected_filename = "my_module.ccp"
        
        def mock_parse_or_preserve(state: Dict[str, Any]) -> Dict[str, Any]:
            # Verify filename is accessible
            self.assertEqual(state["filename"], expected_filename)
            return {"type": "IDENTIFIER", "value": "test"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or', side_effect=mock_parse_or_preserve):
            parser_state = {
                "tokens": [
                    {"type": "IDENTIFIER", "value": "test", "line": 1, "column": 1}
                ],
                "pos": 0,
                "filename": expected_filename
            }
            
            _parse_expression(parser_state)


if __name__ == "__main__":
    unittest.main()
