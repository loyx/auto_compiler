"""Unit tests for _parse_call_expr function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_call_expr_src import _parse_call_expr

Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseCallExpr(unittest.TestCase):
    """Test cases for _parse_call_expr function."""

    def test_empty_parameter_list(self):
        """Test function call with no arguments: foo()"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "foo")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 2)  # After RPAREN
        self.assertEqual(parser_state["error"], "")

    def test_single_parameter(self):
        """Test function call with one argument: foo(1)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        def mock_parse_expression(state: ParserState) -> AST:
            pos = state["pos"]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"],
                "children": []
            }

        with patch('._parse_call_expr_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "foo")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NUMBER")
        self.assertEqual(result["children"][0]["value"], "1")
        self.assertEqual(parser_state["pos"], 3)  # After RPAREN
        self.assertEqual(parser_state["error"], "")

    def test_multiple_parameters(self):
        """Test function call with multiple arguments: foo(1, 2, 3)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            {"type": "COMMA", "value": ",", "line": 1, "column": 6},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 7},
            {"type": "COMMA", "value": ",", "line": 1, "column": 8},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        def mock_parse_expression(state: ParserState) -> AST:
            pos = state["pos"]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"],
                "children": []
            }

        with patch('._parse_call_expr_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "foo")
        self.assertEqual(len(result["children"]), 3)
        for i, expected_val in enumerate(["1", "2", "3"]):
            self.assertEqual(result["children"][i]["type"], "NUMBER")
            self.assertEqual(result["children"][i]["value"], expected_val)
        self.assertEqual(parser_state["pos"], 7)  # After RPAREN
        self.assertEqual(parser_state["error"], "")

    def test_missing_lparen_error(self):
        """Test error when LPAREN is missing"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to NUMBER instead of LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Expected '('")
        self.assertEqual(parser_state["error"], "Expected '(' after function name")
        self.assertEqual(parser_state["pos"], 1)  # Position unchanged

    def test_missing_rparen_error(self):
        """Test error when RPAREN is missing"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        def mock_parse_expression(state: ParserState) -> AST:
            pos = state["pos"]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"],
                "children": []
            }

        with patch('._parse_call_expr_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected EOF")
        self.assertEqual(parser_state["error"], "Unexpected end of input, expected ')' or ','")

    def test_unexpected_token_error(self):
        """Test error when unexpected token instead of comma or rparen"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        def mock_parse_expression(state: ParserState) -> AST:
            pos = state["pos"]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"],
                "children": []
            }

        with patch('._parse_call_expr_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Syntax error in function call")
        self.assertIn("Expected ')' or ',' but got ';'", parser_state["error"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 6)

    def test_eof_during_parsing_error(self):
        """Test error when EOF occurs during argument parsing"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected EOF")
        self.assertEqual(parser_state["error"], "Unexpected end of input in function call")

    def test_parse_expression_error_propagation(self):
        """Test that errors from _parse_expression are propagated"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        def mock_parse_expression_error(state: ParserState) -> AST:
            state["error"] = "Expression parsing failed"
            return {
                "type": "ERROR",
                "value": "Bad expression",
                "line": 1,
                "column": 5,
                "children": []
            }

        with patch('._parse_call_expr_src._parse_expression', side_effect=mock_parse_expression_error):
            result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Bad expression")
        self.assertEqual(parser_state["error"], "Expression parsing failed")

    def test_complex_expression_args(self):
        """Test function call with complex expression arguments"""
        tokens = [
            {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "COMMA", "value": ",", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 7},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 8},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to LPAREN
            "filename": "test.py",
            "error": ""
        }
        func_name_token: Token = tokens[0]

        call_count = [0]

        def mock_parse_expression(state: ParserState) -> AST:
            pos = state["pos"]
            state["pos"] = pos + 1
            call_count[0] += 1
            return {
                "type": "IDENTIFIER",
                "value": tokens[pos]["value"],
                "line": tokens[pos]["line"],
                "column": tokens[pos]["column"],
                "children": []
            }

        with patch('._parse_call_expr_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_call_expr(parser_state, func_name_token)

        self.assertEqual(call_count[0], 2)  # Called twice for x and y
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["children"][1]["value"], "y")


if __name__ == "__main__":
    unittest.main()
