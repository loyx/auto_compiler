#!/usr/bin/env python3
"""Unit tests for _parse_atom function."""

import unittest
from unittest.mock import patch

from ._parse_atom_src import _parse_atom


class TestParseAtom(unittest.TestCase):
    """Test cases for _parse_atom function."""

    def _create_parser_state(self, tokens, pos=0, filename="test.py"):
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type, value, line=1, column=1):
        """Helper to create token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ===== Happy Path: Literals =====

    @patch("._parse_atom_src._parse_literal")
    def test_parse_number_literal(self, mock_parse_literal):
        """Test parsing NUMBER literal delegates to _parse_literal."""
        token = self._create_token("NUMBER", "42")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {"type": "NUMBER", "value": 42, "line": 1, "column": 1}
        mock_parse_literal.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_literal.assert_called_once_with(parser_state, token)

    @patch("._parse_literal_package._parse_literal_src._parse_literal")
    def test_parse_string_literal(self, mock_parse_literal):
        """Test parsing STRING literal delegates to _parse_literal."""
        token = self._create_token("STRING", '"hello"')
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {"type": "STRING", "value": "hello", "line": 1, "column": 1}
        mock_parse_literal.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_literal.assert_called_once_with(parser_state, token)

    @patch("._parse_literal_package._parse_literal_src._parse_literal")
    def test_parse_true_literal(self, mock_parse_literal):
        """Test parsing TRUE literal delegates to _parse_literal."""
        token = self._create_token("TRUE", "true")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {"type": "BOOL", "value": True, "line": 1, "column": 1}
        mock_parse_literal.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_literal.assert_called_once_with(parser_state, token)

    @patch("._parse_literal_package._parse_literal_src._parse_literal")
    def test_parse_false_literal(self, mock_parse_literal):
        """Test parsing FALSE literal delegates to _parse_literal."""
        token = self._create_token("FALSE", "false")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {"type": "BOOL", "value": False, "line": 1, "column": 1}
        mock_parse_literal.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_literal.assert_called_once_with(parser_state, token)

    @patch("._parse_literal_package._parse_literal_src._parse_literal")
    def test_parse_none_literal(self, mock_parse_literal):
        """Test parsing NONE literal delegates to _parse_literal."""
        token = self._create_token("NONE", "none")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {"type": "NONE", "value": None, "line": 1, "column": 1}
        mock_parse_literal.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_literal.assert_called_once_with(parser_state, token)

    # ===== Happy Path: Identifiers =====

    def test_parse_identifier(self):
        """Test parsing IDENT token returns identifier AST."""
        token = self._create_token("IDENT", "x", line=5, column=10)
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        result = _parse_atom(parser_state)

        expected_ast = {
            "type": "IDENT",
            "value": "x",
            "line": 5,
            "column": 10
        }
        self.assertEqual(result, expected_ast)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_with_different_name(self):
        """Test parsing different identifier names."""
        token = self._create_token("IDENT", "my_variable")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        result = _parse_atom(parser_state)

        self.assertEqual(result["value"], "my_variable")
        self.assertEqual(parser_state["pos"], 1)

    # ===== Happy Path: Unary Operations =====

    @patch("._parse_unary_package._parse_unary_src._parse_unary")
    def test_parse_minus_unary(self, mock_parse_unary):
        """Test parsing MINUS unary operator delegates to _parse_unary."""
        token = self._create_token("MINUS", "-")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "NUMBER", "value": 5},
            "line": 1,
            "column": 1
        }
        mock_parse_unary.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_unary.assert_called_once_with(parser_state, token)

    @patch("._parse_unary_package._parse_unary_src._parse_unary")
    def test_parse_not_unary(self, mock_parse_unary):
        """Test parsing NOT unary operator delegates to _parse_unary."""
        token = self._create_token("NOT", "not")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        expected_ast = {
            "type": "UNOP",
            "op": "not",
            "operand": {"type": "BOOL", "value": True},
            "line": 1,
            "column": 1
        }
        mock_parse_unary.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_unary.assert_called_once_with(parser_state, token)

    # ===== Edge Cases: Error Handling =====

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = self._create_parser_state([])

        with self.assertRaises(SyntaxError) as context:
            _parse_atom(parser_state)

        self.assertEqual(str(context.exception), "Incomplete expression")
        self.assertEqual(parser_state["pos"], 0)

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos >= len(tokens) raises SyntaxError."""
        token = self._create_token("NUMBER", "1")
        tokens = [token]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_atom(parser_state)

        self.assertEqual(str(context.exception), "Incomplete expression")

    def test_unknown_token_type_raises_syntax_error(self):
        """Test that unknown token type raises SyntaxError."""
        token = self._create_token("UNKNOWN", "???")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_atom(parser_state)

        self.assertIn("Unexpected token in expression", str(context.exception))
        self.assertIn("UNKNOWN", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_operator_token_raises_syntax_error(self):
        """Test that operator tokens (not unary) raise SyntaxError."""
        token = self._create_token("PLUS", "+")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_atom(parser_state)

        self.assertIn("Unexpected token in expression", str(context.exception))
        self.assertIn("PLUS", str(context.exception))

    # ===== Side Effect Verification =====

    def test_pos_updated_after_identifier(self):
        """Test that parser_state pos is updated after parsing identifier."""
        token1 = self._create_token("IDENT", "x")
        token2 = self._create_token("NUMBER", "1")
        tokens = [token1, token2]
        parser_state = self._create_parser_state(tokens)

        _parse_atom(parser_state)

        self.assertEqual(parser_state["pos"], 1)

    @patch("._parse_literal_package._parse_literal_src._parse_literal")
    def test_pos_updated_by_literal_parser(self, mock_parse_literal):
        """Test that pos update is delegated to _parse_literal for literals."""
        token = self._create_token("NUMBER", "42")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        def literal_side_effect(ps, t):
            ps["pos"] = 1
            return {"type": "NUMBER", "value": 42}

        mock_parse_literal.side_effect = literal_side_effect

        _parse_atom(parser_state)

        self.assertEqual(parser_state["pos"], 1)

    @patch("._parse_unary_package._parse_unary_src._parse_unary")
    def test_pos_updated_by_unary_parser(self, mock_parse_unary):
        """Test that pos update is delegated to _parse_unary for unary ops."""
        token = self._create_token("MINUS", "-")
        tokens = [token]
        parser_state = self._create_parser_state(tokens)

        def unary_side_effect(ps, t):
            ps["pos"] = 2
            return {"type": "UNOP", "op": "-", "operand": None}

        mock_parse_unary.side_effect = unary_side_effect

        _parse_atom(parser_state)

        self.assertEqual(parser_state["pos"], 2)

    # ===== Multiple Tokens Context =====

    def test_identifier_in_middle_of_tokens(self):
        """Test parsing identifier when not at end of token list."""
        token1 = self._create_token("NUMBER", "1")
        token2 = self._create_token("IDENT", "x")
        token3 = self._create_token("PLUS", "+")
        tokens = [token1, token2, token3]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_atom(parser_state)

        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 2)

    @patch("._parse_literal_package._parse_literal_src._parse_literal")
    def test_literal_in_middle_of_tokens(self, mock_parse_literal):
        """Test parsing literal when not at end of token list."""
        token1 = self._create_token("IDENT", "x")
        token2 = self._create_token("STRING", '"test"')
        token3 = self._create_token("PLUS", "+")
        tokens = [token1, token2, token3]
        parser_state = self._create_parser_state(tokens, pos=1)

        expected_ast = {"type": "STRING", "value": "test"}
        mock_parse_literal.return_value = expected_ast

        result = _parse_atom(parser_state)

        self.assertEqual(result, expected_ast)
        mock_parse_literal.assert_called_once_with(parser_state, token2)


if __name__ == "__main__":
    unittest.main()
