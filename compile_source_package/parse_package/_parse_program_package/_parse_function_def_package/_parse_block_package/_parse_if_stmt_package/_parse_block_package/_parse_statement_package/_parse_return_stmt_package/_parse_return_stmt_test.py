# -*- coding: utf-8 -*-
"""Unit tests for _parse_return_stmt function."""

import unittest
from unittest.mock import patch

from ._parse_return_stmt_src import _parse_return_stmt


class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""

    def test_return_stmt_without_value(self):
        """Test parsing 'return;' statement without return value."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)

    def test_return_stmt_with_value(self):
        """Test parsing 'return expr;' statement with return value."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 2, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 2,
            "column": 10
        }
        
        with patch("._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)

    def test_return_stmt_with_complex_expression(self):
        """Test parsing 'return a + b;' with complex expression."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 5, "column": 1},
            {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 8},
            {"type": "OPERATOR", "value": "+", "line": 5, "column": 10},
            {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 13},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "main.c"
        }
        
        mock_expr_ast = {
            "type": "BINARY_EXPR",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 8},
                {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 12}
            ],
            "value": "+",
            "line": 5,
            "column": 8
        }
        
        with patch("._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 4}) or mock_expr_ast
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BINARY_EXPR")
        self.assertEqual(parser_state["pos"], 5)

    def test_missing_semicolon_raises_error(self):
        """Test that missing semicolon raises SyntaxError."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 3, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "error.c"
        }
        
        with patch("._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 9}
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_parse_expr.return_value
            
            with self.assertRaises(SyntaxError) as context:
                _parse_return_stmt(parser_state)
            
            self.assertIn("expected ';' after return statement", str(context.exception))
            self.assertIn("error.c:3:2", str(context.exception))

    def test_missing_semicolon_without_value_raises_error(self):
        """Test that 'return' without semicolon raises SyntaxError."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 4, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "error.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("expected ';' after return statement", str(context.exception))
        self.assertIn("error.c:4:1", str(context.exception))

    def test_return_at_end_of_tokens_without_semicolon(self):
        """Test return statement at end of token stream without semicolon."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 10, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "eof.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("expected ';' after return statement", str(context.exception))

    def test_parser_state_pos_updated_correctly(self):
        """Test that parser_state position is updated correctly after parsing."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
            {"type": "OTHER", "value": "next", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)
        self.assertIsNotNone(result)

    def test_return_stmt_preserves_filename_in_error(self):
        """Test that error message includes correct filename."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 7, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "my_module.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("my_module.c:7:3", str(context.exception))

    def test_return_stmt_default_filename(self):
        """Test that default filename is used when not provided."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("<unknown>:1:1", str(context.exception))

    def test_return_stmt_with_number_literal(self):
        """Test parsing 'return 42;' with number literal."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 6, "column": 2},
            {"type": "NUMBER", "value": "42", "line": 6, "column": 9},
            {"type": "SEMICOLON", "value": ";", "line": 6, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "NUMBER_LITERAL",
            "value": "42",
            "line": 6,
            "column": 9
        }
        
        with patch("._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_expr_ast
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NUMBER_LITERAL")
        self.assertEqual(result["children"][0]["value"], "42")
        self.assertEqual(parser_state["pos"], 3)

    def test_return_stmt_with_function_call(self):
        """Test parsing 'return func();' with function call expression."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 8, "column": 4},
            {"type": "IDENTIFIER", "value": "func", "line": 8, "column": 11},
            {"type": "LPAREN", "value": "(", "line": 8, "column": 15},
            {"type": "RPAREN", "value": ")", "line": 8, "column": 16},
            {"type": "SEMICOLON", "value": ";", "line": 8, "column": 17},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "CALL_EXPR",
            "value": "func",
            "line": 8,
            "column": 11
        }
        
        with patch("._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 4}) or mock_expr_ast
            
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "CALL_EXPR")
        self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()
