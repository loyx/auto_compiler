# -*- coding: utf-8 -*-
"""单元测试：_handle_while_loop 函数"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# 相对导入被测模块
from ._handle_while_loop_src import _handle_while_loop

# 类型定义（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhileLoop(unittest.TestCase):
    """_handle_while_loop 函数的单元测试"""

    def setUp(self) -> None:
        """测试前准备"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_while_loop_both_condition_and_body(self, mock_traverse: MagicMock) -> None:
        """测试：condition 和 body 都存在的情况"""
        condition_node: AST = {"type": "binary_op", "value": "x > 0"}
        body_node: AST = {"type": "block", "children": []}
        
        node: AST = {
            "type": "while_loop",
            "condition": condition_node,
            "body": body_node,
            "line": 10,
            "column": 5
        }
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 被调用两次
        self.assertEqual(mock_traverse.call_count, 2)
        # 验证第一次调用传入 condition
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        # 验证第二次调用传入 body
        mock_traverse.assert_any_call(body_node, self.symbol_table)

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_only_condition(self, mock_traverse: MagicMock) -> None:
        """测试：只有 condition，body 为 None"""
        condition_node: AST = {"type": "binary_op", "value": "x > 0"}
        
        node: AST = {
            "type": "while_loop",
            "condition": condition_node,
            "body": None,
            "line": 10,
            "column": 5
        }
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 只被调用一次（仅 condition）
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_once_with(condition_node, self.symbol_table)

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_only_body(self, mock_traverse: MagicMock) -> None:
        """测试：只有 body，condition 为 None"""
        body_node: AST = {"type": "block", "children": []}
        
        node: AST = {
            "type": "while_loop",
            "condition": None,
            "body": body_node,
            "line": 10,
            "column": 5
        }
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 只被调用一次（仅 body）
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_once_with(body_node, self.symbol_table)

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_both_none(self, mock_traverse: MagicMock) -> None:
        """测试：condition 和 body 都为 None"""
        node: AST = {
            "type": "while_loop",
            "condition": None,
            "body": None,
            "line": 10,
            "column": 5
        }
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse.assert_not_called()

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_missing_keys(self, mock_traverse: MagicMock) -> None:
        """测试：node 中没有 condition 或 body 键（使用 get 返回 None）"""
        node: AST = {
            "type": "while_loop",
            "line": 10,
            "column": 5
        }
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse.assert_not_called()

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_empty_node(self, mock_traverse: MagicMock) -> None:
        """测试：空节点"""
        node: AST = {}
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse.assert_not_called()

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_symbol_table_unchanged_structure(self, mock_traverse: MagicMock) -> None:
        """测试：symbol_table 的基本结构保持不变"""
        condition_node: AST = {"type": "binary_op"}
        body_node: AST = {"type": "block"}
        
        node: AST = {
            "type": "while_loop",
            "condition": condition_node,
            "body": body_node
        }
        
        original_keys = set(self.symbol_table.keys())
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 symbol_table 的顶层键没有变化
        self.assertEqual(set(self.symbol_table.keys()), original_keys)

    @patch("_traverse_node_src._traverse_node")
    def test_handle_while_loop_complex_nested_structure(self, mock_traverse: MagicMock) -> None:
        """测试：复杂的嵌套 AST 结构"""
        condition_node: AST = {
            "type": "binary_op",
            "left": {"type": "identifier", "value": "x"},
            "operator": ">",
            "right": {"type": "literal", "value": 0}
        }
        body_node: AST = {
            "type": "block",
            "children": [
                {"type": "assignment", "target": "y", "value": {"type": "literal", "value": 1}},
                {"type": "function_call", "name": "print", "args": [{"type": "identifier", "value": "y"}]}
            ]
        }
        
        node: AST = {
            "type": "while_loop",
            "condition": condition_node,
            "body": body_node,
            "line": 15,
            "column": 1
        }
        
        _handle_while_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 被调用两次
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        mock_traverse.assert_any_call(body_node, self.symbol_table)


if __name__ == "__main__":
    unittest.main()
