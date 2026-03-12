# -*- coding: utf-8 -*-
"""单元测试文件：_handle_expression 函数测试"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# 相对导入被测模块
from ._handle_expression_src import _handle_expression

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleExpression(unittest.TestCase):
    """_handle_expression 函数单元测试类"""

    def test_handle_expression_normal_with_children(self):
        """测试正常情况：表达式有多个子节点"""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "identifier", "value": "a"},
                {"type": "number", "value": 5}
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {"a": {"data_type": "int", "is_declared": True}},
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse, \
             patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._check_expression_types_package._check_expression_types_src._check_expression_types") as mock_check:
            
            _handle_expression(node, symbol_table)

            # 验证 _traverse_node 被调用两次（每个子节点一次）
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call({"type": "identifier", "value": "a"}, symbol_table)
            mock_traverse.assert_any_call({"type": "number", "value": 5}, symbol_table)

            # 验证 _check_expression_types 被调用一次
            mock_check.assert_called_once_with(node, symbol_table)

    def test_handle_expression_no_children(self):
        """测试边界情况：表达式没有子节点"""
        node: AST = {
            "type": "expression",
            "value": "42",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse, \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types") as mock_check:
            
            _handle_expression(node, symbol_table)

            # 验证 _traverse_node 没有被调用
            mock_traverse.assert_not_called()

            # 验证 _check_expression_types 仍被调用
            mock_check.assert_called_once_with(node, symbol_table)

    def test_handle_expression_symbol_table_without_errors(self):
        """测试边界情况：符号表没有 errors 键，应自动初始化"""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"), \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types"):
            
            _handle_expression(node, symbol_table)

            # 验证 errors 列表被创建
            self.assertIn("errors", symbol_table)
            self.assertIsInstance(symbol_table["errors"], list)
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_expression_symbol_table_with_existing_errors(self):
        """测试边界情况：符号表已有 errors 列表，不应覆盖"""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": []
        }
        existing_errors = ["existing error"]
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": existing_errors
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"), \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types"):
            
            _handle_expression(node, symbol_table)

            # 验证 errors 列表未被替换
            self.assertIs(symbol_table["errors"], existing_errors)

    def test_handle_expression_single_child(self):
        """测试边界情况：表达式只有一个子节点"""
        node: AST = {
            "type": "expression",
            "value": "-",
            "children": [
                {"type": "identifier", "value": "x"}
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse, \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types") as mock_check:
            
            _handle_expression(node, symbol_table)

            # 验证 _traverse_node 被调用一次
            mock_traverse.assert_called_once_with({"type": "identifier", "value": "x"}, symbol_table)

            # 验证 _check_expression_types 被调用一次
            mock_check.assert_called_once_with(node, symbol_table)

    def test_handle_expression_nested_children(self):
        """测试复杂情况：表达式有嵌套子节点"""
        node: AST = {
            "type": "expression",
            "value": "*",
            "children": [
                {
                    "type": "expression",
                    "value": "+",
                    "children": [
                        {"type": "number", "value": 1},
                        {"type": "number", "value": 2}
                    ]
                },
                {"type": "number", "value": 3}
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse, \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types") as mock_check:
            
            _handle_expression(node, symbol_table)

            # 验证 _traverse_node 被调用两次（顶层两个子节点）
            self.assertEqual(mock_traverse.call_count, 2)

            # 验证 _check_expression_types 被调用一次
            mock_check.assert_called_once_with(node, symbol_table)

    def test_handle_expression_preserves_other_symbol_table_fields(self):
        """测试副作用：不修改符号表的其他字段"""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {"x": {"data_type": "int"}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"), \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types"):
            
            _handle_expression(node, symbol_table)

            # 验证其他字段未被修改
            self.assertEqual(symbol_table["variables"], {"x": {"data_type": "int"}})
            self.assertEqual(symbol_table["functions"], {"main": {"return_type": "int"}})
            self.assertEqual(symbol_table["current_scope"], 1)
            self.assertEqual(symbol_table["scope_stack"], [1])

    def test_handle_expression_with_line_column_info(self):
        """测试带行号列号信息的节点"""
        node: AST = {
            "type": "expression",
            "value": "/",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "identifier", "value": "a", "line": 10, "column": 7}
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse, \
             patch("._check_expression_types_package._check_expression_types_src._check_expression_types") as mock_check:
            
            _handle_expression(node, symbol_table)

            # 验证节点信息被正确传递
            mock_traverse.assert_called_once()
            mock_check.assert_called_once_with(node, symbol_table)


if __name__ == "__main__":
    unittest.main()
