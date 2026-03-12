"""Unit tests for _parse_primary function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Mock the dependencies before importing _parse_primary
import sys
from unittest.mock import MagicMock

# Create mock modules for the dependency chain
mock_parse_expression = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src'] = MagicMock()

from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_parse_identifier(self) -> None:
        """Test parsing an IDENTIFIER token."""
        tokens = [self._create_token("IDENTIFIER", "myVar", 1, 5)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_parse_literal_string(self) -> None:
        """Test parsing a LITERAL token (string)."""
        tokens = [self._create_token("LITERAL", '"hello"', 2, 10)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.convert_literal_value_package.convert_literal_value_src.convert_literal_value") as mock_convert:
            mock_convert.return_value = "hello"

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_parse_literal_integer(self) -> None:
        """Test parsing a LITERAL token (integer)."""
        tokens = [self._create_token("LITERAL", "42", 1, 1)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.convert_literal_value_package.convert_literal_value_src.convert_literal_value") as mock_convert:
            mock_convert.return_value = 42

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_float(self) -> None:
        """Test parsing a LITERAL token (float)."""
        tokens = [self._create_token("LITERAL", "3.14", 1, 1)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.convert_literal_value_package.convert_literal_value_src.convert_literal_value") as mock_convert:
            mock_convert.return_value = 3.14

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true(self) -> None:
        """Test parsing a TRUE token."""
        tokens = [self._create_token("TRUE", "true", 3, 7)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_parse_false(self) -> None:
        """Test parsing a FALSE token."""
        tokens = [self._create_token("FALSE", "false", 4, 2)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 4)
        self.assertEqual(result["column"], 2)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_parse_nil(self) -> None:
        """Test parsing a NIL token."""
        tokens = [self._create_token("NIL", "nil", 5, 15)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 15)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_parse_parenthesized_expression_success(self) -> None:
        """Test parsing a parenthesized expression with matching right paren."""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2),
            self._create_token("RIGHT_PAREN", ")", 1, 3)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_expr_ast

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 3)
        self.assertIsNone(parser_state["error"])
        mock_parse_expr.assert_called_once()

    def test_parse_lparen_with_rparen_variant(self) -> None:
        """Test parsing with LPAREN/RPAREN token types."""
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "y", 1, 2),
            self._create_token("RPAREN", ")", 1, 3)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "y",
            "children": [],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_expr_ast

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_parenthesized_expression_missing_closing(self) -> None:
        """Test parsing parenthesized expression with missing closing paren."""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_expr_ast

            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.make_error_node_package.make_error_node_src.make_error_node") as mock_make_error:
                mock_make_error.return_value = {
                    "type": "ERROR",
                    "value": None,
                    "children": [],
                    "line": 1,
                    "column": 3
                }

                result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIsNotNone(parser_state["error"])
        self.assertEqual(parser_state["error"], "Expected ')' after expression")

    def test_parse_parenthesized_expression_wrong_closing_token(self) -> None:
        """Test parsing parenthesized expression with wrong closing token."""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2),
            self._create_token("SEMICOLON", ";", 1, 3)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_expr_ast

            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.make_error_node_package.make_error_node_src.make_error_node") as mock_make_error:
                mock_make_error.return_value = {
                    "type": "ERROR",
                    "value": None,
                    "children": [],
                    "line": 1,
                    "column": 3
                }

                result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIsNotNone(parser_state["error"])
        self.assertIn("Expected ')'", parser_state["error"])
        self.assertIn("SEMICOLON", parser_state["error"])

    def test_parse_parenthesized_expression_with_error(self) -> None:
        """Test parsing parenthesized expression when inner expression has error."""
        tokens = [
            self._create_token("LEFT_PAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2),
            self._create_token("RIGHT_PAREN", ")", 1, 3)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        mock_error_ast = {
            "type": "ERROR",
            "value": None,
            "children": [],
            "line": 1,
            "column": 2
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def set_error_and_return(state):
                state["error"] = "Inner expression error"
                return mock_error_ast

            mock_parse_expr.side_effect = set_error_and_return

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIsNotNone(parser_state["error"])

    def test_empty_tokens(self) -> None:
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.make_error_node_package.make_error_node_src.make_error_node") as mock_make_error:
            mock_make_error.return_value = {
                "type": "ERROR",
                "value": None,
                "children": [],
                "line": 0,
                "column": 0
            }

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Unexpected end of input")
        mock_make_error.assert_called_once_with(0, [])

    def test_pos_at_end_of_tokens(self) -> None:
        """Test parsing when pos is at end of tokens."""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.cc",
            "error": None
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package.make_error_node_package.make_error_node_src.make_error_node") as mock_make_error:
            mock_make_error.return_value = {
                "type": "ERROR",
                "value": None,
                "children": [],
                "line": 0,
                "column": 0
            }

            result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_unexpected_token_type(self) -> None:
        """Test parsing with unexpected token type."""
        tokens = [self._create_token("PLUS", "+", 2, 5)]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.cc",
            "error": None
        }

        result = _parse_primary(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIsNotNone(parser_state["error"])
        self.assertIn("Unexpected token: PLUS", parser_state["error"])
        self.assertIn("line 2", parser_state["error"])
        self.assertIn("column 5", parser_state["error"])

    def test_operator_token(self) -> None:
        """Test parsing with various operator tokens."""
        for op_type in ["MINUS", "STAR", "SLASH", "EQUAL"]:
            tokens = [self._create_token(op_type, op_type.lower(), 1, 1)]
            parser_state = {
                "tokens": tokens,
                "pos": 0,
                "filename": "test.cc",
                "error": None
            }

            result = _parse_primary(parser_state)

            self.assertEqual(result["type"], "ERROR", f"Failed for token type: {op_type}")
            self.assertIsNotNone(parser_state["error"])


if __name__ == "__main__":
    unittest.main()
