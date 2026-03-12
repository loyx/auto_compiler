# -*- coding: utf-8 -*-
"""单元测试文件：_handle_expression 函数测试"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# 相对导入被测模块
from ._handle_expression_src import _handle_expression

# 类型定义
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleExpression(unittest.TestCase):
    """_handle_expression 函数的单元测试类"""

    def setUp(self) -> None:
        """测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_with_children(self, mock_traverse_node: MagicMock) -> None:
        """测试：表达式节点包含多个子节点"""
        node: AST = {
            "type": "binary_op",
            "value": "+",
            "line": 1,
            "column": 5,
            "children": [
                {"type": "identifier", "value": "a", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 7}
            ]
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_any_call(
            {"type": "identifier", "value": "a", "line": 1, "column": 3},
            self.symbol_table
        )
        mock_traverse_node.assert_any_call(
            {"type": "identifier", "value": "b", "line": 1, "column": 7},
            self.symbol_table
        )

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_with_empty_children(self, mock_traverse_node: MagicMock) -> None:
        """测试：表达式节点包含空子节点列表"""
        node: AST = {
            "type": "expression",
            "value": "x",
            "line": 1,
            "column": 5,
            "children": []
        }

        _handle_expression(node, self.symbol_table)

        mock_traverse_node.assert_not_called()

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_without_children_key(self, mock_traverse_node: MagicMock) -> None:
        """测试：表达式节点没有 children 键（使用默认空列表）"""
        node: AST = {
            "type": "expression",
            "value": "x",
            "line": 1,
            "column": 5
        }

        _handle_expression(node, self.symbol_table)

        mock_traverse_node.assert_not_called()

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_with_single_child(self, mock_traverse_node: MagicMock) -> None:
        """测试：表达式节点包含单个子节点"""
        node: AST = {
            "type": "expression",
            "value": "x",
            "line": 1,
            "column": 5,
            "children": [
                {"type": "literal", "value": 42, "line": 1, "column": 5}
            ]
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(
            {"type": "literal", "value": 42, "line": 1, "column": 5},
            self.symbol_table
        )

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_with_nested_expressions(self, mock_traverse_node: MagicMock) -> None:
        """测试：表达式节点包含嵌套表达式子节点"""
        node: AST = {
            "type": "binary_op",
            "value": "*",
            "line": 2,
            "column": 10,
            "children": [
                {
                    "type": "binary_op",
                    "value": "+",
                    "line": 2,
                    "column": 8,
                    "children": [
                        {"type": "identifier", "value": "a", "line": 2, "column": 6},
                        {"type": "identifier", "value": "b", "line": 2, "column": 10}
                    ]
                },
                {"type": "identifier", "value": "c", "line": 2, "column": 14}
            ]
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(mock_traverse_node.call_count, 2)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_preserves_symbol_table(self, mock_traverse_node: MagicMock) -> None:
        """测试：符号表在调用过程中被正确传递"""
        node: AST = {
            "type": "expression",
            "value": "test",
            "children": [
                {"type": "identifier", "value": "var1"}
            ]
        }

        _handle_expression(node, self.symbol_table)

        mock_traverse_node.assert_called_once()
        call_args = mock_traverse_node.call_args
        self.assertIs(call_args[0][1], self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_with_complex_binary_op(self, mock_traverse_node: MagicMock) -> None:
        """测试：复杂二元运算符表达式（如 ==, !=, <=, >=）"""
        node: AST = {
            "type": "binary_op",
            "value": "==",
            "line": 5,
            "column": 20,
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 18},
                {"type": "literal", "value": 0, "line": 5, "column": 23}
            ]
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(mock_traverse_node.call_count, 2)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_expression_with_many_children(self, mock_traverse_node: MagicMock) -> None:
        """测试：表达式节点包含多个子节点（边界测试）"""
        children = [
            {"type": "identifier", "value": f"var{i}", "line": 1, "column": i}
            for i in range(10)
        ]
        node: AST = {
            "type": "expression",
            "value": "func_call",
            "line": 1,
            "column": 1,
            "children": children
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(mock_traverse_node.call_count, 10)


if __name__ == "__main__":
    unittest.main()
