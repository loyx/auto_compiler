# -*- coding: utf-8 -*-
"""单元测试：_parse_primary_expr 函数"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_primary_expr_src import _parse_primary_expr

ParserState = Dict[str, Any]
AST = Dict[str, Any]


class TestParsePrimaryExpr(unittest.TestCase):
    """_parse_primary_expr 函数的单元测试类"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.cc") -> ParserState:
        """辅助函数：创建解析器状态"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_parse_number_literal(self):
        """测试解析 NUMBER token"""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "NUM_LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_string_literal(self):
        """测试解析 STRING token"""
        tokens = [
            {"type": "STRING", "value": "hello world", "line": 2, "column": 10}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "STR_LITERAL")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_identifier(self):
        """测试解析 IDENTIFIER token"""
        tokens = [
            {"type": "IDENTIFIER", "value": "myVar", "line": 3, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_true_literal(self):
        """测试解析 TRUE token"""
        tokens = [
            {"type": "TRUE", "value": "true", "line": 4, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "BOOL_LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 4)
        self.assertEqual(result["column"], 7)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_false_literal(self):
        """测试解析 FALSE token"""
        tokens = [
            {"type": "FALSE", "value": "false", "line": 5, "column": 8}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "BOOL_LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 8)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_none_literal(self):
        """测试解析 NONE token"""
        tokens = [
            {"type": "NONE", "value": "none", "line": 6, "column": 9}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "NONE_LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 6)
        self.assertEqual(result["column"], 9)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_parenthesized_expression(self):
        """测试解析括号表达式 (expression)"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 7, "column": 1},
            {"type": "NUMBER", "value": "123", "line": 7, "column": 2},
            {"type": "RPAREN", "value": ")", "line": 7, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression 返回一个 AST 节点
        mock_inner_expr = {"type": "NUM_LITERAL", "value": "123", "line": 7, "column": 2}
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_inner_expr
            
            result = _parse_primary_expr(parser_state)
            
            # 验证 _parse_expression 被调用
            mock_parse_expr.assert_called_once()
            
            # 验证返回的是内部表达式的结果
            self.assertEqual(result["type"], "NUM_LITERAL")
            self.assertEqual(result["value"], "123")
            
            # 验证 pos 已更新（消耗了 LPAREN、内部表达式、RPAREN）
            self.assertEqual(parser_state["pos"], 2)
            self.assertNotIn("error", parser_state)

    def test_parse_parenthesized_expression_with_nested_call(self):
        """测试括号表达式中 _parse_expression 的正确调用和 pos 更新"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 4}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        def mock_parse_expression_impl(state: ParserState) -> AST:
            # 模拟解析表达式后更新 pos
            state["pos"] = 1
            return {"type": "NUM_LITERAL", "value": "42", "line": 1, "column": 2}
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression_impl) as mock_parse_expr:
            result = _parse_primary_expr(parser_state)
            
            mock_parse_expr.assert_called_once()
            self.assertEqual(result["type"], "NUM_LITERAL")
            self.assertEqual(result["value"], "42")
            # LPAREN (pos=0->1) + inner expr (pos=1->1 via mock) + RPAREN (pos=1->2)
            self.assertEqual(parser_state["pos"], 2)

    def test_empty_tokens_error(self):
        """测试空 tokens 列表时的错误处理"""
        parser_state = self._create_parser_state([], pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of input while parsing primary expression")

    def test_pos_beyond_tokens_error(self):
        """测试 pos 超出 tokens 范围时的错误处理"""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 5)
        self.assertIn("Unexpected end of input", parser_state["error"])

    def test_missing_closing_paren_error(self):
        """测试缺少右括号时的错误处理"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        def mock_parse_expression_impl(state: ParserState) -> AST:
            state["pos"] = 1
            return {"type": "NUM_LITERAL", "value": "42", "line": 1, "column": 2}
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression_impl):
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIsNone(result["value"])
            self.assertIn("Unexpected end of input", parser_state["error"])

    def test_wrong_token_after_paren_error(self):
        """测试括号后跟错误 token 时的错误处理"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        def mock_parse_expression_impl(state: ParserState) -> AST:
            state["pos"] = 1
            return {"type": "NUM_LITERAL", "value": "42", "line": 1, "column": 2}
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression_impl):
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIsNone(result["value"])
            self.assertIn("Expected ')'", parser_state["error"])
            self.assertIn("IDENTIFIER", parser_state["error"])

    def test_unrecognized_token_error(self):
        """测试无法识别的 token 类型时的错误处理"""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Unexpected token 'PLUS' while parsing primary expression")

    def test_parse_expression_error_propagation(self):
        """测试内部 _parse_expression 错误时的传播"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        def mock_parse_expression_impl(state: ParserState) -> AST:
            state["pos"] = 1
            state["error"] = "Expression parse error"
            return {"type": "ERROR", "value": None, "line": 1, "column": 2}
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression_impl):
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["error"], "Expression parse error")

    def test_token_without_line_column(self):
        """测试 token 缺少 line/column 字段时的默认值处理"""
        tokens = [
            {"type": "NUMBER", "value": "99"}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "NUM_LITERAL")
        self.assertEqual(result["value"], "99")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_multiple_primary_expressions_sequential(self):
        """测试连续解析多个主表达式"""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "STRING", "value": "test", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 9}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 解析第一个
        result1 = _parse_primary_expr(parser_state)
        self.assertEqual(result1["type"], "NUM_LITERAL")
        self.assertEqual(result1["value"], "1")
        self.assertEqual(parser_state["pos"], 1)
        
        # 解析第二个
        result2 = _parse_primary_expr(parser_state)
        self.assertEqual(result2["type"], "STR_LITERAL")
        self.assertEqual(result2["value"], "test")
        self.assertEqual(parser_state["pos"], 2)
        
        # 解析第三个
        result3 = _parse_primary_expr(parser_state)
        self.assertEqual(result3["type"], "IDENTIFIER")
        self.assertEqual(result3["value"], "x")
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
