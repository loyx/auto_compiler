# -*- coding: utf-8 -*-
"""单元测试文件：_is_binary_operator"""

import unittest
from typing import Any, Dict

from ._is_binary_operator_src import _is_binary_operator

Token = Dict[str, Any]


class TestIsBinaryOperator(unittest.TestCase):
    """测试 _is_binary_operator 函数"""

    def test_keyword_and(self):
        """测试关键字 AND"""
        token: Token = {"type": "KEYWORD", "value": "AND"}
        self.assertTrue(_is_binary_operator(token))

    def test_keyword_or(self):
        """测试关键字 OR"""
        token: Token = {"type": "KEYWORD", "value": "OR"}
        self.assertTrue(_is_binary_operator(token))

    def test_keyword_case_sensitive(self):
        """测试关键字大小写敏感"""
        token_lower: Token = {"type": "KEYWORD", "value": "and"}
        token_upper: Token = {"type": "KEYWORD", "value": "And"}
        self.assertFalse(_is_binary_operator(token_lower))
        self.assertFalse(_is_binary_operator(token_upper))

    def test_comparison_operators(self):
        """测试比较运算符"""
        operators = ["==", "!=", "<", ">", "<=", ">="]
        for op in operators:
            token: Token = {"type": "OPERATOR", "value": op}
            self.assertTrue(_is_binary_operator(token), f"运算符 {op} 应该被识别为二元运算符")

    def test_arithmetic_operators(self):
        """测试算术运算符"""
        operators = ["+", "-", "*", "/"]
        for op in operators:
            token: Token = {"type": "OPERATOR", "value": op}
            self.assertTrue(_is_binary_operator(token), f"运算符 {op} 应该被识别为二元运算符")

    def test_non_binary_keyword(self):
        """测试非二元运算符的关键字"""
        keywords = ["IF", "ELSE", "WHILE", "FOR", "DEF", "RETURN"]
        for kw in keywords:
            token: Token = {"type": "KEYWORD", "value": kw}
            self.assertFalse(_is_binary_operator(token), f"关键字 {kw} 不应该被识别为二元运算符")

    def test_non_binary_operator(self):
        """测试非二元运算符的符号"""
        operators = ["=", "(", ")", "[", "]", ",", ";", ":"]
        for op in operators:
            token: Token = {"type": "OPERATOR", "value": op}
            self.assertFalse(_is_binary_operator(token), f"符号 {op} 不应该被识别为二元运算符")

    def test_identifier_token(self):
        """测试标识符 token"""
        token: Token = {"type": "IDENTIFIER", "value": "x"}
        self.assertFalse(_is_binary_operator(token))

    def test_number_token(self):
        """测试数字 token"""
        token: Token = {"type": "NUMBER", "value": "42"}
        self.assertFalse(_is_binary_operator(token))

    def test_string_token(self):
        """测试字符串 token"""
        token: Token = {"type": "STRING", "value": "hello"}
        self.assertFalse(_is_binary_operator(token))

    def test_empty_dict(self):
        """测试空字典"""
        token: Token = {}
        self.assertFalse(_is_binary_operator(token))

    def test_missing_type_field(self):
        """测试缺少 type 字段的 token"""
        token: Token = {"value": "AND"}
        self.assertFalse(_is_binary_operator(token))

    def test_missing_value_field(self):
        """测试缺少 value 字段的 token"""
        token: Token = {"type": "KEYWORD"}
        self.assertFalse(_is_binary_operator(token))

    def test_none_value(self):
        """测试 value 为 None 的 token"""
        token: Token = {"type": "KEYWORD", "value": None}
        self.assertFalse(_is_binary_operator(token))

    def test_none_type(self):
        """测试 type 为 None 的 token"""
        token: Token = {"type": None, "value": "AND"}
        self.assertFalse(_is_binary_operator(token))

    def test_token_with_position_info(self):
        """测试包含位置信息的 token"""
        token: Token = {
            "type": "KEYWORD",
            "value": "AND",
            "line": 10,
            "column": 5
        }
        self.assertTrue(_is_binary_operator(token))

    def test_operator_with_position_info(self):
        """测试包含位置信息的运算符 token"""
        token: Token = {
            "type": "OPERATOR",
            "value": "+",
            "line": 3,
            "column": 12
        }
        self.assertTrue(_is_binary_operator(token))

    def test_whitespace_value(self):
        """测试空白字符 value"""
        token: Token = {"type": "WHITESPACE", "value": " "}
        self.assertFalse(_is_binary_operator(token))

    def test_empty_string_value(self):
        """测试空字符串 value"""
        token: Token = {"type": "OPERATOR", "value": ""}
        self.assertFalse(_is_binary_operator(token))


if __name__ == "__main__":
    unittest.main()
