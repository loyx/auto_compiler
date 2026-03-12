# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# Pre-mock _parse_binary to avoid circular import during module loading
# This must be done before importing _parse_expression
_mock_parse_binary = MagicMock()
_mock_parse_binary.__name__ = '_parse_binary'

# Create a mock module for _parse_binary_src
_mock_binary_src = MagicMock()
_mock_binary_src._parse_binary = _mock_parse_binary

# Register the mock module in sys.modules to prevent actual import
_binary_src_module_path = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_binary_package._parse_binary_src'
sys.modules[_binary_src_module_path] = _mock_binary_src

# Relative import from the same package
from ._parse_expression_src import _parse_expression

# Store reference to the mocked function for assertion
_mocked_parse_binary = _mock_parse_binary


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""
    
    def setUp(self):
        """Reset mock before each test and clear side_effect."""
        _mocked_parse_binary.reset_mock()
        _mocked_parse_binary.side_effect = None
        _mocked_parse_binary.return_value = None
    
    def test_parse_expression_delegates_to_parse_binary(self):
        """Test that _parse_expression delegates to _parse_binary with min_precedence=0."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_propagates_syntax_error(self):
        """Test that SyntaxError from _parse_binary is propagated."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "INVALID", "value": "?", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "error.py"
        }
        
        _mocked_parse_binary.side_effect = SyntaxError("Invalid token")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertEqual(str(context.exception), "Invalid token")
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
    
    def test_parse_expression_with_complex_expression(self):
        """Test _parse_expression with a complex expression."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "complex.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "value": "x"},
            "right": {"type": "LITERAL", "value": 5}
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_with_position_offset(self):
        """Test _parse_expression when parser is not at position 0."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "KEYWORD", "value": "let", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 4}
            ],
            "pos": 3,
            "filename": "offset.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "LITERAL",
            "value": 10,
            "line": 1,
            "column": 4
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_with_unary_operator(self):
        """Test _parse_expression with unary operator expression."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 2, "column": 5},
                {"type": "NUMBER", "value": "10", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "unary.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 10}
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_with_parentheses(self):
        """Test _parse_expression with parenthesized expression."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "PAREN", "value": "(", "line": 3, "column": 1},
                {"type": "NUMBER", "value": "1", "line": 3, "column": 2},
                {"type": "OPERATOR", "value": "+", "line": 3, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 3, "column": 4},
                {"type": "PAREN", "value": ")", "line": 3, "column": 5}
            ],
            "pos": 0,
            "filename": "paren.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "empty.py"
        }
        
        _mocked_parse_binary.return_value = {"type": "EMPTY", "value": None}
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, {"type": "EMPTY", "value": None})
    
    def test_parse_expression_with_string_literal(self):
        """Test _parse_expression with string literal."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "STRING", "value": '"hello"', "line": 1, "column": 1}],
            "pos": 0,
            "filename": "string.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "LITERAL",
            "value": "hello",
            "line": 1,
            "column": 1
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_with_boolean_literal(self):
        """Test _parse_expression with boolean literal."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "KEYWORD", "value": "true", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "bool.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "LITERAL",
            "value": True,
            "line": 1,
            "column": 1
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)
    
    def test_parse_expression_with_function_call(self):
        """Test _parse_expression with function call."""
        parser_state: Dict[str, Any] = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
                {"type": "PAREN", "value": "(", "line": 1, "column": 2},
                {"type": "PAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "call.py"
        }
        expected_ast: Dict[str, Any] = {
            "type": "CALL",
            "function": {"type": "IDENTIFIER", "value": "foo"},
            "arguments": []
        }
        
        _mocked_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        _mocked_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)


if __name__ == '__main__':
    unittest.main()
