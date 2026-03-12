# -*- coding: utf-8 -*-
"""单元测试文件：_parse_primary_expr"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """_parse_primary_expr 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    # ========== Happy Path 测试 ==========

    def test_parse_identifier(self):
        """测试解析标识符"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_number_literal(self):
        """测试解析数字字面量"""
        tokens = [self._create_token("NUMBER", "42", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """测试解析字符串字面量"""
        tokens = [self._create_token("STRING", '"hello"', 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_boolean_literal(self):
        """测试解析布尔字面量"""
        tokens = [self._create_token("BOOLEAN", "true", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "true")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """测试解析 null 字面量"""
        tokens = [self._create_token("NULL", "null", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "null")
        self.assertEqual(parser_state["pos"], 1)

    # ========== 括号表达式测试 ==========

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_parse_parenthesized_expression(self, mock_unary_expr):
        """测试解析括号表达式"""
        mock_unary_expr.return_value = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "y",
            "line": 1,
            "column": 2
        }

        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "y", 1, 2),
            self._create_token("RPAREN", ")", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"], "y")
        self.assertEqual(parser_state["pos"], 3)
        mock_unary_expr.assert_called_once()

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_parse_parenthesized_expression_with_error(self, mock_unary_expr):
        """测试括号内表达式解析出错的情况"""
        mock_unary_expr.return_value = {
            "type": "ERROR",
            "children": [],
            "value": "Unexpected token",
            "line": 1,
            "column": 2
        }

        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("PLUS", "+", 1, 2),
            self._create_token("RPAREN", ")", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, 0)
        parser_state["error"] = "Unexpected token"

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_parenthesized_missing_rparen(self):
        """测试括号表达式缺少右括号"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary_expr:
            mock_unary_expr.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Missing closing parenthesis", result["value"])
        self.assertIn("error", parser_state)

    def test_parse_parenthesized_wrong_closing_token(self):
        """测试括号表达式使用错误的闭合符号"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2),
            self._create_token("RBRACKET", "]", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary_expr:
            mock_unary_expr.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }

            result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Expected RPAREN, got RBRACKET", result["value"])
        self.assertIn("error", parser_state)

    # ========== 边界值测试 ==========

    def test_empty_input(self):
        """测试空输入（tokens 为空列表）"""
        tokens = []
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", result["value"])
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end(self):
        """测试 pos 已经在 tokens 末尾"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens, 1)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_pos_beyond_end(self):
        """测试 pos 超出 tokens 范围"""
        tokens = [self._create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens, 5)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", result["value"])

    # ========== 非法输入测试 ==========

    def test_unexpected_token_type(self):
        """测试遇到意外的 token 类型"""
        tokens = [self._create_token("PLUS", "+", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token: PLUS", result["value"])
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["pos"], 0)

    def test_operator_token(self):
        """测试运算符 token"""
        tokens = [self._create_token("MINUS", "-", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token: MINUS", result["value"])

    def test_keyword_token(self):
        """测试关键字 token"""
        tokens = [self._create_token("IF", "if", 1, 1)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token: IF", result["value"])

    # ========== 多位置测试 ==========

    def test_parse_identifier_at_different_position(self):
        """测试在不同位置解析标识符"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("IDENTIFIER", "var", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 1)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "var")
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_literal_at_different_position(self):
        """测试在不同位置解析字面量"""
        tokens = [
            self._create_token("MINUS", "-", 1, 1),
            self._create_token("NUMBER", "123", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, 1)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "123")
        self.assertEqual(parser_state["pos"], 2)

    # ========== 错误节点位置信息测试 ==========

    def test_error_node_has_correct_position(self):
        """测试错误节点包含正确的位置信息"""
        tokens = [self._create_token("COMMA", ",", 5, 10)]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    # ========== 嵌套括号表达式测试 ==========

    @patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr")
    def test_nested_parentheses(self, mock_unary_expr):
        """测试嵌套括号表达式（通过 mock 模拟）"""
        mock_unary_expr.return_value = {
            "type": "PAREN_EXPR",
            "children": [],
            "value": None,
            "line": 1,
            "column": 2
        }

        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("LPAREN", "(", 1, 2),
            self._create_token("IDENTIFIER", "x", 1, 3),
            self._create_token("RPAREN", ")", 1, 4),
            self._create_token("RPAREN", ")", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(result["children"][0]["type"], "PAREN_EXPR")
        self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()
