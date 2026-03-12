# -*- coding: utf-8 -*-
"""单元测试：_parse_primary_expr 函数"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_primary_expr_src import _parse_primary_expr


Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
    """辅助函数：创建 token 字典"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.txt") -> ParserState:
    """辅助函数：创建 parser_state 字典"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParsePrimaryExpr(unittest.TestCase):
    """_parse_primary_expr 函数测试类"""

    def test_parse_identifier(self):
        """测试解析标识符"""
        token = make_token("IDENTIFIER", "myVar", line=1, column=5)
        parser_state = make_parser_state([token], pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_integer(self):
        """测试解析整数"""
        token = make_token("NUMBER", "42", line=2, column=10)
        parser_state = make_parser_state([token], pos=0)

        with patch("._parse_number_value_package._parse_number_value_src._parse_number_value") as mock_parse_num:
            mock_parse_num.return_value = 42
            result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "NUMBER_LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_num.assert_called_once_with("42")

    def test_parse_number_float(self):
        """测试解析浮点数"""
        token = make_token("NUMBER", "3.14", line=1, column=1)
        parser_state = make_parser_state([token], pos=0)

        with patch("._parse_number_value_package._parse_number_value_src._parse_number_value") as mock_parse_num:
            mock_parse_num.return_value = 3.14
            result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "NUMBER_LITERAL")
        self.assertEqual(result["value"], 3.14)
        mock_parse_num.assert_called_once_with("3.14")

    def test_parse_string(self):
        """测试解析字符串字面量"""
        token = make_token("STRING", '"hello world"', line=3, column=7)
        parser_state = make_parser_state([token], pos=0)

        with patch("._parse_string_value_package._parse_string_value_src._parse_string_value") as mock_parse_str:
            mock_parse_str.return_value = "hello world"
            result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "STRING_LITERAL")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_str.assert_called_once_with('"hello world"')

    def test_parse_boolean_true(self):
        """测试解析布尔值 true"""
        token = make_token("BOOLEAN", "true", line=1, column=1)
        parser_state = make_parser_state([token], pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "BOOLEAN_LITERAL")
        self.assertTrue(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_boolean_false(self):
        """测试解析布尔值 false"""
        token = make_token("BOOLEAN", "FALSE", line=2, column=5)
        parser_state = make_parser_state([token], pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "BOOLEAN_LITERAL")
        self.assertFalse(result["value"])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null(self):
        """测试解析 null 字面量"""
        token = make_token("NULL", "null", line=4, column=12)
        parser_state = make_parser_state([token], pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "NULL_LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 4)
        self.assertEqual(result["column"], 12)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_grouping_expr(self):
        """测试解析括号表达式"""
        left_paren = make_token("LEFT_PAREN", "(", line=1, column=1)
        parser_state = make_parser_state([left_paren], pos=0)

        expected_ast = {
            "type": "GROUPING",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch("._parse_grouping_expr_package._parse_grouping_expr_src._parse_grouping_expr") as mock_grouping:
            mock_grouping.return_value = expected_ast
            result = _parse_primary_expr(parser_state)

        self.assertEqual(result, expected_ast)
        mock_grouping.assert_called_once_with(parser_state, left_paren)
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_array_literal(self):
        """测试解析数组字面量"""
        left_bracket = make_token("LEFT_BRACKET", "[", line=1, column=1)
        parser_state = make_parser_state([left_bracket], pos=0)

        expected_ast = {
            "type": "ARRAY_LITERAL",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch("._parse_array_literal_package._parse_array_literal_src._parse_array_literal") as mock_array:
            mock_array.return_value = expected_ast
            result = _parse_primary_expr(parser_state)

        self.assertEqual(result, expected_ast)
        mock_array.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_dict_literal(self):
        """测试解析字典字面量"""
        left_brace = make_token("LEFT_BRACE", "{", line=1, column=1)
        parser_state = make_parser_state([left_brace], pos=0)

        expected_ast = {
            "type": "DICT_LITERAL",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch("._parse_dict_literal_package._parse_dict_literal_src._parse_dict_literal") as mock_dict:
            mock_dict.return_value = expected_ast
            result = _parse_primary_expr(parser_state)

        self.assertEqual(result, expected_ast)
        mock_dict.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)

    def test_unexpected_end_of_input(self):
        """测试输入结束时的异常"""
        parser_state = make_parser_state([], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unexpected_token(self):
        """测试意外 token 的异常"""
        token = make_token("PLUS", "+", line=5, column=20)
        parser_state = make_parser_state([token], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("line 5", str(context.exception))
        self.assertIn("column 20", str(context.exception))

    def test_pos_at_end_of_tokens(self):
        """测试 pos 等于 tokens 长度时的异常"""
        token = make_token("IDENTIFIER", "x")
        parser_state = make_parser_state([token], pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_beyond_tokens_length(self):
        """测试 pos 超出 tokens 长度时的异常"""
        token = make_token("IDENTIFIER", "x")
        parser_state = make_parser_state([token], pos=5)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_multiple_tokens_only_consumes_one(self):
        """测试多个 token 时只消费一个"""
        tokens = [
            make_token("IDENTIFIER", "first", line=1, column=1),
            make_token("NUMBER", "123", line=1, column=10),
            make_token("STRING", '"text"', line=2, column=1)
        ]
        parser_state = make_parser_state(tokens, pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "first")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_from_middle_position(self):
        """测试从中间位置开始解析"""
        tokens = [
            make_token("PLUS", "+", line=1, column=1),
            make_token("IDENTIFIER", "middle", line=1, column=5),
            make_token("MINUS", "-", line=1, column=15)
        ]
        parser_state = make_parser_state(tokens, pos=1)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "middle")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()
