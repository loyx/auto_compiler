# -*- coding: utf-8 -*-
"""单元测试：_parse_primary_expr 函数"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """_parse_primary_expr 函数测试用例"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    # ==================== Happy Path Tests ====================

    def test_parse_identifier(self):
        """测试：解析标识符"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_with_position(self):
        """测试：解析带位置信息的标识符"""
        tokens = [
            self._create_token("NUMBER", "1"),
            self._create_token("IDENTIFIER", "var", line=5, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "var")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_integer_literal(self):
        """测试：解析整数字面量"""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_float_literal(self):
        """测试：解析浮点数字面量"""
        tokens = [self._create_token("NUMBER", "3.14")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_negative_integer_literal(self):
        """测试：解析负整数字面量"""
        tokens = [self._create_token("NUMBER", "-10")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], -10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """测试：解析字符串字面量"""
        tokens = [self._create_token("STRING", '"hello"')]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal_single_quotes(self):
        """测试：解析单引号字符串字面量"""
        tokens = [self._create_token("STRING", "'world'")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "world")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true_literal(self):
        """测试：解析 TRUE 字面量"""
        tokens = [self._create_token("TRUE", "true")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false_literal(self):
        """测试：解析 FALSE 字面量"""
        tokens = [self._create_token("FALSE", "false")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """测试：解析 NULL 字面量"""
        tokens = [self._create_token("NULL", "null")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], None)
        self.assertEqual(parser_state["pos"], 1)

    @patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_parse_parenthesized_expression(self, mock_parse_expression):
        """测试：解析括号表达式"""
        mock_ast = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [],
            "line": 1,
            "column": 2
        }
        mock_parse_expression.return_value = mock_ast
        
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "1"),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result, mock_ast)
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_expression.assert_called_once()

    @patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_parse_nested_parenthesized_expression(self, mock_parse_expression):
        """测试：解析嵌套括号表达式"""
        inner_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 3
        }
        mock_parse_expression.return_value = inner_ast
        
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("RPAREN", ")"),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result, inner_ast)
        self.assertEqual(parser_state["pos"], 5)

    # ==================== Boundary Tests ====================

    def test_empty_tokens_list(self):
        """测试：空 token 列表"""
        parser_state = self._create_parser_state([])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("<test>", str(context.exception))

    def test_pos_beyond_tokens_length(self):
        """测试：pos 超出 token 列表长度"""
        tokens = [self._create_token("NUMBER", "1")]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_at_tokens_length(self):
        """测试：pos 等于 token 列表长度"""
        tokens = [self._create_token("NUMBER", "1")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_missing_filename_uses_default(self):
        """测试：缺失 filename 时使用默认值"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))

    # ==================== Error Cases ====================

    def test_unexpected_token_operator(self):
        """测试：意外 token - 运算符"""
        tokens = [self._create_token("PLUS", "+", line=2, column=5)]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("line 2", str(context.exception))
        self.assertIn("column 5", str(context.exception))

    def test_unexpected_token_keyword(self):
        """测试：意外 token - 关键字"""
        tokens = [self._create_token("IF", "if", line=3, column=1)]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected token 'if'", str(context.exception))

    def test_missing_closing_paren(self):
        """测试：缺少右括号"""
        tokens = [
            self._create_token("LPAREN", "(", line=1, column=1),
            self._create_token("NUMBER", "1")
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "LITERAL", "value": 1, "children": []}
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or {"type": "LITERAL", "value": 1, "children": []}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))

    def test_missing_closing_paren_at_end(self):
        """测试：缺少右括号 - 到达输入末尾"""
        tokens = [
            self._create_token("LPAREN", "(", line=1, column=1),
            self._create_token("NUMBER", "5")
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def update_pos_and_return(state):
                state["pos"] = 2
                return {"type": "LITERAL", "value": 5, "children": [], "line": 1, "column": 2}
            
            mock_parse_expr.side_effect = update_pos_and_return
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))

    def test_wrong_closing_token(self):
        """测试：错误的闭合 token"""
        tokens = [
            self._create_token("LPAREN", "(", line=1, column=1),
            self._create_token("NUMBER", "1"),
            self._create_token("LBRACKET", "[", line=1, column=3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def update_pos_and_return(state):
                state["pos"] = 2
                return {"type": "LITERAL", "value": 1, "children": [], "line": 1, "column": 2}
            
            mock_parse_expr.side_effect = update_pos_and_return
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))

    # ==================== Edge Cases ====================

    def test_string_literal_edge_empty_string(self):
        """测试：空字符串字面量"""
        tokens = [self._create_token("STRING", '""')]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "")

    def test_string_literal_edge_single_char(self):
        """测试：单字符字符串字面量"""
        tokens = [self._create_token("STRING", '"a"')]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "a")

    def test_number_literal_edge_zero(self):
        """测试：零字面量"""
        tokens = [self._create_token("NUMBER", "0")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 0)

    def test_number_literal_edge_large_float(self):
        """测试：大浮点数字面量"""
        tokens = [self._create_token("NUMBER", "123456.789012")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 123456.789012)

    def test_multiple_consecutive_primary_exprs(self):
        """测试：连续解析多个基本表达式"""
        tokens = [
            self._create_token("IDENTIFIER", "a"),
            self._create_token("NUMBER", "42"),
            self._create_token("STRING", '"test"')
        ]
        parser_state = self._create_parser_state(tokens)
        
        result1 = _parse_primary_expr(parser_state)
        self.assertEqual(result1["type"], "IDENTIFIER")
        self.assertEqual(result1["value"], "a")
        self.assertEqual(parser_state["pos"], 1)
        
        result2 = _parse_primary_expr(parser_state)
        self.assertEqual(result2["type"], "LITERAL")
        self.assertEqual(result2["value"], 42)
        self.assertEqual(parser_state["pos"], 2)
        
        result3 = _parse_primary_expr(parser_state)
        self.assertEqual(result3["type"], "LITERAL")
        self.assertEqual(result3["value"], "test")
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
