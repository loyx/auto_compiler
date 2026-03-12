# -*- coding: utf-8 -*-
"""
单元测试：_get_precedence 函数
测试运算符优先级查询功能
"""
import unittest
from ._get_precedence_src import _get_precedence


class TestGetPrecedence(unittest.TestCase):
    """_get_precedence 函数的测试用例"""

    def test_logical_or_operator(self):
        """测试逻辑或运算符 || 优先级为 1"""
        result = _get_precedence("OPERATOR", "||")
        self.assertEqual(result, 1)

    def test_logical_and_operator(self):
        """测试逻辑与运算符 && 优先级为 2"""
        result = _get_precedence("OPERATOR", "&&")
        self.assertEqual(result, 2)

    def test_equality_operators(self):
        """测试相等运算符 == 和 != 优先级为 3"""
        self.assertEqual(_get_precedence("OPERATOR", "=="), 3)
        self.assertEqual(_get_precedence("OPERATOR", "!="), 3)

    def test_relational_operators(self):
        """测试关系运算符 < > <= >= 优先级为 4"""
        self.assertEqual(_get_precedence("OPERATOR", "<"), 4)
        self.assertEqual(_get_precedence("OPERATOR", ">"), 4)
        self.assertEqual(_get_precedence("OPERATOR", "<="), 4)
        self.assertEqual(_get_precedence("OPERATOR", ">="), 4)

    def test_addition_subtraction_operators(self):
        """测试加减运算符 + - 优先级为 5"""
        self.assertEqual(_get_precedence("OPERATOR", "+"), 5)
        self.assertEqual(_get_precedence("OPERATOR", "-"), 5)

    def test_multiplication_division_operators(self):
        """测试乘除运算符 * / 优先级为 6"""
        self.assertEqual(_get_precedence("OPERATOR", "*"), 6)
        self.assertEqual(_get_precedence("OPERATOR", "/"), 6)

    def test_non_operator_token_type(self):
        """测试非 OPERATOR 类型的 token 返回 0"""
        test_cases = [
            ("IDENTIFIER", "+"),
            ("NUMBER", "5"),
            ("STRING", "hello"),
            ("KEYWORD", "if"),
            ("", "+"),
        ]
        for token_type, token_value in test_cases:
            with self.subTest(token_type=token_type, token_value=token_value):
                result = _get_precedence(token_type, token_value)
                self.assertEqual(result, 0)

    def test_unknown_operator_value(self):
        """测试未知的运算符值返回 0"""
        unknown_operators = ["%", "**", "//", "<<", ">>", "&", "|", "^", "~", "="]
        for op in unknown_operators:
            with self.subTest(operator=op):
                result = _get_precedence("OPERATOR", op)
                self.assertEqual(result, 0)

    def test_empty_token_value(self):
        """测试空字符串 token_value 返回 0"""
        result = _get_precedence("OPERATOR", "")
        self.assertEqual(result, 0)

    def test_case_sensitivity(self):
        """测试运算符区分大小写"""
        # 小写运算符不应匹配
        self.assertEqual(_get_precedence("OPERATOR", "and"), 0)
        self.assertEqual(_get_precedence("OPERATOR", "or"), 0)
        self.assertEqual(_get_precedence("OPERATOR", "And"), 0)

    def test_all_priority_levels(self):
        """测试所有优先级级别 (0-6) 都有覆盖"""
        priorities = set()
        test_cases = [
            ("OPERATOR", "||"),
            ("OPERATOR", "&&"),
            ("OPERATOR", "=="),
            ("OPERATOR", "<"),
            ("OPERATOR", "+"),
            ("OPERATOR", "*"),
            ("IDENTIFIER", "x"),  # 非运算符
        ]
        for token_type, token_value in test_cases:
            priorities.add(_get_precedence(token_type, token_value))
        
        # 验证覆盖了 0, 1, 2, 3, 4, 5, 6 所有优先级
        self.assertEqual(priorities, {0, 1, 2, 3, 4, 5, 6})


if __name__ == "__main__":
    unittest.main()
