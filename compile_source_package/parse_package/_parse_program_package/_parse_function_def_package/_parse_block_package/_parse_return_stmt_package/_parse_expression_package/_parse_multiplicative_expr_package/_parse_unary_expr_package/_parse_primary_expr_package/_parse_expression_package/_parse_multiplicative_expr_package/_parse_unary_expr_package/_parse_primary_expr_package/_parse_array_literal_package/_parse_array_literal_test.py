# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === relative imports ===
from ._parse_array_literal_src import _parse_array_literal

# === Type aliases (matching source) ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseArrayLiteral(unittest.TestCase):
    """Test cases for _parse_array_literal function."""

    def test_empty_array(self):
        """Test parsing empty array []."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        result = _parse_array_literal(parser_state)

        self.assertEqual(result["type"], "ARRAY_LITERAL")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_single_element_array(self):
        """Test parsing array with single element [expr]."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        mock_element_ast: AST = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": 42,
            "line": 1,
            "column": 2,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression"
        ) as mock_parse_expression:
            mock_parse_expression.return_value = mock_element_ast
            result = _parse_array_literal(parser_state)

        self.assertEqual(result["type"], "ARRAY_LITERAL")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_element_ast)
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_expression.assert_called_once()

    def test_multiple_elements_array(self):
        """Test parsing array with multiple elements [expr, expr, expr]."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "COMMA", "value": ",", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 7},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        mock_element_1: AST = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": 1,
            "line": 1,
            "column": 2,
        }
        mock_element_2: AST = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": 2,
            "line": 1,
            "column": 4,
        }
        mock_element_3: AST = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": 3,
            "line": 1,
            "column": 6,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression"
        ) as mock_parse_expression:
            mock_parse_expression.side_effect = [mock_element_1, mock_element_2, mock_element_3]
            result = _parse_array_literal(parser_state)

        self.assertEqual(result["type"], "ARRAY_LITERAL")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], mock_element_1)
        self.assertEqual(result["children"][1], mock_element_2)
        self.assertEqual(result["children"][2], mock_element_3)
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_parse_expression.call_count, 3)

    def test_missing_left_bracket(self):
        """Test error when first token is not LEFT_BRACKET."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)

        self.assertIn("Expected LEFT_BRACKET", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_unexpected_end_after_left_bracket(self):
        """Test error when input ends after LEFT_BRACKET."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_missing_right_bracket(self):
        """Test error when RIGHT_BRACKET is missing after elements."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        mock_element_ast: AST = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": 42,
            "line": 1,
            "column": 2,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression"
        ) as mock_parse_expression:
            mock_parse_expression.return_value = mock_element_ast
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unexpected_token_after_element(self):
        """Test error when unexpected token appears after element (not COMMA or RIGHT_BRACKET)."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 0,
        }

        mock_element_ast: AST = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": 42,
            "line": 1,
            "column": 2,
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression"
        ) as mock_parse_expression:
            mock_parse_expression.return_value = mock_element_ast
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)

        self.assertIn("Expected COMMA or RIGHT_BRACKET", str(context.exception))

    def test_pos_out_of_bounds(self):
        """Test error when pos is already beyond token list."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.txt",
            "error": "",
            "pos": 5,
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))


if __name__ == "__main__":
    unittest.main()
