# -*- coding: utf-8 -*-
"""
单元测试文件：_build_binary_op
测试目标：验证二元操作 AST 节点构建函数的正确性
"""

import unittest
from typing import Any, Dict

from ._build_binary_op_src import _build_binary_op


class TestBuildBinaryOp(unittest.TestCase):
    """测试 _build_binary_op 函数"""

    def _create_ast_node(self, node_type: str, value: Any = None, line: int = 1, column: int = 1) -> Dict:
        """辅助函数：创建 AST 节点"""
        node = {
            "type": node_type,
            "children": [],
            "line": line,
            "column": column
        }
        if value is not None:
            node["value"] = value
        return node

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict:
        """辅助函数：创建 Token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_build_binary_op_basic(self):
        """测试基本功能：构建加法操作节点"""
        left = self._create_ast_node("LITERAL", 5, line=1, column=1)
        right = self._create_ast_node("LITERAL", 3, line=1, column=5)
        op_token = self._create_token("PLUS", "+", line=1, column=3)

        result = _build_binary_op(left, right, op_token)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertIs(result["children"][0], left)
        self.assertIs(result["children"][1], right)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_build_binary_op_different_operators(self):
        """测试不同运算符：减法、乘法、除法"""
        left = self._create_ast_node("IDENTIFIER", "x")
        right = self._create_ast_node("IDENTIFIER", "y")

        operators = [
            ("MINUS", "-"),
            ("STAR", "*"),
            ("SLASH", "/"),
            ("PERCENT", "%"),
        ]

        for token_type, op_value in operators:
            with self.subTest(operator=op_value):
                op_token = self._create_token(token_type, op_value)
                result = _build_binary_op(left, right, op_token)

                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], op_value)
                self.assertEqual(len(result["children"]), 2)

    def test_build_binary_op_complex_operands(self):
        """测试复杂操作数：嵌套 AST 节点"""
        # 左操作数是一个二元操作节点
        left_inner_left = self._create_ast_node("LITERAL", 1)
        left_inner_right = self._create_ast_node("LITERAL", 2)
        left = _build_binary_op(left_inner_left, left_inner_right, self._create_token("PLUS", "+"))

        # 右操作数是一个标识符
        right = self._create_ast_node("IDENTIFIER", "z")

        op_token = self._create_token("STAR", "*")
        result = _build_binary_op(left, right, op_token)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "BINARY_OP")
        self.assertEqual(result["children"][0]["value"], "+")
        self.assertEqual(result["children"][1]["type"], "IDENTIFIER")

    def test_build_binary_op_position_from_left_operand(self):
        """测试位置信息：从右操作数继承位置"""
        left = self._create_ast_node("LITERAL", 10, line=5, column=10)
        right = self._create_ast_node("LITERAL", 20, line=5, column=15)
        op_token = self._create_token("PLUS", "+", line=5, column=13)

        result = _build_binary_op(left, right, op_token)

        # 位置应该来自左操作数
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_build_binary_op_preserves_operand_references(self):
        """测试引用保持：结果中的子节点是原对象的引用"""
        left = self._create_ast_node("LITERAL", 100)
        right = self._create_ast_node("LITERAL", 200)
        op_token = self._create_token("PLUS", "+")

        result = _build_binary_op(left, right, op_token)

        # 修改原节点应该反映在结果中（因为是引用）
        left["value"] = 999
        self.assertEqual(result["children"][0]["value"], 999)

        right["type"] = "MODIFIED"
        self.assertEqual(result["children"][1]["type"], "MODIFIED")

    def test_build_binary_op_various_ast_types(self):
        """测试不同 AST 类型作为操作数"""
        ast_types = [
            ("IDENTIFIER", "var_name"),
            ("LITERAL", 42),
            ("LITERAL", "string_value"),
            ("LITERAL", 3.14),
            ("LITERAL", True),
            ("LITERAL", None),
        ]

        for node_type, value in ast_types:
            with self.subTest(node_type=node_type, value=value):
                left = self._create_ast_node(node_type, value)
                right = self._create_ast_node("LITERAL", 0)
                op_token = self._create_token("PLUS", "+")

                result = _build_binary_op(left, right, op_token)

                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["children"][0]["type"], node_type)
                self.assertEqual(result["children"][0].get("value"), value)

    def test_build_binary_op_zero_position(self):
        """测试边界值：位置为 0"""
        left = self._create_ast_node("LITERAL", 0, line=0, column=0)
        right = self._create_ast_node("LITERAL", 1, line=0, column=1)
        op_token = self._create_token("PLUS", "+", line=0, column=0)

        result = _build_binary_op(left, right, op_token)

        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_build_binary_op_large_line_column_numbers(self):
        """测试边界值：大行号列号"""
        left = self._create_ast_node("LITERAL", 1, line=9999, column=999)
        right = self._create_ast_node("LITERAL", 2, line=9999, column=1000)
        op_token = self._create_token("PLUS", "+", line=9999, column=999)

        result = _build_binary_op(left, right, op_token)

        self.assertEqual(result["line"], 9999)
        self.assertEqual(result["column"], 999)

    def test_build_binary_op_empty_string_operator(self):
        """测试边界值：空字符串运算符"""
        left = self._create_ast_node("LITERAL", 1)
        right = self._create_ast_node("LITERAL", 2)
        op_token = self._create_token("UNKNOWN", "")

        result = _build_binary_op(left, right, op_token)

        self.assertEqual(result["value"], "")

    def test_build_binary_op_special_character_operators(self):
        """测试特殊字符运算符"""
        left = self._create_ast_node("LITERAL", 1)
        right = self._create_ast_node("LITERAL", 2)

        special_ops = ["**", "//", "<<", ">>", "&", "|", "^", "==", "!=", "<=", ">="]

        for op_char in special_ops:
            with self.subTest(operator=op_char):
                op_token = self._create_token("OP", op_char)
                result = _build_binary_op(left, right, op_token)

                self.assertEqual(result["value"], op_char)


if __name__ == "__main__":
    unittest.main()
