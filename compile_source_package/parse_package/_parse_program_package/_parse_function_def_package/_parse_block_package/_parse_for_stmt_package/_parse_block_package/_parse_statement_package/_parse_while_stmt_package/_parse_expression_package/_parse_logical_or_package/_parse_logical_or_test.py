# -*- coding: utf-8 -*-
"""
单元测试：_parse_logical_or 函数
测试逻辑或表达式（|| 运算符）的解析功能
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._parse_logical_or_src import _parse_logical_or


class TestParseLogicalOr(unittest.TestCase):
    """测试 _parse_logical_or 函数的各种场景"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点字典"""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
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

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    @patch('._parse_logical_or_src._expect')
    def test_single_logical_or(self, mock_expect, mock_current_token, mock_parse_logical_and):
        """测试单个逻辑或表达式：a || b"""
        # 准备数据
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        right_operand = self._create_ast_node("IDENTIFIER", "b")
        op_token = self._create_token("OPERATOR", "||", line=1, column=3)
        eof_token = self._create_token("EOF", "", line=1, column=5)
        
        # 配置 mock
        mock_parse_logical_and.side_effect = [left_operand, right_operand]
        mock_current_token.side_effect = [op_token, eof_token]
        mock_expect.return_value = op_token
        
        parser_state = self._create_parser_state([op_token])
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        
        # 验证调用
        self.assertEqual(mock_parse_logical_and.call_count, 2)
        mock_expect.assert_called_once()

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    @patch('._parse_logical_or_src._expect')
    def test_multiple_logical_or_left_associative(self, mock_expect, mock_current_token, mock_parse_logical_and):
        """测试多个逻辑或表达式（左结合）：a || b || c"""
        # 准备数据
        operand_a = self._create_ast_node("IDENTIFIER", "a")
        operand_b = self._create_ast_node("IDENTIFIER", "b")
        operand_c = self._create_ast_node("IDENTIFIER", "c")
        op_token1 = self._create_token("OPERATOR", "||", line=1, column=3)
        op_token2 = self._create_token("OPERATOR", "||", line=1, column=7)
        eof_token = self._create_token("EOF", "", line=1, column=9)
        
        # 配置 mock
        mock_parse_logical_and.side_effect = [operand_a, operand_b, operand_c]
        mock_current_token.side_effect = [op_token1, op_token2, eof_token]
        mock_expect.side_effect = [op_token1, op_token2]
        
        parser_state = self._create_parser_state([op_token1, op_token2])
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证结果：应该是 (a || b) || c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        
        # 右操作数应该是 c
        self.assertEqual(result["children"][1], operand_c)
        
        # 左操作数应该是 (a || b)
        left_sub = result["children"][0]
        self.assertEqual(left_sub["type"], "BINARY_OP")
        self.assertEqual(left_sub["value"], "||")
        self.assertEqual(left_sub["children"][0], operand_a)
        self.assertEqual(left_sub["children"][1], operand_b)
        
        # 验证调用次数
        self.assertEqual(mock_parse_logical_and.call_count, 3)
        self.assertEqual(mock_expect.call_count, 2)

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    def test_no_logical_or(self, mock_current_token, mock_parse_logical_and):
        """测试没有逻辑或运算符的情况：直接返回 _parse_logical_and 的结果"""
        # 准备数据
        operand = self._create_ast_node("IDENTIFIER", "x")
        non_or_token = self._create_token("OPERATOR", "&&", line=1, column=2)
        
        # 配置 mock
        mock_parse_logical_and.return_value = operand
        mock_current_token.return_value = non_or_token
        
        parser_state = self._create_parser_state([non_or_token])
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证结果
        self.assertEqual(result, operand)
        
        # 验证只调用了一次 _parse_logical_and
        mock_parse_logical_and.assert_called_once()

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    def test_eof_token(self, mock_current_token, mock_parse_logical_and):
        """测试 EOF token 的情况"""
        # 准备数据
        operand = self._create_ast_node("IDENTIFIER", "x")
        eof_token = self._create_token("EOF", "", line=1, column=2)
        
        # 配置 mock
        mock_parse_logical_and.return_value = operand
        mock_current_token.return_value = eof_token
        
        parser_state = self._create_parser_state([])
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证结果
        self.assertEqual(result, operand)
        mock_parse_logical_and.assert_called_once()

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    @patch('._parse_logical_or_src._expect')
    def test_preserves_position_updates(self, mock_expect, mock_current_token, mock_parse_logical_and):
        """测试 parser_state 的 pos 位置被正确更新"""
        # 准备数据
        left_operand = self._create_ast_node("IDENTIFIER", "a")
        right_operand = self._create_ast_node("IDENTIFIER", "b")
        op_token = self._create_token("OPERATOR", "||", line=1, column=3)
        eof_token = self._create_token("EOF", "", line=1, column=5)
        
        # 配置 mock
        mock_parse_logical_and.side_effect = [left_operand, right_operand]
        mock_current_token.side_effect = [op_token, eof_token]
        mock_expect.return_value = op_token
        
        parser_state = self._create_parser_state([op_token], pos=0)
        initial_pos = parser_state["pos"]
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证 pos 被更新了（_expect 会消耗 token）
        self.assertNotEqual(parser_state["pos"], initial_pos)

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    @patch('._parse_logical_or_src._expect')
    def test_complex_expression_with_nested_and(self, mock_expect, mock_current_token, mock_parse_logical_and):
        """测试复杂表达式：(a && b) || (c && d)"""
        # 准备数据
        and_expr1 = self._create_ast_node("BINARY_OP", "&&", children=[
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ])
        and_expr2 = self._create_ast_node("BINARY_OP", "&&", children=[
            self._create_ast_node("IDENTIFIER", "c"),
            self._create_ast_node("IDENTIFIER", "d")
        ])
        op_token = self._create_token("OPERATOR", "||", line=1, column=6)
        eof_token = self._create_token("EOF", "", line=1, column=10)
        
        # 配置 mock
        mock_parse_logical_and.side_effect = [and_expr1, and_expr2]
        mock_current_token.side_effect = [op_token, eof_token]
        mock_expect.return_value = op_token
        
        parser_state = self._create_parser_state([op_token])
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["children"][0], and_expr1)
        self.assertEqual(result["children"][1], and_expr2)

    @patch('._parse_logical_or_src._parse_logical_and')
    @patch('._parse_logical_or_src._current_token')
    @patch('._parse_logical_or_src._expect')
    def test_operator_token_metadata_preserved(self, mock_expect, mock_current_token, mock_parse_logical_and):
        """测试运算符 token 的元数据（line, column）被正确保留"""
        # 准备数据
        left_operand = self._create_ast_node("IDENTIFIER", "x")
        right_operand = self._create_ast_node("IDENTIFIER", "y")
        op_token = self._create_token("OPERATOR", "||", line=5, column=10)
        eof_token = self._create_token("EOF", "", line=5, column=12)
        
        # 配置 mock
        mock_parse_logical_and.side_effect = [left_operand, right_operand]
        mock_current_token.side_effect = [op_token, eof_token]
        mock_expect.return_value = op_token
        
        parser_state = self._create_parser_state([op_token])
        
        # 执行测试
        result = _parse_logical_or(parser_state)
        
        # 验证元数据
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
