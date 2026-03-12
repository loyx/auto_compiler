# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._is_binary_operator_src import _is_binary_operator

# === Test Helper Types ===
Token = Dict[str, Any]


# === Test Cases ===
class TestIsBinaryOperator(unittest.TestCase):
    """测试 _is_binary_operator 函数的正确性"""

    def test_star_star_operator(self):
        """测试 STAR_STAR (**) 运算符"""
        token: Token = {"type": "STAR_STAR", "value": "**", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_star_operator(self):
        """测试 STAR (*) 运算符"""
        token: Token = {"type": "STAR", "value": "*", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_slash_operator(self):
        """测试 SLASH (/) 运算符"""
        token: Token = {"type": "SLASH", "value": "/", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_percent_operator(self):
        """测试 PERCENT (%) 运算符"""
        token: Token = {"type": "PERCENT", "value": "%", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_plus_operator(self):
        """测试 PLUS (+) 运算符"""
        token: Token = {"type": "PLUS", "value": "+", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_minus_operator(self):
        """测试 MINUS (-) 运算符"""
        token: Token = {"type": "MINUS", "value": "-", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_equal_equal_operator(self):
        """测试 EQUAL_EQUAL (==) 运算符"""
        token: Token = {"type": "EQUAL_EQUAL", "value": "==", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_bang_equal_operator(self):
        """测试 BANG_EQUAL (!=) 运算符"""
        token: Token = {"type": "BANG_EQUAL", "value": "!=", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_less_operator(self):
        """测试 LESS (<) 运算符"""
        token: Token = {"type": "LESS", "value": "<", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_greater_operator(self):
        """测试 GREATER (>) 运算符"""
        token: Token = {"type": "GREATER", "value": ">", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_less_equal_operator(self):
        """测试 LESS_EQUAL (<=) 运算符"""
        token: Token = {"type": "LESS_EQUAL", "value": "<=", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_greater_equal_operator(self):
        """测试 GREATER_EQUAL (>=) 运算符"""
        token: Token = {"type": "GREATER_EQUAL", "value": ">=", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_and_operator(self):
        """测试 AND 运算符"""
        token: Token = {"type": "AND", "value": "and", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_or_operator(self):
        """测试 OR 运算符"""
        token: Token = {"type": "OR", "value": "or", "line": 1, "column": 1}
        self.assertTrue(_is_binary_operator(token))

    def test_none_token(self):
        """测试 None 输入返回 False"""
        self.assertFalse(_is_binary_operator(None))

    def test_non_binary_operator_type(self):
        """测试非二元运算符类型返回 False"""
        token: Token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_number_token(self):
        """测试数字 token 返回 False"""
        token: Token = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_string_token(self):
        """测试字符串 token 返回 False"""
        token: Token = {"type": "STRING", "value": "hello", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_keyword_token(self):
        """测试关键字 token 返回 False"""
        token: Token = {"type": "IF", "value": "if", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_empty_dict_token(self):
        """测试空字典 token 返回 False"""
        token: Token = {}
        self.assertFalse(_is_binary_operator(token))

    def test_token_without_type_key(self):
        """测试缺少 type 键的 token 返回 False"""
        token: Token = {"value": "test", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_unknown_operator_type(self):
        """测试未知运算符类型返回 False"""
        token: Token = {"type": "UNKNOWN_OP", "value": "??", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_case_sensitivity(self):
        """测试类型名称大小写敏感"""
        token: Token = {"type": "plus", "value": "+", "line": 1, "column": 1}
        self.assertFalse(_is_binary_operator(token))

    def test_token_with_extra_fields(self):
        """测试带有额外字段的 token 仍能正确识别"""
        token: Token = {
            "type": "PLUS",
            "value": "+",
            "line": 5,
            "column": 10,
            "extra_field": "ignored"
        }
        self.assertTrue(_is_binary_operator(token))


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
