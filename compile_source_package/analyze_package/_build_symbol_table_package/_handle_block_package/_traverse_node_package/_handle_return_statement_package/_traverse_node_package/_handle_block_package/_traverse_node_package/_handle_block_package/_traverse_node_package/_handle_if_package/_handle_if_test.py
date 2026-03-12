# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_if 函数测试
测试 _handle_if 函数处理 if 语句节点的逻辑
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict
import sys

# 先 mock 掉依赖模块，避免导入错误
mock_traverse_node = MagicMock()
sys.modules['projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._traverse_node_src'] = MagicMock()
sys.modules['projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._handle_block_src'] = MagicMock()

# 相对导入被测试模块
from ._handle_if_src import _handle_if

# 类型定义（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIf(unittest.TestCase):
    """_handle_if 函数的单元测试类"""

    def setUp(self) -> None:
        """测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_handle_if_with_single_child(self) -> None:
        """测试 if 节点有一个子节点的情况"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 1, "column": 5}
            ],
            "line": 1,
            "column": 1
        }

        with patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 被调用了一次
            self.assertEqual(mock_traverse.call_count, 1)
            # 验证调用参数正确
            mock_traverse.assert_called_with(node["children"][0], self.symbol_table)

    def test_handle_if_with_multiple_children(self) -> None:
        """测试 if 节点有多个子节点（条件、then 分支、else 分支）"""
        condition_node: AST = {"type": "binary_op", "value": ">", "line": 1, "column": 5}
        then_node: AST = {"type": "block", "children": [], "line": 1, "column": 10}
        else_node: AST = {"type": "block", "children": [], "line": 2, "column": 5}

        node: AST = {
            "type": "if",
            "children": [condition_node, then_node, else_node],
            "line": 1,
            "column": 1
        }

        with patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 被调用了三次
            self.assertEqual(mock_traverse.call_count, 3)
            # 验证每次调用的参数
            expected_calls = [
                unittest.mock.call(condition_node, self.symbol_table),
                unittest.mock.call(then_node, self.symbol_table),
                unittest.mock.call(else_node, self.symbol_table)
            ]
            mock_traverse.assert_has_calls(expected_calls, any_order=False)

    def test_handle_if_with_empty_children(self) -> None:
        """测试 if 节点的 children 为空列表的情况"""
        node: AST = {
            "type": "if",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # 不应该抛出异常
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 没有被调用
            mock_traverse.assert_not_called()

    def test_handle_if_without_children_key(self) -> None:
        """测试 if 节点没有 children 键的情况"""
        node: AST = {
            "type": "if",
            "line": 1,
            "column": 1
        }

        with patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # 不应该抛出异常
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 没有被调用
            mock_traverse.assert_not_called()

    def test_handle_if_with_none_children(self) -> None:
        """测试 if 节点的 children 为 None 的情况"""
        node: AST = {
            "type": "if",
            "children": None,
            "line": 1,
            "column": 1
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # 不应该抛出异常
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 没有被调用（None 被视为 falsy）
            mock_traverse.assert_not_called()

    def test_handle_if_preserves_symbol_table(self) -> None:
        """测试 symbol_table 被正确传递给 _traverse_node"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 1, "column": 5}
            ],
            "line": 1,
            "column": 1
        }

        # 添加一些初始数据到 symbol_table
        self.symbol_table["variables"]["x"] = {
            "data_type": "int",
            "is_declared": True,
            "line": 0,
            "column": 0,
            "scope_level": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_if(node, self.symbol_table)

            # 验证 symbol_table 被原样传递
            call_args = mock_traverse.call_args
            self.assertEqual(call_args[0][1], self.symbol_table)

    def test_handle_if_complex_nested_structure(self) -> None:
        """测试复杂的嵌套 if 节点结构"""
        nested_if_node: AST = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "y < 10", "line": 2, "column": 5},
                {"type": "block", "children": [], "line": 2, "column": 10}
            ],
            "line": 2,
            "column": 1
        }

        node: AST = {
            "type": "if",
            "children": [
                {"type": "binary_op", "value": ">", "line": 1, "column": 5},
                {"type": "block", "children": [nested_if_node], "line": 1, "column": 10},
                {"type": "block", "children": [], "line": 3, "column": 5}
            ],
            "line": 1,
            "column": 1
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 被调用了三次（只处理直接子节点，不递归）
            self.assertEqual(mock_traverse.call_count, 3)

    def test_handle_if_minimal_node_structure(self) -> None:
        """测试最小化的 if 节点结构（只有 type）"""
        node: AST = {
            "type": "if"
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # 不应该抛出异常
            _handle_if(node, self.symbol_table)

            # 验证 _traverse_node 没有被调用
            mock_traverse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
