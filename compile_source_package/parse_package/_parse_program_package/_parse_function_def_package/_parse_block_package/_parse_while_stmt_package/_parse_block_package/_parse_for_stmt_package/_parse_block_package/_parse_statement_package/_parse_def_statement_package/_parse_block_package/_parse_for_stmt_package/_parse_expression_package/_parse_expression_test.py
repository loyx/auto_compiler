# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_dict_literal_package._parse_dict_literal_src import _parse_dict_literal
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_empty_token_stream_raises_syntax_error(self):
        """Test that empty tokens stream raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond token length raises SyntaxError."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_array_literal_delegates_to_parse_array_literal(self):
        """Test that LBRACKET token delegates to _parse_array_literal."""
        expected_ast = {
            "type": "array_literal",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
                {"type": "RBRACKET", "value": "]", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_array_literal, 'return_value', expected_ast) as mock_array:
            result = _parse_expression(parser_state)
            
            mock_array.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_dict_literal_delegates_to_parse_dict_literal(self):
        """Test that LBRACE token delegates to _parse_dict_literal."""
        expected_ast = {
            "type": "dict_literal",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_dict_literal, 'return_value', expected_ast) as mock_dict:
            result = _parse_expression(parser_state)
            
            mock_dict.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_primary_expression_delegates_to_parse_primary_then_binary_op(self):
        """Test that non-special tokens delegate to _parse_primary then _parse_binary_op."""
        primary_ast = {
            "type": "identifier",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        final_ast = {
            "type": "binary_op",
            "left": primary_ast,
            "operator": "+",
            "right": {"type": "number", "value": "1"},
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', final_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, final_ast)

    def test_number_literal_without_binary_op(self):
        """Test parsing a simple number literal without binary operations."""
        primary_ast = {
            "type": "number",
            "value": "42",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', primary_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, primary_ast)

    def test_string_literal_without_binary_op(self):
        """Test parsing a simple string literal without binary operations."""
        primary_ast = {
            "type": "string",
            "value": "hello",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', primary_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, primary_ast)

    def test_function_call_without_binary_op(self):
        """Test parsing a function call without binary operations."""
        primary_ast = {
            "type": "function_call",
            "name": "foo",
            "arguments": [],
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', primary_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, primary_ast)

    def test_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        inner_ast = {
            "type": "identifier",
            "value": "x",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', inner_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', inner_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, inner_ast)

    def test_array_literal_at_non_zero_position(self):
        """Test parsing array literal when pos is not at start."""
        expected_ast = {
            "type": "array_literal",
            "children": [
                {"type": "number", "value": "1"},
                {"type": "number", "value": "2"}
            ],
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 2},
                {"type": "LBRACKET", "value": "[", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 6},
                {"type": "COMMA", "value": ",", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 8},
                {"type": "RBRACKET", "value": "]", "line": 1, "column": 9}
            ],
            "pos": 2,
            "filename": "test.py"
        }
        
        with patch.object(_parse_array_literal, 'return_value', expected_ast) as mock_array:
            result = _parse_expression(parser_state)
            
            mock_array.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_dict_literal_at_non_zero_position(self):
        """Test parsing dict literal when pos is not at start."""
        expected_ast = {
            "type": "dict_literal",
            "children": [
                {"type": "key_value", "key": "a", "value": {"type": "number", "value": "1"}}
            ],
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 2},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 5},
                {"type": "STRING", "value": "a", "line": 1, "column": 6},
                {"type": "COLON", "value": ":", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 8},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 9}
            ],
            "pos": 2,
            "filename": "test.py"
        }
        
        with patch.object(_parse_dict_literal, 'return_value', expected_ast) as mock_dict:
            result = _parse_expression(parser_state)
            
            mock_dict.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_boolean_literal(self):
        """Test parsing boolean literals (True/False)."""
        primary_ast = {
            "type": "boolean",
            "value": "True",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "TRUE", "value": "True", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', primary_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, primary_ast)

    def test_none_literal(self):
        """Test parsing None literal."""
        primary_ast = {
            "type": "none",
            "value": "None",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "NONE", "value": "None", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', primary_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, primary_ast)

    def test_complex_binary_expression(self):
        """Test parsing complex binary expression with multiple operators."""
        primary_ast = {
            "type": "identifier",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        complex_ast = {
            "type": "binary_op",
            "left": {
                "type": "binary_op",
                "left": primary_ast,
                "operator": "*",
                "right": {"type": "number", "value": "2"}
            },
            "operator": "+",
            "right": {"type": "number", "value": "1"},
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
                {"type": "PLUS", "value": "+", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch.object(_parse_primary, 'return_value', primary_ast) as mock_primary, \
             patch.object(_parse_binary_op, 'return_value', complex_ast) as mock_binary:
            
            result = _parse_expression(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            mock_binary.assert_called_once_with(parser_state, 0)
            self.assertEqual(result, complex_ast)

    def test_preserves_filename_in_error(self):
        """Test that error message includes the correct filename."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "/path/to/my_module.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("/path/to/my_module.py", str(context.exception))


if __name__ == "__main__":
    unittest.main()
