"""Unit tests for _parse_primary function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

from ._parse_primary_src import _parse_primary


def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {"type": token_type, "value": value, "line": line, "column": column}


def make_parser_state(tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.txt") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {"tokens": tokens, "pos": pos, "filename": filename, "error": None}


class TestParsePrimaryLiterals(unittest.TestCase):
    """Test cases for literal parsing."""

    def test_parse_number_literal(self):
        """Test parsing NUMBER token."""
        tokens = [make_token("NUMBER", "42")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["literal_type"], "NUMBER")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)
        self.assertIsNone(state["error"])

    def test_parse_string_literal_double_quotes(self):
        """Test parsing STRING token with double quotes (quotes removed)."""
        tokens = [make_token("STRING", '"hello"')]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["literal_type"], "STRING")
        self.assertEqual(state["pos"], 1)

    def test_parse_string_literal_single_quotes(self):
        """Test parsing STRING token with single quotes (quotes removed)."""
        tokens = [make_token("STRING", "'world'")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "world")
        self.assertEqual(result["literal_type"], "STRING")

    def test_parse_identifier(self):
        """Test parsing IDENTIFIER token."""
        tokens = [make_token("IDENTIFIER", "myVar")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "myVar")
        self.assertEqual(state["pos"], 1)

    def test_parse_true_literal(self):
        """Test parsing TRUE token."""
        tokens = [make_token("TRUE", "true")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["literal_type"], "BOOLEAN")

    def test_parse_false_literal(self):
        """Test parsing FALSE token."""
        tokens = [make_token("FALSE", "false")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["literal_type"], "BOOLEAN")

    def test_parse_null_literal(self):
        """Test parsing NULL token."""
        tokens = [make_token("NULL", "null")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["literal_type"], "NULL")


class TestParsePrimaryParenthesized(unittest.TestCase):
    """Test cases for parenthesized expressions."""

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_unary_package._parse_unary_src._parse_unary")
    def test_parse_parenthesized_expression_success(self, mock_parse_unary):
        """Test parsing parenthesized expression with matching closing paren."""
        mock_parse_unary.return_value = {"type": "LITERAL", "value": "5"}
        
        tokens = [
            make_token("LEFT_PAREN", "(", line=2, column=3),
            make_token("NUMBER", "5"),
            make_token("RIGHT_PAREN", ")")
        ]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        mock_parse_unary.assert_called_once()
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "5")
        self.assertEqual(state["pos"], 3)
        self.assertIsNone(state["error"])

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_unary_package._parse_unary_src._parse_unary")
    def test_parse_parenthesized_expression_missing_closing(self, mock_parse_unary):
        """Test parsing parenthesized expression without closing paren."""
        mock_parse_unary.return_value = {"type": "LITERAL", "value": "5"}
        
        tokens = [
            make_token("LEFT_PAREN", "(", line=2, column=3),
            make_token("NUMBER", "5")
        ]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(state["error"], "Missing closing parenthesis")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_unary_package._parse_unary_src._parse_unary")
    def test_parse_parenthesized_expression_unary_error(self, mock_parse_unary):
        """Test parsing when _parse_unary sets an error."""
        def set_error(state):
            state["error"] = "Inner error"
            return {"type": "ERROR"}
        mock_parse_unary.side_effect = set_error
        
        tokens = [
            make_token("LEFT_PAREN", "(", line=1, column=1),
            make_token("NUMBER", "5")
        ]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(state["error"], "Inner error")


class TestParsePrimaryCollections(unittest.TestCase):
    """Test cases for array and dict literals."""

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_array_literal_package._parse_array_literal_src._parse_array_literal")
    def test_parse_array_literal(self, mock_parse_array):
        """Test parsing array literal delegates to _parse_array_literal."""
        mock_parse_array.return_value = {"type": "ARRAY_LITERAL", "children": []}
        
        tokens = [make_token("LEFT_BRACKET", "[", line=3, column=5)]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        mock_parse_array.assert_called_once_with(state, 3, 5)
        self.assertEqual(result["type"], "ARRAY_LITERAL")
        self.assertEqual(state["pos"], 1)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_dict_literal_package._parse_dict_literal_src._parse_dict_literal")
    def test_parse_dict_literal(self, mock_parse_dict):
        """Test parsing dict literal delegates to _parse_dict_literal."""
        mock_parse_dict.return_value = {"type": "DICT_LITERAL", "children": []}
        
        tokens = [make_token("LEFT_BRACE", "{", line=4, column=7)]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        mock_parse_dict.assert_called_once_with(state, 4, 7)
        self.assertEqual(result["type"], "DICT_LITERAL")
        self.assertEqual(state["pos"], 1)


class TestParsePrimaryErrors(unittest.TestCase):
    """Test cases for error handling."""

    def test_empty_tokens(self):
        """Test parsing when tokens list is empty."""
        state = make_parser_state([])
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(state["error"], "Unexpected end of input")
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(state["pos"], 0)

    def test_pos_beyond_tokens(self):
        """Test parsing when pos is beyond tokens length."""
        tokens = [make_token("NUMBER", "1")]
        state = make_parser_state(tokens, pos=5)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(state["error"], "Unexpected end of input")

    def test_unrecognized_token_type(self):
        """Test parsing unrecognized token type."""
        tokens = [make_token("UNKNOWN_TOKEN", "???")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(state["error"], "Unexpected token: UNKNOWN_TOKEN")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 0)

    def test_error_preserves_position(self):
        """Test that position is not advanced on error."""
        tokens = [make_token("INVALID", "x")]
        state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(state)
        
        self.assertEqual(state["pos"], 0)
        self.assertIsNotNone(state["error"])


class TestParsePrimaryEdgeCases(unittest.TestCase):
    """Edge case tests."""

    def test_string_with_mismatched_quotes_not_stripped(self):
        """Test string with mismatched quotes is not stripped."""
        tokens = [make_token("STRING", '"hello')]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello')
        self.assertEqual(result["literal_type"], "STRING")

    def test_single_char_string(self):
        """Test single character string (too short to have quotes)."""
        tokens = [make_token("STRING", "a")]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "a")

    def test_custom_line_column_preserved(self):
        """Test that custom line and column are preserved in result."""
        tokens = [make_token("NUMBER", "123", line=10, column=25)]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    def test_token_missing_optional_fields(self):
        """Test token without line/column uses defaults."""
        tokens = [{"type": "NUMBER", "value": "999"}]
        state = make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)


if __name__ == "__main__":
    unittest.main()
