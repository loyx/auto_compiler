#!/usr/bin/env python3
"""
单元测试文件：_handle_atom_token 函数测试
测试原子表达式 token 分发逻辑
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_atom_token_src import _handle_atom_token


class TestHandleAtomToken(unittest.TestCase):
    """_handle_atom_token 函数的单元测试类"""

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """辅助函数：创建测试用的 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, pos: int = 0) -> Dict[str, Any]:
        """辅助函数：创建测试用的 parser_state 字典"""
        return {
            "tokens": [],
            "pos": pos,
            "filename": "test.py"
        }

    # ==================== Happy Path Tests ====================

    def test_handle_identifier_token(self):
        """测试 IDENTIFIER token 处理"""
        token = self._create_token("IDENTIFIER", "my_var", line=5, column=10)
        parser_state = self._create_parser_state(pos=3)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "my_var")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 4)

    def test_handle_number_token(self):
        """测试 NUMBER token 处理"""
        token = self._create_token("NUMBER", "3.14", line=2, column=5)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "3.14")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_integer_token(self):
        """测试 INTEGER token 处理"""
        token = self._create_token("INTEGER", "42", line=1, column=1)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_string_token(self):
        """测试 STRING token 处理"""
        token = self._create_token("STRING", '"hello world"', line=3, column=8)
        parser_state = self._create_parser_state(pos=5)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello world"')
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 8)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 6)

    def test_handle_true_token(self):
        """测试 TRUE token 处理"""
        token = self._create_token("TRUE", "true", line=10, column=15)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 15)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_false_token(self):
        """测试 FALSE token 处理"""
        token = self._create_token("FALSE", "false", line=7, column=20)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 7)
        self.assertEqual(result["column"], 20)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_none_token(self):
        """测试 NONE token 处理"""
        token = self._create_token("NONE", "None", line=4, column=12)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 4)
        self.assertEqual(result["column"], 12)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_null_token(self):
        """测试 NULL token 处理"""
        token = self._create_token("NULL", "null", line=6, column=18)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 6)
        self.assertEqual(result["column"], 18)

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Error Handling Tests ====================

    def test_handle_unsupported_token_type(self):
        """测试不支持的 token 类型处理"""
        token = self._create_token("LPAREN", "(", line=1, column=1)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 ERROR 节点
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "(")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证错误信息被设置
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "Unexpected token: LPAREN")

        # 验证 pos 未被消费（不支持的 token 不消费）
        self.assertEqual(parser_state["pos"], 0)

    def test_handle_unknown_token_type(self):
        """测试未知 token 类型处理"""
        token = self._create_token("UNKNOWN_TYPE", "???", line=99, column=99)
        parser_state = self._create_parser_state(pos=10)

        result = _handle_atom_token(token, parser_state)

        # 验证 ERROR 节点
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "???")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 99)
        self.assertEqual(result["column"], 99)

        # 验证错误信息被设置
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "Unexpected token: UNKNOWN_TYPE")

        # 验证 pos 未被消费
        self.assertEqual(parser_state["pos"], 10)

    # ==================== Boundary Value Tests ====================

    def test_handle_token_with_missing_fields(self):
        """测试 token 缺少某些字段的情况"""
        token = {"type": "IDENTIFIER"}  # 缺少 value, line, column
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证使用默认值
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])

        # 验证 token 被消费
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_empty_parser_state(self):
        """测试空的 parser_state"""
        token = self._create_token("NUMBER", "0")
        parser_state = {}  # 空的 dict

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点正常创建
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "0")

        # 验证 pos 被设置
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_token_with_zero_position(self):
        """测试 token 在位置 0 的情况"""
        token = self._create_token("STRING", '""', line=1, column=1)
        parser_state = self._create_parser_state(pos=0)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '""')

        # 验证 pos 从 0 增加到 1
        self.assertEqual(parser_state["pos"], 1)

    def test_handle_token_with_large_position(self):
        """测试 token 在大位置值的情况"""
        token = self._create_token("TRUE", "true", line=1000, column=500)
        parser_state = self._create_parser_state(pos=9999)

        result = _handle_atom_token(token, parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 1000)
        self.assertEqual(result["column"], 500)

        # 验证 pos 增加
        self.assertEqual(parser_state["pos"], 10000)

    # ==================== State Change Tests ====================

    def test_parser_state_pos_increment_multiple_calls(self):
        """测试多次调用时 pos 的递增"""
        parser_state = self._create_parser_state(pos=0)

        token1 = self._create_token("IDENTIFIER", "a")
        result1 = _handle_atom_token(token1, parser_state)
        self.assertEqual(parser_state["pos"], 1)

        token2 = self._create_token("NUMBER", "1")
        result2 = _handle_atom_token(token2, parser_state)
        self.assertEqual(parser_state["pos"], 2)

        token3 = self._create_token("STRING", '"test"')
        result3 = _handle_atom_token(token3, parser_state)
        self.assertEqual(parser_state["pos"], 3)

    def test_error_state_preserved_after_error(self):
        """测试错误状态在错误处理后保留"""
        token = self._create_token("OPERATOR", "+")
        parser_state = self._create_parser_state(pos=5)

        result = _handle_atom_token(token, parser_state)

        # 验证错误被设置
        self.assertEqual(parser_state["error"], "Unexpected token: OPERATOR")

        # 验证 pos 未变
        self.assertEqual(parser_state["pos"], 5)

    # ==================== AST Node Structure Tests ====================

    def test_ast_node_has_required_fields(self):
        """测试所有 AST 节点都有必需的字段"""
        test_cases = [
            ("IDENTIFIER", "var_name"),
            ("NUMBER", "123"),
            ("INTEGER", "456"),
            ("STRING", '"text"'),
            ("TRUE", "true"),
            ("FALSE", "false"),
            ("NONE", "None"),
            ("NULL", "null"),
        ]

        for token_type, value in test_cases:
            with self.subTest(token_type=token_type):
                token = self._create_token(token_type, value)
                parser_state = self._create_parser_state()
                result = _handle_atom_token(token, parser_state)

                # 验证所有必需字段存在
                self.assertIn("type", result)
                self.assertIn("value", result)
                self.assertIn("children", result)
                self.assertIn("line", result)
                self.assertIn("column", result)

                # 验证 children 是列表
                self.assertIsInstance(result["children"], list)
                self.assertEqual(len(result["children"]), 0)

    def test_error_node_structure(self):
        """测试 ERROR 节点结构"""
        token = self._create_token("INVALID", "x")
        parser_state = self._create_parser_state()

        result = _handle_atom_token(token, parser_state)

        # 验证 ERROR 节点结构
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "x")
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)
        self.assertIn("line", result)
        self.assertIn("column", result)


if __name__ == "__main__":
    unittest.main()
