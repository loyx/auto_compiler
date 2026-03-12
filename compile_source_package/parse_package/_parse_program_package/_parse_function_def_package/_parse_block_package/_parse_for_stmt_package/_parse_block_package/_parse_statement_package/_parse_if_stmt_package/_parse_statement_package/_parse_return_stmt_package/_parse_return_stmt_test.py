# -*- coding: utf-8 -*-
"""
单元测试：_parse_return_stmt 函数
测试 return 语句解析功能
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List


# 相对导入被测模块
from ._parse_return_stmt_src import _parse_return_stmt


class TestParseReturnStmt(unittest.TestCase):
    """_parse_return_stmt 函数测试类"""

    def _create_parser_state(
        self,
        tokens: List[Dict[str, Any]],
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_return_without_expression(self):
        """测试无表达式的 return 语句：return;"""
        tokens = [
            self._create_token("RETURN", "return", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=8)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Mock _expect_token 来模拟消耗 token
        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ) as mock_expect:
            result = _parse_return_stmt(parser_state)

        # 验证 AST 节点结构
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["value"], "return")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])

        # 验证 _expect_token 被调用两次 (RETURN 和 SEMICOLON)
        self.assertEqual(mock_expect.call_count, 2)
        mock_expect.assert_any_call(parser_state, "RETURN")

    def test_return_with_expression(self):
        """测试有表达式的 return 语句：return x + 1;"""
        tokens = [
            self._create_token("RETURN", "return", line=2, column=5),
            self._create_token("IDENTIFIER", "x", line=2, column=12),
            self._create_token("PLUS", "+", line=2, column=14),
            self._create_token("NUMBER", "1", line=2, column=16),
            self._create_token("SEMICOLON", ";", line=2, column=17)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Mock expression AST
        mock_expr_ast = {
            "type": "BINARY_EXPR",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "NUMBER", "value": "1"}
            ],
            "line": 2,
            "column": 12
        }

        # Mock _expect_token 和 _parse_expression
        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ) as mock_expect:
            with patch(
                "._parse_return_stmt_package._parse_return_stmt_src._parse_expression",
                return_value=mock_expr_ast
            ) as mock_parse_expr:
                result = _parse_return_stmt(parser_state)

        # 验证 AST 节点结构
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["value"], "return")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_expr_ast)

        # 验证 _parse_expression 被调用
        mock_parse_expr.assert_called_once()

        # 验证 _expect_token 被调用两次
        self.assertEqual(mock_expect.call_count, 2)

    def test_return_with_complex_expression(self):
        """测试复杂表达式的 return 语句：return func(a, b);"""
        tokens = [
            self._create_token("RETURN", "return", line=3, column=1),
            self._create_token("IDENTIFIER", "func", line=3, column=8),
            self._create_token("LPAREN", "(", line=3, column=12),
            self._create_token("IDENTIFIER", "a", line=3, column=13),
            self._create_token("COMMA", ",", line=3, column=14),
            self._create_token("IDENTIFIER", "b", line=3, column=16),
            self._create_token("RPAREN", ")", line=3, column=17),
            self._create_token("SEMICOLON", ";", line=3, column=18)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_expr_ast = {
            "type": "CALL_EXPR",
            "value": "func",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "IDENTIFIER", "value": "b"}
            ],
            "line": 3,
            "column": 8
        }

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ):
            with patch(
                "._parse_return_stmt_package._parse_return_stmt_src._parse_expression",
                return_value=mock_expr_ast
            ):
                result = _parse_return_stmt(parser_state)

        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["children"][0]["type"], "CALL_EXPR")
        self.assertEqual(result["children"][0]["value"], "func")

    def test_return_statement_position_update(self):
        """测试 parser_state 位置更新"""
        tokens = [
            self._create_token("RETURN", "return", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=8)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        call_count = [0]

        def mock_expect_side_effect(state, token_type):
            call_count[0] += 1
            return {**state, "pos": state["pos"] + 1}

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=mock_expect_side_effect
        ):
            _parse_return_stmt(parser_state)

        # 应该消耗两个 token: RETURN 和 SEMICOLON
        self.assertEqual(call_count[0], 2)

    def test_return_at_different_positions(self):
        """测试 return 在不同位置的解析"""
        # return 在文件中间位置
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("ASSIGN", "=", line=1, column=3),
            self._create_token("NUMBER", "5", line=1, column=5),
            self._create_token("SEMICOLON", ";", line=1, column=6),
            self._create_token("RETURN", "return", line=2, column=1),
            self._create_token("IDENTIFIER", "x", line=2, column=8),
            self._create_token("SEMICOLON", ";", line=2, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=4)

        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 2,
            "column": 8
        }

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ):
            with patch(
                "._parse_return_stmt_package._parse_return_stmt_src._parse_expression",
                return_value=mock_expr_ast
            ):
                result = _parse_return_stmt(parser_state)

        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 1)

    def test_return_with_literal_expression(self):
        """测试返回字面量的 return 语句：return 42;"""
        tokens = [
            self._create_token("RETURN", "return", line=1, column=1),
            self._create_token("NUMBER", "42", line=1, column=8),
            self._create_token("SEMICOLON", ";", line=1, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_expr_ast = {
            "type": "NUMBER_LITERAL",
            "value": "42",
            "line": 1,
            "column": 8
        }

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ):
            with patch(
                "._parse_return_stmt_package._parse_return_stmt_src._parse_expression",
                return_value=mock_expr_ast
            ):
                result = _parse_return_stmt(parser_state)

        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["value"], "42")

    def test_return_with_string_literal(self):
        """测试返回字符串的 return 语句：return "hello";"""
        tokens = [
            self._create_token("RETURN", "return", line=1, column=1),
            self._create_token("STRING", '"hello"', line=1, column=8),
            self._create_token("SEMICOLON", ";", line=1, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_expr_ast = {
            "type": "STRING_LITERAL",
            "value": '"hello"',
            "line": 1,
            "column": 8
        }

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ):
            with patch(
                "._parse_return_stmt_package._parse_return_stmt_src._parse_expression",
                return_value=mock_expr_ast
            ):
                result = _parse_return_stmt(parser_state)

        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["children"][0]["type"], "STRING_LITERAL")

    def test_return_preserves_token_info(self):
        """测试 return 语句保留原始 token 的行号和列号"""
        tokens = [
            self._create_token("RETURN", "return", line=10, column=25),
            self._create_token("SEMICOLON", ";", line=10, column=32)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ):
            result = _parse_return_stmt(parser_state)

        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    def test_return_multiple_statements_sequence(self):
        """测试多个 return 语句序列中的单个解析"""
        tokens = [
            self._create_token("RETURN", "return", line=1, column=1),
            self._create_token("NUMBER", "1", line=1, column=8),
            self._create_token("SEMICOLON", ";", line=1, column=9),
            self._create_token("RETURN", "return", line=2, column=1),
            self._create_token("NUMBER", "2", line=2, column=8),
            self._create_token("SEMICOLON", ";", line=2, column=9)
        ]
        # 解析第一个 return
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_expr_ast_1 = {"type": "NUMBER_LITERAL", "value": "1"}

        with patch(
            "._parse_return_stmt_package._parse_return_stmt_src._expect_token",
            side_effect=lambda state, token_type: {
                **state,
                "pos": state["pos"] + 1
            }
        ):
            with patch(
                "._parse_return_stmt_package._parse_return_stmt_src._parse_expression",
                return_value=mock_expr_ast_1
            ):
                result = _parse_return_stmt(parser_state)

        self.assertEqual(result["children"][0]["value"], "1")


if __name__ == "__main__":
    unittest.main()
