# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.txt"
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(
        self,
        node_type: str,
        value: Any = None,
        children: list = None,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_simple_expression(self, mock_binary_op, mock_primary):
        """Test parsing a simple expression without binary operations."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)
        
        expected_ast = self._create_ast_node("literal", 42)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, expected_ast, 0)
        self.assertEqual(result, expected_ast)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_binary_expression(self, mock_binary_op, mock_primary):
        """Test parsing an expression with binary operations."""
        tokens = [
            self._create_token("NUMBER", "10", column=1),
            self._create_token("PLUS", "+", column=3),
            self._create_token("NUMBER", "5", column=5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        left_ast = self._create_ast_node("literal", 10, column=1)
        result_ast = self._create_ast_node(
            "binary_op",
            children=[left_ast, self._create_ast_node("literal", 5)]
        )
        
        mock_primary.return_value = left_ast
        mock_binary_op.return_value = result_ast
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once()
        mock_binary_op.assert_called_once_with(parser_state, left_ast, 0)
        self.assertEqual(result, result_ast)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_identifier_expression(self, mock_binary_op, mock_primary):
        """Test parsing an identifier expression."""
        tokens = [self._create_token("IDENTIFIER", "x", column=1)]
        parser_state = self._create_parser_state(tokens)
        
        expected_ast = self._create_ast_node("identifier", "x", column=1)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_string_literal(self, mock_binary_op, mock_primary):
        """Test parsing a string literal expression."""
        tokens = [self._create_token("STRING", '"hello"', column=1)]
        parser_state = self._create_parser_state(tokens)
        
        expected_ast = self._create_ast_node("literal", "hello", column=1)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], "hello")

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_boolean_literal(self, mock_binary_op, mock_primary):
        """Test parsing a boolean literal expression."""
        tokens = [self._create_token("BOOLEAN", "true", column=1)]
        parser_state = self._create_parser_state(tokens)
        
        expected_ast = self._create_ast_node("literal", True, column=1)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], True)

    def test_parse_empty_tokens(self):
        """Test parsing with empty token list raises SyntaxError."""
        parser_state = self._create_parser_state([], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))
        self.assertIn("test.txt:1:1", str(context.exception))

    def test_parse_pos_at_end(self):
        """Test parsing when pos is already at end of tokens."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_parse_error_with_custom_filename(self):
        """Test error message includes custom filename."""
        parser_state = self._create_parser_state([], filename="custom_file.txt")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("custom_file.txt:1:1", str(context.exception))

    @patch('_parse_expression_src._parse_primary')
    def test_parse_primary_failure_propagates(self, mock_primary):
        """Test that _parse_primary exceptions propagate."""
        tokens = [self._create_token("NUMBER", "42", line=5, column=10)]
        parser_state = self._create_parser_state(tokens)
        
        mock_primary.side_effect = SyntaxError("Primary parse failed")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertEqual(str(context.exception), "Primary parse failed")
        mock_primary.assert_called_once_with(parser_state)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_with_token_position_info(self, mock_binary_op, mock_primary):
        """Test that token position info is preserved in error."""
        tokens = [
            self._create_token("NUMBER", "100", line=10, column=25)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = self._create_ast_node("literal", 100, line=10, column=25)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_complex_expression_chain(self, mock_binary_op, mock_primary):
        """Test parsing a complex expression with multiple operations."""
        tokens = [
            self._create_token("NUMBER", "1", column=1),
            self._create_token("PLUS", "+", column=3),
            self._create_token("NUMBER", "2", column=5),
            self._create_token("STAR", "*", column=7),
            self._create_token("NUMBER", "3", column=9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        left_ast = self._create_ast_node("literal", 1)
        result_ast = self._create_ast_node("binary_op", children=[left_ast])
        
        mock_primary.return_value = left_ast
        mock_binary_op.return_value = result_ast
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once()
        mock_binary_op.assert_called_once_with(parser_state, left_ast, 0)
        self.assertEqual(result["type"], "binary_op")

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_parenthesized_expression(self, mock_binary_op, mock_primary):
        """Test parsing a parenthesized expression."""
        tokens = [
            self._create_token("LPAREN", "(", column=1),
            self._create_token("NUMBER", "42", column=2),
            self._create_token("RPAREN", ")", column=4)
        ]
        parser_state = self._create_parser_state(tokens)
        
        expected_ast = self._create_ast_node("literal", 42, column=2)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["value"], 42)

    @patch('_parse_expression_src._parse_primary')
    @patch('_parse_expression_src._parse_binary_op')
    def test_parse_preserves_parser_state_structure(self, mock_binary_op, mock_primary):
        """Test that parser state structure is preserved after parsing."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)
        
        expected_ast = self._create_ast_node("literal", 42)
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        _parse_expression(parser_state)
        
        self.assertIn("tokens", parser_state)
        self.assertIn("pos", parser_state)
        self.assertIn("filename", parser_state)
        self.assertEqual(len(parser_state["tokens"]), 1)


if __name__ == "__main__":
    unittest.main()
