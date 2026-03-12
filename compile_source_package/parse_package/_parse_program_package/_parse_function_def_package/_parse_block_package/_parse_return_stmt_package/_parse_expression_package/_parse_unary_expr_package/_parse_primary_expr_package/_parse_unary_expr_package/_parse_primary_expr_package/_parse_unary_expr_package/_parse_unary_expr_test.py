# -*- coding: utf-8 -*-
"""单元测试：_parse_unary_expr 函数"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 相对导入被测试模块
from ._parse_unary_expr_src import _parse_unary_expr

# 类型别名
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseUnaryExpr(unittest.TestCase):
    """_parse_unary_expr 函数单元测试类"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: List[Token], pos: int = 0, filename: str = "test.cc") -> ParserState:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_minus_unary_operator(self):
        """测试 MINUS 一元运算符：-x"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "MINUS")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 2)
            self.assertNotIn("error", parser_state)

    def test_plus_unary_operator(self):
        """测试 PLUS 一元运算符：+x"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "PLUS")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 2)

    def test_not_unary_operator(self):
        """测试 NOT 一元运算符：!x"""
        tokens = [
            self._create_token("NOT", "!", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "NOT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 2)

    def test_bitwise_not_unary_operator(self):
        """测试 BITWISE_NOT 一元运算符：~x"""
        tokens = [
            self._create_token("BITWISE_NOT", "~", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "BITWISE_NOT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 2)

    def test_chained_unary_operators(self):
        """测试链式一元运算符：--x"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("MINUS", "-", 1, 2),
            self._create_token("IDENTIFIER", "x", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
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
            self.assertEqual(result["value"], "MINUS")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)

            # 内层 UNARY_OP
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "UNARY_OP")
            self.assertEqual(inner_node["value"], "MINUS")
            self.assertEqual(inner_node["line"], 1)
            self.assertEqual(inner_node["column"], 2)
            self.assertEqual(len(inner_node["children"]), 1)

            # 最内层 IDENTIFIER
            self.assertEqual(inner_node["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 3)

    def test_delegation_to_primary_expr(self):
        """测试非一元运算符时委托给 _parse_primary_expr"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("PLUS", "+", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        expected_ast = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = expected_ast

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result, expected_ast)
            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)  # pos 不应改变，由 _parse_primary_expr 处理

    def test_empty_tokens_error(self):
        """测试空 tokens 列表时的错误处理"""
        parser_state = self._create_parser_state([], 0)

        result = _parse_unary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_pos_beyond_tokens_length_error(self):
        """测试 pos 超出 tokens 长度时的错误处理"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens, 5)  # pos 超出长度

        result = _parse_unary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_error_propagation_from_operand(self):
        """测试操作数解析错误时的错误传播"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        error_ast = {
            "type": "ERROR",
            "children": [],
            "value": "Invalid expression",
            "line": 1,
            "column": 2
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            def set_error_and_return(state):
                state["error"] = "Invalid expression"
                return error_ast

            mock_primary.side_effect = set_error_and_return

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "ERROR")
            self.assertIn("error", parser_state)
            self.assertEqual(parser_state["error"], "Invalid expression")

    def test_unary_with_literal(self):
        """测试一元运算符作用于字面量：-42"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("NUMBER", "42", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": "42",
                "line": 1,
                "column": 2
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "MINUS")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 2)

    def test_triple_chained_unary_operators(self):
        """测试三重链式一元运算符：!!!x"""
        tokens = [
            self._create_token("NOT", "!", 1, 1),
            self._create_token("NOT", "!", 1, 2),
            self._create_token("NOT", "!", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 4
            }

            result = _parse_unary_expr(parser_state)

            # 验证三层嵌套 UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "NOT")
            self.assertEqual(result["column"], 1)

            level1 = result["children"][0]
            self.assertEqual(level1["type"], "UNARY_OP")
            self.assertEqual(level1["column"], 2)

            level2 = level1["children"][0]
            self.assertEqual(level2["type"], "UNARY_OP")
            self.assertEqual(level2["column"], 3)

            self.assertEqual(level2["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()
