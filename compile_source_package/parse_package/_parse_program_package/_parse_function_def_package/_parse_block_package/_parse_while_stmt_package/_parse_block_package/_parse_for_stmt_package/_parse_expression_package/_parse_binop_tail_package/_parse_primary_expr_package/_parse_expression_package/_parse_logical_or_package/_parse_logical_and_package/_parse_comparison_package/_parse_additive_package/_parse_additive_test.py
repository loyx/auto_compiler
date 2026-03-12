# -*- coding: utf-8 -*-
"""
单元测试：_parse_additive 函数
测试加法/减法表达式解析器的行为
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测试模块
import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.join(os.path.dirname(__file__), '../../../../../../../../../../../../..')
sys.path.insert(0, project_root)

from main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """_parse_additive 函数的测试用例类"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助方法：创建测试用的 Token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """辅助方法：创建测试用的 AST 节点"""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    def test_simple_addition(self):
        """测试简单加法表达式：a + b"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Mock _parse_multiplicative 返回不同的 AST 节点
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value="a", line=1, column=1),
                self._create_ast_node("IDENTIFIER", value="b", line=1, column=5),
            ]

            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(parser_state["pos"], 3)  # 所有 token 都被消耗

    def test_simple_subtraction(self):
        """测试简单减法表达式：x - y"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("MINUS", "-", 1, 3),
            self._create_token("IDENTIFIER", "y", 1, 5),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_binop_tail_package._parse_primary_expr_package._parse_expression_package._parse_logical_or_package._parse_logical_and_package._parse_comparison_package._parse_additive_package._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value="x", line=1, column=1),
                self._create_ast_node("IDENTIFIER", value="y", line=1, column=5),
            ]

            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)

    def test_left_associativity(self):
        """测试左结合性：a + b - c 应该解析为 (a + b) - c"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("MINUS", "-", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value="a", line=1, column=1),
                self._create_ast_node("IDENTIFIER", value="b", line=1, column=5),
                self._create_ast_node("IDENTIFIER", value="c", line=1, column=9),
            ]

            result = _parse_additive(parser_state)

            # 最外层应该是减法操作
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)

            # 左子节点应该是加法操作
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "+")
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")

            # 右子节点应该是 c
            right_child = result["children"][1]
            self.assertEqual(right_child["value"], "c")

    def test_no_operator(self):
        """测试没有运算符的情况：只解析单个操作数"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        expected_node = self._create_ast_node("IDENTIFIER", value="x", line=1, column=1)

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.return_value = expected_node

            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 0)  # pos 没有被推进

    def test_missing_right_operand(self):
        """测试运算符后缺少操作数的错误情况：a +"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            # 第一次调用返回左操作数
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value="a", line=1, column=1),
                # 第二次调用设置错误状态
                lambda state: state.update({"error": "Unexpected end"}) or self._create_ast_node("ERROR", value="Unexpected end"),
            ]

            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "ERROR")
            self.assertIn("Expected operand after +", result["value"])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)

    def test_error_propagation_from_multiplicative(self):
        """测试从 _parse_multiplicative 传播的错误"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "Previous error"
        }

        error_node = self._create_ast_node("ERROR", value="Previous error", line=1, column=1)

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.return_value = error_node

            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Previous error")

    def test_multiple_additions(self):
        """测试多个加法：a + b + c + d"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("PLUS", "+", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("PLUS", "+", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        identifiers = ["a", "b", "c", "d"]
        columns = [1, 5, 9, 13]

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value=identifiers[i], line=1, column=columns[i])
                for i in range(4)
            ]

            result = _parse_additive(parser_state)

            # 验证最外层是最后一个加法
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["column"], 11)

            # 验证左子树包含前面的所有加法
            leftmost = result["children"][0]
            while leftmost["type"] == "BINARY_OP":
                if leftmost["children"][0]["type"] != "BINARY_OP":
                    break
                leftmost = leftmost["children"][0]

            self.assertEqual(leftmost["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "d")

    def test_mixed_addition_subtraction(self):
        """测试混合加减法：a - b + c"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("MINUS", "-", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("PLUS", "+", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value="a", line=1, column=1),
                self._create_ast_node("IDENTIFIER", value="b", line=1, column=5),
                self._create_ast_node("IDENTIFIER", value="c", line=1, column=9),
            ]

            result = _parse_additive(parser_state)

            # 最外层应该是加法（最后执行的运算）
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["column"], 7)

            # 左子节点应该是减法
            left_child = result["children"][0]
            self.assertEqual(left_child["operator"], "-")
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")

    def test_position_tracking(self):
        """测试位置追踪：确保 pos 正确更新"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("PLUS", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("MINUS", "-", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.side_effect = [
                self._create_ast_node("IDENTIFIER", value="a", line=1, column=1),
                self._create_ast_node("IDENTIFIER", value="b", line=1, column=5),
                self._create_ast_node("IDENTIFIER", value="c", line=1, column=9),
            ]

            result = _parse_additive(parser_state)

            # 所有 5 个 token 都应该被消耗
            self.assertEqual(parser_state["pos"], 5)

    def test_empty_tokens(self):
        """测试空 token 列表的情况"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative") as mock_multi:
            mock_multi.return_value = self._create_ast_node("EMPTY", value=None)

            result = _parse_additive(parser_state)

            self.assertEqual(result["type"], "EMPTY")
            self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()
