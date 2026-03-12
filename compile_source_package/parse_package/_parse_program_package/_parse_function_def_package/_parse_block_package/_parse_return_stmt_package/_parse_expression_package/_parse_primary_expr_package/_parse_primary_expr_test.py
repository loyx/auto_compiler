# -*- coding: utf-8 -*-
"""单元测试：_parse_primary_expr 函数"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# 在导入 _parse_primary_expr_src 之前，先 patch _parse_or_expr
# 使用 patch 的 start() 方法在导入前应用 mock

# 创建 mock 函数
mock_parse_or_expr_func = MagicMock(return_value={"type": "MOCK_OR_EXPR", "value": "mocked", "line": 0, "column": 0})

# 我们需要 patch 的是 _parse_primary_expr_src 模块中的 _parse_or_expr 引用
# 但由于导入时 _parse_or_expr_src 本身有依赖问题，我们需要先 mock 整个 _parse_or_expr_src 模块

# 创建 mock 模块
mock_or_expr_src_module = MagicMock()
mock_or_expr_src_module._parse_or_expr = mock_parse_or_expr_func

# 注册到 sys.modules，key 是完整的模块路径
# _parse_primary_expr_src 使用相对导入: from ._parse_or_expr_package._parse_or_expr_src import _parse_or_expr
# 这会被解析为 _parse_primary_expr_package._parse_or_expr_package._parse_or_expr_src

# 获取当前测试模块的包名
TEST_PACKAGE = '_parse_primary_expr_package'
OR_EXPR_PACKAGE = f'{TEST_PACKAGE}._parse_or_expr_package'
OR_EXPR_SRC = f'{OR_EXPR_PACKAGE}._parse_or_expr_src'

# 注册 mock 模块
sys.modules[OR_EXPR_SRC] = mock_or_expr_src_module
sys.modules[OR_EXPR_PACKAGE] = MagicMock(_parse_or_expr_src=mock_or_expr_src_module)

# 现在导入被测试模块
from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """测试 _parse_primary_expr 函数的各种场景"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path 测试 ====================

    def test_parse_identifier(self):
        """测试解析标识符"""
        token = self._create_token("IDENTIFIER", "myVar", 1, 5)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)  # pos 应该前进

    def test_parse_integer_literal(self):
        """测试解析整数字面量"""
        token = self._create_token("INTEGER", "42", 2, 10)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_float_literal(self):
        """测试解析浮点数字面量"""
        token = self._create_token("FLOAT", "3.14", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """测试解析字符串字面量"""
        token = self._create_token("STRING", '"hello world"', 3, 7)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello world")  # 去除引号
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_char_literal(self):
        """测试解析字符字面量"""
        token = self._create_token("CHAR", "'a'", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "a")  # 去除引号
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true_literal(self):
        """测试解析 true 字面量"""
        token = self._create_token("TRUE", "true", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false_literal(self):
        """测试解析 false 字面量"""
        token = self._create_token("FALSE", "false", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """测试解析 null 字面量"""
        token = self._create_token("NULL", "null", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    # ==================== 括号表达式测试 ====================

    @patch("_parse_primary_expr_package._parse_primary_expr_src._parse_or_expr")
    def test_parse_parenthesized_expression(self, mock_parse_or_expr: MagicMock):
        """测试解析括号表达式"""
        lparen = self._create_token("LPAREN", "(", 1, 1)
        rparen = self._create_token("RPAREN", ")", 1, 10)
        tokens = [lparen, rparen]
        parser_state = self._create_parser_state(tokens)

        # mock _parse_or_expr 的返回值
        mock_ast = {
            "type": "BINARY_OP",
            "children": [],
            "value": "+",
            "line": 1,
            "column": 2
        }
        mock_parse_or_expr.return_value = mock_ast

        result = _parse_primary_expr(parser_state)

        # 验证返回的是 _parse_or_expr 的结果
        self.assertEqual(result, mock_ast)
        self.assertEqual(parser_state["pos"], 2)  # 消费了左右括号
        mock_parse_or_expr.assert_called_once()

    @patch("_parse_primary_expr_package._parse_primary_expr_src._parse_or_expr")
    def test_parse_parenthesized_expression_nested(self, mock_parse_or_expr: MagicMock):
        """测试嵌套括号表达式（_parse_or_expr 可能返回复杂 AST）"""
        lparen = self._create_token("LPAREN", "(", 2, 5)
        rparen = self._create_token("RPAREN", ")", 2, 20)
        tokens = [lparen, rparen]
        parser_state = self._create_parser_state(tokens, filename="nested.src")

        mock_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 2,
            "column": 6
        }
        mock_parse_or_expr.return_value = mock_ast

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        mock_parse_or_expr.assert_called_once()

    # ==================== 边界值测试 ====================

    def test_empty_tokens_list(self):
        """测试空 token 列表"""
        parser_state = self._create_parser_state([], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("意外的文件结束", str(context.exception))

    def test_pos_beyond_tokens_length(self):
        """测试 pos 超出 token 列表长度"""
        token = self._create_token("IDENTIFIER", "x", 1, 1)
        parser_state = self._create_parser_state([token], pos=5)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("意外的文件结束", str(context.exception))

    def test_pos_at_tokens_length(self):
        """测试 pos 等于 token 列表长度"""
        token = self._create_token("IDENTIFIER", "x", 1, 1)
        parser_state = self._create_parser_state([token], pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        self.assertIn("意外的文件结束", str(context.exception))

    # ==================== 错误处理测试 ====================

    def test_unsupported_token_type(self):
        """测试不支持的 token 类型"""
        token = self._create_token("PLUS", "+", 5, 15)
        parser_state = self._create_parser_state([token], filename="error.src")

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        error_msg = str(context.exception)
        self.assertIn("error.src:5:15", error_msg)
        self.assertIn("期望基本表达式", error_msg)
        self.assertIn("'+'", error_msg)
        self.assertIn("(PLUS)", error_msg)

    @patch("_parse_primary_expr_package._parse_primary_expr_src._parse_or_expr")
    def test_missing_rparen_eof(self, mock_parse_or_expr: MagicMock):
        """测试缺少右括号（文件结束）"""
        lparen = self._create_token("LPAREN", "(", 3, 8)
        parser_state = self._create_parser_state([lparen], filename="missing.src")

        mock_parse_or_expr.return_value = {"type": "IDENTIFIER", "value": "x"}

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        error_msg = str(context.exception)
        self.assertIn("missing.src:3:8", error_msg)
        self.assertIn("期望 ')'", error_msg)
        self.assertIn("未找到", error_msg)

    @patch("_parse_primary_expr_package._parse_primary_expr_src._parse_or_expr")
    def test_wrong_rparen(self, mock_parse_or_expr: MagicMock):
        """测试错误的右括号（得到其他 token）"""
        lparen = self._create_token("LPAREN", "(", 4, 12)
        wrong_token = self._create_token("COMMA", ",", 4, 20)
        parser_state = self._create_parser_state([lparen, wrong_token], filename="wrong.src")

        mock_parse_or_expr.return_value = {"type": "IDENTIFIER", "value": "x"}

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        error_msg = str(context.exception)
        self.assertIn("wrong.src:4:20", error_msg)
        self.assertIn("期望 ')'", error_msg)
        self.assertIn("','", error_msg)
        self.assertIn("(COMMA)", error_msg)

    # ==================== 多 token 场景测试 ====================

    def test_identifier_with_following_tokens(self):
        """测试标识符后有其他 token（只消费当前 token）"""
        id_token = self._create_token("IDENTIFIER", "var1", 1, 1)
        plus_token = self._create_token("PLUS", "+", 1, 6)
        tokens = [id_token, plus_token]
        parser_state = self._create_parser_state(tokens)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["value"], "var1")
        self.assertEqual(parser_state["pos"], 1)  # 只消费了标识符

    def test_literal_with_following_tokens(self):
        """测试字面量后有其他 token"""
        int_token = self._create_token("INTEGER", "100", 2, 3)
        semicolon_token = self._create_token("SEMICOLON", ";", 2, 7)
        tokens = [int_token, semicolon_token]
        parser_state = self._create_parser_state(tokens)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["value"], 100)
        self.assertEqual(parser_state["pos"], 1)  # 只消费了整数

    # ==================== 特殊值测试 ====================

    def test_negative_integer(self):
        """测试负整数（作为字面量）"""
        token = self._create_token("INTEGER", "-42", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], -42)

    def test_zero_integer(self):
        """测试零"""
        token = self._create_token("INTEGER", "0", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 0)

    def test_empty_string(self):
        """测试空字符串"""
        token = self._create_token("STRING", '""', 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "")

    def test_scientific_notation_float(self):
        """测试科学计数法浮点数"""
        token = self._create_token("FLOAT", "1.5e10", 1, 1)
        parser_state = self._create_parser_state([token])

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 1.5e10)

    # ==================== 文件名缺失测试 ====================

    def test_error_without_filename(self):
        """测试没有 filename 时的错误信息"""
        token = self._create_token("PLUS", "+", 1, 1)
        parser_state = {
            "tokens": [token],
            "pos": 0
            # 没有 filename
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)

        error_msg = str(context.exception)
        self.assertIn("<unknown>", error_msg)


if __name__ == "__main__":
    unittest.main()
