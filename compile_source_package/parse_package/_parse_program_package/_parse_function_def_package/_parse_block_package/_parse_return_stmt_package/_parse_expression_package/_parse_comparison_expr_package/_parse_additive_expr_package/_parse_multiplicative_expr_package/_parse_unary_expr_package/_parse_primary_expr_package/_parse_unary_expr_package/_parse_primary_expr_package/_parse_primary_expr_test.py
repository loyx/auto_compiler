# -*- coding: utf-8 -*-
"""单元测试文件：_parse_primary_expr"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测试模块
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
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    # ==================== Happy Path 测试 ====================

    def test_parse_identifier(self):
        """测试解析标识符"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_number_literal(self):
        """测试解析数字字面量"""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_string_literal(self):
        """测试解析字符串字面量"""
        tokens = [self._create_token("STRING", '"hello"')]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_boolean_literal(self):
        """测试解析布尔字面量"""
        tokens = [self._create_token("BOOLEAN", "true")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "true")
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_null_literal(self):
        """测试解析 null 字面量"""
        tokens = [self._create_token("NULL", "null")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "null")
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    @patch('._parse_primary_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_parse_parenthesized_expression(self, mock_unary_expr):
        """测试解析括号表达式"""
        # 设置 mock 返回值
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
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        # 验证返回的是内部表达式的结果
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        # 验证 pos 已经消费了 LPAREN 和 RPAREN
        self.assertEqual(parser_state["pos"], 3)
        self.assertNotIn("error", parser_state)
        # 验证 _parse_unary_expr 被调用
        mock_unary_expr.assert_called_once()

    # ==================== 边界值测试 ====================

    def test_empty_tokens(self):
        """测试空 token 列表"""
        parser_state = self._create_parser_state([])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_pos_at_end(self):
        """测试 pos 已经在末尾"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_pos_beyond_end(self):
        """测试 pos 超出末尾"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_token_missing_type(self):
        """测试 token 缺少 type 字段"""
        tokens = [{"value": "x", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token", parser_state["error"])

    def test_token_missing_value(self):
        """测试 token 缺少 value 字段"""
        tokens = [{"type": "IDENTIFIER", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        # 应该能正常处理，value 为默认值 ""
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["pos"], 1)

    # ==================== 错误路径测试 ====================

    def test_unexpected_token_type(self):
        """测试意外的 token 类型"""
        tokens = [self._create_token("OPERATOR", "+")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertIn("Unexpected token '+'", parser_state["error"])

    def test_paren_missing_rparen_eof(self):
        """测试括号表达式缺少右括号（遇到文件末尾）"""
        tokens = [self._create_token("LPAREN", "(")]
        parser_state = self._create_parser_state(tokens)
        
        with patch('._parse_primary_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Expected ')' but found end of input")

    def test_paren_missing_rparen_other_token(self):
        """测试括号表达式缺少右括号（遇到其他 token）"""
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("OPERATOR", "+")
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch('._parse_primary_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr') as mock_unary:
            mock_unary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Expected ')' but found '+'", parser_state["error"])

    @patch('._parse_primary_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_paren_inner_error(self, mock_unary_expr):
        """测试括号内表达式解析出错"""
        # 设置 mock 返回 ERROR 并设置 error
        mock_unary_expr.side_effect = lambda state: state.update({"error": "Inner error"}) or {
            "type": "ERROR",
            "children": [],
            "value": None,
            "line": -1,
            "column": -1
        }
        
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("OPERATOR", "+")
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Inner error", parser_state.get("error", ""))

    # ==================== 多分支逻辑测试 ====================

    def test_multiple_identifiers_sequence(self):
        """测试多个标识符序列（只解析第一个）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("IDENTIFIER", "y", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)  # 只消费了一个 token

    def test_literal_then_identifier(self):
        """测试字面量后跟标识符"""
        tokens = [
            self._create_token("NUMBER", "123", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "123")
        self.assertEqual(parser_state["pos"], 1)

    # ==================== 状态变化测试 ====================

    def test_pos_updated_correctly(self):
        """测试 pos 正确更新"""
        tokens = [self._create_token("IDENTIFIER", "var_name", 2, 5)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

    def test_error_state_preserved(self):
        """测试错误状态设置"""
        tokens = [self._create_token("UNKNOWN", "???")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertIn("error", parser_state)
        self.assertTrue(parser_state["error"].startswith("Unexpected token"))

    # ==================== 依赖异常测试 ====================

    @patch('._parse_primary_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_unary_expr_exception(self, mock_unary_expr):
        """测试 _parse_unary_expr 抛出异常"""
        mock_unary_expr.side_effect = Exception("Mocked exception")
        
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "x")
        ]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(Exception) as context:
            _parse_primary_expr(parser_state)
        
        self.assertEqual(str(context.exception), "Mocked exception")


if __name__ == "__main__":
    unittest.main()
