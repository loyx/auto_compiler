# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_block 函数测试
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._handle_block_src import _handle_block

# 类型别名（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """_handle_block 函数单元测试类"""

    def setUp(self) -> None:
        """每个测试用例前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试用例后的清理工作"""
        pass

    def test_handle_block_empty_children(self) -> None:
        """测试空 block（无子节点）的情况"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证 _traverse_node 未被调用（因为没有子节点）
        mock_traverse.assert_not_called()
        # 验证作用域已恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_with_children(self) -> None:
        """测试包含多个子节点的 block"""
        child1: AST = {"type": "var_decl", "value": "x", "line": 2, "column": 5}
        child2: AST = {"type": "assignment", "value": "y", "line": 3, "column": 5}
        node: AST = {
            "type": "block",
            "children": [child1, child2],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证 _traverse_node 被调用了两次
        self.assertEqual(mock_traverse.call_count, 2)
        # 验证调用参数正确
        calls = mock_traverse.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], child1)
        self.assertEqual(calls[0][0][1], symbol_table)
        self.assertEqual(calls[1][0][0], child2)
        self.assertEqual(calls[1][0][1], symbol_table)
        # 验证作用域已恢复
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_management(self) -> None:
        """测试作用域层级管理（进入/离开 block）"""
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "x", "line": 2, "column": 5}],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [0, 1]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证作用域层级正确恢复
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [0, 1])

    def test_handle_block_missing_scope_stack(self) -> None:
        """测试 symbol_table 缺少 scope_stack 字段的情况"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证自动创建了 scope_stack
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["current_scope"], 1)

    def test_handle_block_missing_current_scope(self) -> None:
        """测试 symbol_table 缺少 current_scope 字段的情况"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "scope_stack": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证自动创建了 current_scope
        self.assertIn("current_scope", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 1)

    def test_handle_block_invalid_children_type(self) -> None:
        """测试 children 字段不是列表的情况"""
        node: AST = {
            "type": "block",
            "children": "invalid",  # 应该是列表
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证 _traverse_node 未被调用
        mock_traverse.assert_not_called()
        # 验证错误被记录
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Block node 'children' must be a list", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 5)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        # 验证作用域未被修改
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_invalid_children_type_missing_errors(self) -> None:
        """测试 children 字段不是列表且 symbol_table 缺少 errors 字段的情况"""
        node: AST = {
            "type": "block",
            "children": "invalid",
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证自动创建了 errors 列表
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_handle_block_nested_blocks(self) -> None:
        """测试嵌套 block 的作用域管理"""
        inner_child: AST = {"type": "var_decl", "value": "y", "line": 3, "column": 7}
        inner_block: AST = {
            "type": "block",
            "children": [inner_child],
            "line": 2,
            "column": 5
        }
        outer_child: AST = {"type": "var_decl", "value": "x", "line": 4, "column": 5}
        node: AST = {
            "type": "block",
            "children": [inner_block, outer_child],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        def traverse_side_effect(n: AST, st: SymbolTable) -> None:
            """模拟 _traverse_node 的行为，对 block 类型递归调用 _handle_block"""
            if n.get("type") == "block":
                _handle_block(n, st)

        with patch("._traverse_node_package._traverse_node_src._traverse_node", side_effect=traverse_side_effect):
            _handle_block(node, symbol_table)

        # 验证最终作用域恢复为 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_missing_children_field(self) -> None:
        """测试 node 缺少 children 字段的情况（应使用默认空列表）"""
        node: AST = {
            "type": "block",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证 _traverse_node 未被调用（默认空列表）
        mock_traverse.assert_not_called()
        # 验证作用域已恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_stack_not_empty_after_exit(self) -> None:
        """测试离开 block 时 scope_stack 非空的情况"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证作用域恢复到之前的值
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])


if __name__ == "__main__":
    unittest.main()
