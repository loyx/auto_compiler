# -*- coding: utf-8 -*-
"""
单元测试：_parse_and_expr 函数
测试 'and' 表达式链解析逻辑
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """测试 _parse_and_expr 函数"""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast(self, ast_type: str, children: list = None, value: Any = None, 
                    line: int = 1, column: int = 1, operator: str = None) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点字典"""
        ast = {
            "type": ast_type,
            "children": children if children is not None else [],
            "value": value,
            "line": line,
            "column": column
        }
        if operator is not None:
            ast["operator"] = operator
        return ast

    def _create_parser_state(self, tokens: list = None, pos: int = 0, 
                             filename: str = "test.py", error: str = "") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename,
            "error": error
        }

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_single_comparison_no_and(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：单个 comparison 表达式，没有 AND"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        initial_state = self._create_parser_state(tokens=[self._create_token("EOF")])
        
        # 设置 mock 返回值
        mock_parse_comparison.return_value = (left_ast, initial_state)
        mock_peek.return_value = self._create_token("EOF")
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果
        self.assertEqual(result_ast, left_ast)
        mock_parse_comparison.assert_called_once_with(initial_state)
        mock_peek.assert_called_once()
        mock_consume.assert_not_called()

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_one_and_expression(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：一个 AND 表达式 (a and b)"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        right_ast = self._create_ast("COMPARISON", value="b")
        and_token = self._create_token("AND", line=1, column=5)
        eof_token = self._create_token("EOF")
        initial_state = self._create_parser_state(tokens=[and_token, eof_token])
        state_after_consume = self._create_parser_state(tokens=[and_token, eof_token], pos=1)
        
        # 设置 mock 返回值：第一次 parse_comparison 返回 left_ast
        # 第二次 parse_comparison 返回 right_ast
        mock_parse_comparison.side_effect = [
            (left_ast, initial_state),
            (right_ast, state_after_consume)
        ]
        # peek 先返回 AND，然后返回 EOF
        mock_peek.side_effect = [and_token, eof_token]
        mock_consume.return_value = state_after_consume
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["operator"], "and")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 5)
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["children"][0], left_ast)
        self.assertEqual(result_ast["children"][1], right_ast)
        
        # 验证调用
        self.assertEqual(mock_parse_comparison.call_count, 2)
        self.assertEqual(mock_peek.call_count, 2)
        mock_consume.assert_called_once()

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_multiple_and_expressions(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：多个 AND 表达式链 (a and b and c)"""
        # 准备数据
        ast_a = self._create_ast("COMPARISON", value="a")
        ast_b = self._create_ast("COMPARISON", value="b")
        ast_c = self._create_ast("COMPARISON", value="c")
        and_token_1 = self._create_token("AND", line=1, column=5)
        and_token_2 = self._create_token("AND", line=1, column=10)
        eof_token = self._create_token("EOF")
        initial_state = self._create_parser_state(tokens=[and_token_1, and_token_2, eof_token])
        state_1 = self._create_parser_state(tokens=[and_token_1, and_token_2, eof_token], pos=1)
        state_2 = self._create_parser_state(tokens=[and_token_1, and_token_2, eof_token], pos=2)
        
        # 设置 mock 返回值
        mock_parse_comparison.side_effect = [
            (ast_a, initial_state),
            (ast_b, state_1),
            (ast_c, state_2)
        ]
        mock_peek.side_effect = [and_token_1, and_token_2, eof_token]
        mock_consume.side_effect = [state_1, state_2]
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果：应该是左结合的 ((a and b) and c)
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["operator"], "and")
        self.assertEqual(result_ast["line"], 1)  # 第二个 AND 的位置
        self.assertEqual(result_ast["column"], 10)
        self.assertEqual(len(result_ast["children"]), 2)
        # 右子节点应该是 c
        self.assertEqual(result_ast["children"][1], ast_c)
        # 左子节点应该是 (a and b)
        left_child = result_ast["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["operator"], "and")
        self.assertEqual(left_child["children"][0], ast_a)
        self.assertEqual(left_child["children"][1], ast_b)
        
        # 验证调用次数
        self.assertEqual(mock_parse_comparison.call_count, 3)
        self.assertEqual(mock_peek.call_count, 3)
        self.assertEqual(mock_consume.call_count, 2)

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_none_token(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：peek 返回 None（空 token 列表）"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        initial_state = self._create_parser_state(tokens=[])
        
        # 设置 mock 返回值
        mock_parse_comparison.return_value = (left_ast, initial_state)
        mock_peek.return_value = None
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果
        self.assertEqual(result_ast, left_ast)
        mock_parse_comparison.assert_called_once()
        mock_peek.assert_called_once()
        mock_consume.assert_not_called()

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_token_without_type_field(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：token 没有 type 字段"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        invalid_token = {"value": "something", "line": 1, "column": 1}
        initial_state = self._create_parser_state(tokens=[invalid_token])
        
        # 设置 mock 返回值
        mock_parse_comparison.return_value = (left_ast, initial_state)
        mock_peek.return_value = invalid_token
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果：应该当作非 AND token 处理
        self.assertEqual(result_ast, left_ast)
        mock_parse_comparison.assert_called_once()
        mock_peek.assert_called_once()
        mock_consume.assert_not_called()

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_and_token_different_case(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：AND token 大小写不匹配（如 'And' 或 'and'）"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        lowercase_and = self._create_token("and")  # 小写
        initial_state = self._create_parser_state(tokens=[lowercase_and])
        
        # 设置 mock 返回值
        mock_parse_comparison.return_value = (left_ast, initial_state)
        mock_peek.return_value = lowercase_and
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果：不匹配，应该返回单个 comparison
        self.assertEqual(result_ast, left_ast)
        mock_consume.assert_not_called()

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_token_missing_line_column(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：AND token 缺少 line/column 字段（使用默认值 0）"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        right_ast = self._create_ast("COMPARISON", value="b")
        and_token = {"type": "AND", "value": "and"}  # 没有 line/column
        eof_token = self._create_token("EOF")
        initial_state = self._create_parser_state(tokens=[and_token, eof_token])
        state_after = self._create_parser_state(tokens=[and_token, eof_token], pos=1)
        
        # 设置 mock 返回值
        mock_parse_comparison.side_effect = [
            (left_ast, initial_state),
            (right_ast, state_after)
        ]
        mock_peek.side_effect = [and_token, eof_token]
        mock_consume.return_value = state_after
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果：line/column 应该默认为 0
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["line"], 0)
        self.assertEqual(result_ast["column"], 0)

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_parser_state_with_error(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：parser_state 带有错误信息"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        initial_state = self._create_parser_state(
            tokens=[self._create_token("EOF")],
            error="previous error"
        )
        
        # 设置 mock 返回值
        mock_parse_comparison.return_value = (left_ast, initial_state)
        mock_peek.return_value = self._create_token("EOF")
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证结果：错误信息应该保留
        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["error"], "previous error")

    @patch('_parse_and_expr_package._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('_parse_and_expr_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_and_expr_package._consume_token_package._consume_token_src._consume_token')
    def test_ast_node_structure(self, mock_consume, mock_peek, mock_parse_comparison):
        """测试：生成的 BINARY_OP AST 节点结构完整性"""
        # 准备数据
        left_ast = self._create_ast("COMPARISON", value="a")
        right_ast = self._create_ast("COMPARISON", value="b")
        and_token = self._create_token("AND", line=2, column=10)
        eof_token = self._create_token("EOF")
        initial_state = self._create_parser_state(tokens=[and_token, eof_token])
        state_after = self._create_parser_state(tokens=[and_token, eof_token], pos=1)
        
        # 设置 mock 返回值
        mock_parse_comparison.side_effect = [
            (left_ast, initial_state),
            (right_ast, state_after)
        ]
        mock_peek.side_effect = [and_token, eof_token]
        mock_consume.return_value = state_after
        
        # 执行测试
        result_ast, result_state = _parse_and_expr(initial_state)
        
        # 验证 AST 节点所有必需字段
        self.assertIn("type", result_ast)
        self.assertIn("operator", result_ast)
        self.assertIn("children", result_ast)
        self.assertIn("value", result_ast)
        self.assertIn("line", result_ast)
        self.assertIn("column", result_ast)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["operator"], "and")
        self.assertEqual(result_ast["value"], None)
        self.assertIsInstance(result_ast["children"], list)
        self.assertEqual(len(result_ast["children"]), 2)


if __name__ == "__main__":
    unittest.main()
