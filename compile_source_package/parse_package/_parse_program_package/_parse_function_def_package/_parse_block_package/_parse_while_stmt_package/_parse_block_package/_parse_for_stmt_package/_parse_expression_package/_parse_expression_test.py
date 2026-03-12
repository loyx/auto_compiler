"""
Unit tests for _parse_expression function.
Tests expression parsing after 'in' keyword in for statements.
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create parser state dictionary."""
        return {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def test_parse_expression_success(self):
        """Test successful expression parsing with primary expr and binop tail."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 3},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        mock_primary = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1,
            "children": []
        }
        mock_binop_result = {
            "type": "BINARY_OP",
            "value": "+",
            "line": 1,
            "column": 1,
            "children": [mock_primary, {"type": "NUMBER", "value": "1", "line": 1, "column": 3, "children": []}]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_primary
                mock_parse_binop.return_value = mock_binop_result
                
                result = _parse_expression(parser_state)
                
                mock_parse_primary.assert_called_once()
                mock_parse_binop.assert_called_once()
                self.assertEqual(result, mock_binop_result)
                self.assertEqual(parser_state["pos"], 0)

    def test_parse_expression_empty_tokens(self):
        """Test expression parsing with empty token list - should return error."""
        parser_state = self._create_parser_state(tokens=[], pos=0)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])
        self.assertEqual(
            parser_state["error"],
            "Unexpected end of input while parsing expression"
        )

    def test_parse_expression_pos_at_end(self):
        """Test expression parsing when pos is at end of tokens - should return error."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(
            parser_state["error"],
            "Unexpected end of input while parsing expression"
        )

    def test_parse_expression_pos_beyond_length(self):
        """Test expression parsing when pos is beyond token list length."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=5)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(
            parser_state["error"],
            "Unexpected end of input while parsing expression"
        )

    def test_parse_expression_only_primary(self):
        """Test expression with only primary expression (no binary operators)."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        mock_primary = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_primary
                mock_parse_binop.return_value = mock_primary  # binop tail returns same if no operators
                
                result = _parse_expression(parser_state)
                
                mock_parse_primary.assert_called_once_with(parser_state)
                mock_parse_binop.assert_called_once_with(parser_state, mock_primary)
                self.assertEqual(result, mock_primary)

    def test_parse_expression_complex_expression(self):
        """Test parsing a complex expression with multiple operators."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
            {"type": "STAR", "value": "*", "line": 1, "column": 4},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        mock_primary = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1,
            "children": []
        }
        mock_binop_result = {
            "type": "BINARY_OP",
            "value": "+",
            "line": 1,
            "column": 1,
            "children": [mock_primary, {"type": "BINARY_OP", "value": "*", "children": []}]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_primary
                mock_parse_binop.return_value = mock_binop_result
                
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], "+")

    def test_parse_expression_preserves_parser_state(self):
        """Test that parser state is properly passed to sub-functions."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0, filename="test_file.py")
        
        mock_primary = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_primary
                mock_parse_binop.return_value = mock_primary
                
                _parse_expression(parser_state)
                
                # Verify parser_state was passed to sub-functions
                mock_parse_primary.assert_called_once()
                called_state = mock_parse_primary.call_args[0][0]
                self.assertEqual(called_state["filename"], "test_file.py")
                self.assertEqual(called_state["pos"], 0)

    def test_parse_expression_error_propagation(self):
        """Test that errors from sub-functions are handled."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        mock_error_node = {
            "type": "ERROR",
            "value": None,
            "line": 1,
            "column": 1,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_error_node
                mock_parse_binop.return_value = mock_error_node
                
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "ERROR")
                mock_parse_primary.assert_called_once()
                mock_parse_binop.assert_called_once()

    def test_parse_expression_with_list_literal(self):
        """Test parsing expression that is a list literal."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "RBRACKET", "value": "]", "line": 1, "column": 3},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        mock_list_node = {
            "type": "LIST",
            "value": None,
            "line": 1,
            "column": 1,
            "children": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2, "children": []}
            ]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_list_node
                mock_parse_binop.return_value = mock_list_node
                
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LIST")
                self.assertEqual(len(result["children"]), 1)

    def test_parse_expression_with_string_literal(self):
        """Test parsing expression that is a string literal."""
        tokens = [
            {"type": "STRING", "value": '"hello"', "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        mock_string_node = {
            "type": "STRING_LITERAL",
            "value": '"hello"',
            "line": 1,
            "column": 1,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse_primary:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_binop_tail_src._parse_binop_tail") as mock_parse_binop:
                mock_parse_primary.return_value = mock_string_node
                mock_parse_binop.return_value = mock_string_node
                
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "STRING_LITERAL")
                self.assertEqual(result["value"], '"hello"')


if __name__ == "__main__":
    unittest.main()
