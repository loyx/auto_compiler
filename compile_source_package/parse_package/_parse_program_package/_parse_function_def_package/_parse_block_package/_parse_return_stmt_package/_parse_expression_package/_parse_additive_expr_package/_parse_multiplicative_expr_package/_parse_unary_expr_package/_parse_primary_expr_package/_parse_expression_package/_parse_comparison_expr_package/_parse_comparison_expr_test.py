# -*- coding: utf-8 -*-
"""单元测试：_parse_comparison_expr 函数"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """_parse_comparison_expr 函数的单元测试类"""

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

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_lt_comparison(self, mock_additive):
        """测试单个小于比较运算符：a < b"""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_additive.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["left"], left_operand)
        self.assertEqual(result["right"], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(mock_additive.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_eq_comparison(self, mock_additive):
        """测试等于比较运算符：a == b"""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        mock_additive.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("EQ", "==", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "==")
        self.assertEqual(result["left"], left_operand)
        self.assertEqual(result["right"], right_operand)
        self.assertEqual(parser_state["pos"], 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_ne_comparison(self, mock_additive):
        """测试不等于比较运算符：a != b"""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        mock_additive.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("NE", "!=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "!=")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_le_comparison(self, mock_additive):
        """测试小于等于比较运算符：a <= b"""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        mock_additive.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LE", "<=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<=")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_gt_comparison(self, mock_additive):
        """测试大于比较运算符：a > b"""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_additive.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("GT", ">", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_single_ge_comparison(self, mock_additive):
        """测试大于等于比较运算符：a >= b"""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        mock_additive.side_effect = [left_operand, right_operand]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("GE", ">=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">=")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_chained_comparisons(self, mock_additive):
        """测试链式比较：a < b < c"""
        operand1 = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand2 = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand3 = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        mock_additive.side_effect = [operand1, operand2, operand3]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("LT", "<", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        
        left_part = result["left"]
        self.assertEqual(left_part["type"], "BINARY_OP")
        self.assertEqual(left_part["operator"], "<")
        self.assertEqual(left_part["left"], operand1)
        self.assertEqual(left_part["right"], operand2)
        
        self.assertEqual(result["right"], operand3)
        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(mock_additive.call_count, 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_no_comparison_operator(self, mock_additive):
        """测试没有比较运算符的情况：只返回 additive expr 的结果"""
        operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_additive.return_value = operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(mock_additive.call_count, 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_empty_tokens(self, mock_additive):
        """测试空 token 列表"""
        operand = {"type": "LITERAL", "value": 42, "line": 1, "column": 1}
        mock_additive.return_value = operand
        
        parser_state = self._create_parser_state([], pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(mock_additive.call_count, 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_comparison_followed_by_non_comparison(self, mock_additive):
        """测试比较运算符后跟非比较运算符：a < b + c"""
        operand1 = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand2 = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_additive.side_effect = [operand1, operand2]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("PLUS", "+", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["left"], operand1)
        self.assertEqual(result["right"], operand2)
        self.assertEqual(parser_state["pos"], 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_mixed_comparison_operators(self, mock_additive):
        """测试混合比较运算符：a < b >= c"""
        operand1 = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand2 = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand3 = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10}
        mock_additive.side_effect = [operand1, operand2, operand3]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("GE", ">=", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">=")
        self.assertEqual(result["column"], 7)
        
        left_part = result["left"]
        self.assertEqual(left_part["type"], "BINARY_OP")
        self.assertEqual(left_part["operator"], "<")
        
        self.assertEqual(result["right"], operand3)
        self.assertEqual(parser_state["pos"], 4)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_position_at_end(self, mock_additive):
        """测试 pos 已在 tokens 末尾的情况"""
        operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_additive.return_value = operand
        
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LT", "<", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=2)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(mock_additive.call_count, 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr')
    def test_literal_comparison(self, mock_additive):
        """测试字面量比较：1 < 2"""
        left_literal = {"type": "LITERAL", "value": 1, "line": 1, "column": 1}
        right_literal = {"type": "LITERAL", "value": 2, "line": 1, "column": 5}
        mock_additive.side_effect = [left_literal, right_literal]
        
        tokens = [
            self._create_token("LITERAL", "1", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("LITERAL", "2", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["left"], left_literal)
        self.assertEqual(result["right"], right_literal)


if __name__ == "__main__":
    unittest.main()
