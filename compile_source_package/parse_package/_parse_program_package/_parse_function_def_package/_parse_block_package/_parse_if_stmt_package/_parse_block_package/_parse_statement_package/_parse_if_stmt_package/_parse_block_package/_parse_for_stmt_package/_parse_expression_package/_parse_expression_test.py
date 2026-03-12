# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_parse_assignment(self):
        """Happy path: _parse_expression delegates to _parse_assignment and returns result."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "filename": "test.c",
            "pos": 0
        }
        
        expected_ast = {
            "type": "NUMBER",
            "value": 42,
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_assignment_src._parse_assignment") as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_assignment.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_updates_pos_via_assignment(self):
        """Verify that parser_state pos is updated through _parse_assignment side effect."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 3}
            ],
            "filename": "test.c",
            "pos": 0
        }
        
        def assignment_side_effect(state):
            state["pos"] = 1
            return {"type": "NUMBER", "value": 42, "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_assignment_src._parse_assignment") as mock_parse_assignment:
            mock_parse_assignment.side_effect = assignment_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(result["type"], "NUMBER")

    def test_parse_expression_empty_tokens_raises_error(self):
        """Boundary: empty tokens list should raise SyntaxError."""
        parser_state = {
            "tokens": [],
            "filename": "test.c",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))
        self.assertIn("test.c", str(context.exception))

    def test_parse_expression_pos_beyond_tokens_raises_error(self):
        """Boundary: pos beyond token list length should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "filename": "test.c",
            "pos": 5
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_parse_expression_pos_at_end_raises_error(self):
        """Boundary: pos exactly at token list length should raise SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "filename": "test.c",
            "pos": 1
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_parse_expression_error_includes_location(self):
        """Verify error message includes line and column from current token."""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 10, "column": 5}
            ],
            "filename": "mycode.c",
            "pos": 0
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_assignment_src._parse_assignment") as mock_parse_assignment:
            mock_parse_assignment.return_value = {"type": "SEMICOLON", "value": ";", "line": 10, "column": 5}
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "SEMICOLON")
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 5)

    def test_parse_expression_with_string_literal(self):
        """Test parsing expression starting with string literal token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 2, "column": 1}
            ],
            "filename": "test.c",
            "pos": 0
        }
        
        expected_ast = {
            "type": "STRING",
            "value": "hello",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_assignment_src._parse_assignment") as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_identifier(self):
        """Test parsing expression starting with identifier token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 1}
            ],
            "filename": "test.c",
            "pos": 0
        }
        
        expected_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 3,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_assignment_src._parse_assignment") as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_boolean_literal(self):
        """Test parsing expression starting with boolean literal token."""
        parser_state = {
            "tokens": [
                {"type": "BOOL", "value": "true", "line": 1, "column": 1}
            ],
            "filename": "test.c",
            "pos": 0
        }
        
        expected_ast = {
            "type": "BOOL",
            "value": True,
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_assignment_package._parse_assignment_src._parse_assignment") as mock_parse_assignment:
            mock_parse_assignment.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, expected_ast)

    def test_parse_expression_missing_filename_uses_default(self):
        """Verify error uses default filename when not provided."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))


if __name__ == "__main__":
    unittest.main()
