import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """单元测试：_parse_primary_expr 函数"""

    def _make_token(self, token_type: str, value: Any, line: int, column: int) -> Dict[str, Any]:
        """Helper: create a token dict."""
        return {"type": token_type, "value": value, "line": line, "column": column}

    def _make_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper: create a parser_state dict."""
        return {"tokens": tokens, "pos": pos, "filename": filename, "error": None}

    def test_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = self._make_parser_state([])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_pos_at_end(self):
        """Test parsing when pos >= len(tokens)."""
        token = self._make_token("IDENTIFIER", "x", 1, 1)
        parser_state = self._make_parser_state([token], pos=1)
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")

    def test_parse_identifier_without_call(self):
        """Test parsing a simple identifier that is not a function call."""
        token = self._make_token("IDENTIFIER", "x", 1, 1)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state.get("error"))

    def test_parse_identifier_with_call(self):
        """Test parsing an identifier followed by LPAREN (function call)."""
        ident_token = self._make_token("IDENTIFIER", "func", 1, 1)
        lparen_token = self._make_token("LPAREN", "(", 1, 5)
        parser_state = self._make_parser_state([ident_token, lparen_token])
        mock_result = {"type": "CALL", "value": "func", "children": []}
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_call_expr_package._parse_call_expr_src._parse_call_expr") as mock_parse_call:
            mock_parse_call.return_value = mock_result
            result = _parse_primary_expr(parser_state)
            self.assertEqual(result["type"], "CALL")
            mock_parse_call.assert_called_once()
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_number_literal(self):
        """Test parsing a NUMBER token."""
        token = self._make_token("NUMBER", 42, 1, 1)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a STRING token."""
        token = self._make_token("STRING", "hello", 2, 3)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true_literal(self):
        """Test parsing a TRUE token."""
        token = self._make_token("TRUE", "true", 1, 1)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "true")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false_literal(self):
        """Test parsing a FALSE token."""
        token = self._make_token("FALSE", "false", 1, 1)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "false")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_none_literal(self):
        """Test parsing a NONE token."""
        token = self._make_token("NONE", "None", 1, 1)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "None")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        lparen_token = self._make_token("LPAREN", "(", 1, 1)
        inner_token = self._make_token("NUMBER", 42, 1, 2)
        rparen_token = self._make_token("RPAREN", ")", 1, 3)
        parser_state = self._make_parser_state([lparen_token, inner_token, rparen_token])
        mock_inner_expr = {"type": "LITERAL", "value": 42, "line": 1, "column": 2, "children": []}
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package.expression_parser_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            result = _parse_primary_expr(parser_state)
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)
            mock_parse_expr.assert_called_once()
            self.assertEqual(parser_state["pos"], 3)

    def test_parse_parenthesized_expression_missing_rparen(self):
        """Test parsing a parenthesized expression without closing RPAREN."""
        lparen_token = self._make_token("LPAREN", "(", 1, 1)
        inner_token = self._make_token("NUMBER", 42, 1, 2)
        parser_state = self._make_parser_state([lparen_token, inner_token])
        mock_inner_expr = {"type": "LITERAL", "value": 42, "line": 1, "column": 2, "children": []}
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package.expression_parser_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            result = _parse_primary_expr(parser_state)
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Expected ')'")
            self.assertEqual(parser_state["error"], "Expected ')'")

    def test_parse_list_literal(self):
        """Test parsing a list literal."""
        lbracket_token = self._make_token("LBRACKET", "[", 1, 1)
        parser_state = self._make_parser_state([lbracket_token])
        mock_list_result = {"type": "LIST", "value": [], "children": []}
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_expr_package._parse_list_literal_package._parse_list_literal_src._parse_list_literal") as mock_parse_list:
            mock_parse_list.return_value = mock_list_result
            result = _parse_primary_expr(parser_state)
            self.assertEqual(result["type"], "LIST")
            mock_parse_list.assert_called_once()
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_unexpected_token(self):
        """Test parsing an unexpected token type."""
        token = self._make_token("PLUS", "+", 1, 1)
        parser_state = self._make_parser_state([token])
        result = _parse_primary_expr(parser_state)
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected token: PLUS")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["error"], "Unexpected token: PLUS")

    def test_parse_multiple_identifiers_sequence(self):
        """Test parsing multiple identifiers in sequence."""
        token1 = self._make_token("IDENTIFIER", "x", 1, 1)
        token2 = self._make_token("IDENTIFIER", "y", 1, 3)
        parser_state = self._make_parser_state([token1, token2])
        result1 = _parse_primary_expr(parser_state)
        self.assertEqual(result1["type"], "IDENTIFIER")
        self.assertEqual(result1["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
        result2 = _parse_primary_expr(parser_state)
        self.assertEqual(result2["type"], "IDENTIFIER")
        self.assertEqual(result2["value"], "y")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
