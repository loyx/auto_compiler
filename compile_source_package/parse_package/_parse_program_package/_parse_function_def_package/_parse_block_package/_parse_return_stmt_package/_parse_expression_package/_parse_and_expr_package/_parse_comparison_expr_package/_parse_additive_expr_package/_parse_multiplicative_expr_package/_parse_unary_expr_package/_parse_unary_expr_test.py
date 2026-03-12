# -*- coding: utf-8 -*-
"""单元测试：_parse_unary_expr 函数"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """_parse_unary_expr 函数的单元测试类"""

    def setUp(self) -> None:
        """测试前准备"""
        pass

    def tearDown(self) -> None:
        """测试后清理"""
        pass

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    # ==================== Happy Path ====================

    def test_parse_unary_minus(self) -> None:
        """测试解析一元减号运算符：-x"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Mock _parse_primary_expr 来返回标识符节点
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            # 验证返回的 AST 节点
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][0]["value"], "x")

            # 验证 pos 被正确更新
            self.assertEqual(parser_state["pos"], 1)

            # 验证 _parse_primary_expr 被调用
            mock_primary.assert_called_once()

    def test_parse_unary_plus(self) -> None:
        """测试解析一元加号运算符：+value"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("IDENTIFIER", "value", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "value",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

    def test_parse_unary_bang(self) -> None:
        """测试解析逻辑非运算符：!flag"""
        tokens = [
            self._create_token("BANG", "!", 1, 1),
            self._create_token("IDENTIFIER", "flag", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "flag",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")

    def test_parse_unary_tilde(self) -> None:
        """测试解析按位取反运算符：~mask"""
        tokens = [
            self._create_token("TILDE", "~", 1, 1),
            self._create_token("IDENTIFIER", "mask", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "mask",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "~")

    def test_parse_chained_unary_operators(self) -> None:
        """测试解析链式一元运算符：--x"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("MINUS", "-", 1, 2),
            self._create_token("IDENTIFIER", "x", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 需要模拟 _parse_primary_expr 在递归调用中被调用
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 3
            }

            result = _parse_unary_expr(parser_state)

            # 外层 UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

            # 内层 UNARY_OP
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "UNARY_OP")
            self.assertEqual(inner_node["value"], "-")
            self.assertEqual(inner_node["line"], 1)
            self.assertEqual(inner_node["column"], 2)

            # 最内层 IDENTIFIER
            self.assertEqual(inner_node["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(inner_node["children"][0]["value"], "x")

            # 验证 pos 被正确更新到 2
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_no_unary_operator_delegates_to_primary(self) -> None:
        """测试当没有一元运算符时委托给 _parse_primary_expr"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("PLUS", "+", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        expected_primary_result = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = expected_primary_result

            result = _parse_unary_expr(parser_state)

            # 验证直接返回 _parse_primary_expr 的结果
            self.assertEqual(result, expected_primary_result)

            # 验证 _parse_primary_expr 被调用
            mock_primary.assert_called_once()

            # 验证 pos 没有被修改（因为不是一元运算符）
            self.assertEqual(parser_state["pos"], 0)

    # ==================== Boundary Cases ====================

    def test_empty_tokens_raises_syntax_error(self) -> None:
        """测试空 tokens 列表抛出 SyntaxError"""
        parser_state = self._create_parser_state(tokens=[], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_at_end_raises_syntax_error(self) -> None:
        """测试 pos 在 tokens 末尾时抛出 SyntaxError"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unary_operator_at_end_raises_error(self) -> None:
        """测试一元运算符后没有操作数时抛出错误"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # _parse_primary_expr 在空输入时会抛出 SyntaxError
        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.side_effect = SyntaxError("Unexpected end of input")

            with self.assertRaises(SyntaxError):
                _parse_unary_expr(parser_state)

    # ==================== Branch Coverage ====================

    def test_all_unary_operator_types(self) -> None:
        """测试所有一元运算符类型"""
        unary_ops = [
            ("PLUS", "+"),
            ("MINUS", "-"),
            ("BANG", "!"),
            ("TILDE", "~")
        ]

        for op_type, op_value in unary_ops:
            with self.subTest(op_type=op_type, op_value=op_value):
                tokens = [
                    self._create_token(op_type, op_value, 1, 1),
                    self._create_token("NUMBER", "42", 1, 2)
                ]
                parser_state = self._create_parser_state(tokens, pos=0)

                with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
                    mock_primary.return_value = {
                        "type": "NUMBER",
                        "children": [],
                        "value": "42",
                        "line": 1,
                        "column": 2
                    }

                    result = _parse_unary_expr(parser_state)

                    self.assertEqual(result["type"], "UNARY_OP")
                    self.assertEqual(result["value"], op_value)
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 1)

    def test_non_unary_operator_types(self) -> None:
        """测试非一元运算符类型委托给 _parse_primary_expr"""
        non_unary_types = ["IDENTIFIER", "NUMBER", "STRING", "LPAREN", "TRUE", "FALSE", "NULL"]

        for token_type in non_unary_types:
            with self.subTest(token_type=token_type):
                tokens = [self._create_token(token_type, "value", 1, 1)]
                parser_state = self._create_parser_state(tokens, pos=0)

                expected_result = {
                    "type": token_type,
                    "children": [],
                    "value": "value",
                    "line": 1,
                    "column": 1
                }

                with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
                    mock_primary.return_value = expected_result

                    result = _parse_unary_expr(parser_state)

                    self.assertEqual(result, expected_result)
                    mock_primary.assert_called()

    # ==================== Position and State Updates ====================

    def test_position_updated_correctly_after_consuming_operator(self) -> None:
        """测试消费运算符后 pos 正确更新"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2),
            self._create_token("PLUS", "+", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            _parse_unary_expr(parser_state)

            # 消费了 MINUS token，pos 应该从 0 变为 1
            self.assertEqual(parser_state["pos"], 1)

    def test_position_not_changed_when_no_unary_operator(self) -> None:
        """测试没有一元运算符时 pos 不变"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("MINUS", "-", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 1
            }

            _parse_unary_expr(parser_state)

            # 没有消费 token，pos 应该保持为 0
            self.assertEqual(parser_state["pos"], 0)

    # ==================== AST Structure Verification ====================

    def test_unary_op_ast_structure(self) -> None:
        """测试 UNARY_OP AST 节点结构完整性"""
        tokens = [
            self._create_token("BANG", "!", 5, 10),
            self._create_token("IDENTIFIER", "flag", 5, 11)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "flag",
                "line": 5,
                "column": 11
            }

            result = _parse_unary_expr(parser_state)

            # 验证所有必需字段存在
            self.assertIn("type", result)
            self.assertIn("children", result)
            self.assertIn("value", result)
            self.assertIn("line", result)
            self.assertIn("column", result)

            # 验证字段值
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_unary_op_preserves_source_location(self) -> None:
        """测试一元运算符保留源代码位置信息"""
        test_cases = [
            (1, 1),
            (10, 5),
            (100, 50),
            (1, 100)
        ]

        for line, column in test_cases:
            with self.subTest(line=line, column=column):
                tokens = [
                    self._create_token("MINUS", "-", line, column),
                    self._create_token("NUMBER", "0", line, column + 1)
                ]
                parser_state = self._create_parser_state(tokens, pos=0)

                with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
                    mock_primary.return_value = {
                        "type": "NUMBER",
                        "children": [],
                        "value": "0",
                        "line": line,
                        "column": column + 1
                    }

                    result = _parse_unary_expr(parser_state)

                    self.assertEqual(result["line"], line)
                    self.assertEqual(result["column"], column)


if __name__ == "__main__":
    unittest.main()
