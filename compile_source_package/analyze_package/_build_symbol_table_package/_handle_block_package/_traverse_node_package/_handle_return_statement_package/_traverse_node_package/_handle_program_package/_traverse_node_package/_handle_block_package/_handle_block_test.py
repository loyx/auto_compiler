# -*- coding: utf-8 -*-
"""单元测试：_handle_block 函数"""

import unittest
from unittest.mock import patch, call
from typing import Dict, Any, List

# 绝对导入被测试模块
from _handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """测试 _handle_block 函数的作用域管理逻辑"""

    def setUp(self):
        """每个测试前重置 mock"""
        self.traverse_node_patcher = patch('.._traverse_node_src._traverse_node')
        self.mock_traverse_node = self.traverse_node_patcher.start()

    def tearDown(self):
        """每个测试后停止 mock"""
        self.traverse_node_patcher.stop()

    def _create_symbol_table(self, current_scope: int = 0, scope_stack: List[int] = None) -> Dict[str, Any]:
        """创建符号表辅助函数"""
        if scope_stack is None:
            scope_stack = []
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": scope_stack,
            "errors": []
        }

    def _create_block_node(self, children: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建 block 类型 AST 节点辅助函数"""
        if children is None:
            children = []
        return {
            "type": "block",
            "children": children
        }

    def test_handle_block_empty_block(self):
        """测试空 block：没有子节点"""
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])
        node = self._create_block_node(children=[])

        _handle_block(node, symbol_table)

        # 进入 block 后 scope 应该为 1
        self.assertEqual(symbol_table["current_scope"], 0)
        # scope_stack 应该为空（进入时压入 1，退出时弹出）
        self.assertEqual(symbol_table["scope_stack"], [])
        # _traverse_node 不应该被调用
        self.mock_traverse_node.assert_not_called()

    def test_handle_block_single_child(self):
        """测试单个子节点的 block"""
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])
        child_node = {"type": "statement", "value": "test"}
        node = self._create_block_node(children=[child_node])

        _handle_block(node, symbol_table)

        # _traverse_node 应该被调用一次
        self.mock_traverse_node.assert_called_once_with(child_node, symbol_table)
        # 退出 block 后 scope 应该恢复为 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_multiple_children(self):
        """测试多个子节点的 block"""
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])
        child1 = {"type": "statement", "value": "stmt1"}
        child2 = {"type": "declaration", "value": "decl1"}
        child3 = {"type": "expression", "value": "expr1"}
        node = self._create_block_node(children=[child1, child2, child3])

        _handle_block(node, symbol_table)

        # _traverse_node 应该被调用 3 次
        self.assertEqual(self.mock_traverse_node.call_count, 3)
        expected_calls = [
            call(child1, symbol_table),
            call(child2, symbol_table),
            call(child3, symbol_table)
        ]
        self.mock_traverse_node.assert_has_calls(expected_calls)
        # 退出 block 后 scope 应该恢复为 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_nested_scope_initial(self):
        """测试已有作用域层级的 block"""
        symbol_table = self._create_symbol_table(current_scope=2, scope_stack=[1, 2])
        node = self._create_block_node(children=[])

        _handle_block(node, symbol_table)

        # 进入 block 时 scope 应该变为 3
        # 退出 block 后应该恢复为 2
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [1, 2])

    def test_handle_block_scope_stack_management(self):
        """测试作用域栈的正确管理"""
        symbol_table = self._create_symbol_table(current_scope=1, scope_stack=[1])
        node = self._create_block_node(children=[])

        _handle_block(node, symbol_table)

        # 进入时压入 2，退出时弹出，恢复为 1
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [1])

    def test_handle_block_deeply_nested_scope(self):
        """测试深层嵌套作用域"""
        symbol_table = self._create_symbol_table(current_scope=5, scope_stack=[1, 2, 3, 4, 5])
        child_node = {"type": "statement"}
        node = self._create_block_node(children=[child_node])

        _handle_block(node, symbol_table)

        # 进入时变为 6，退出时恢复为 5
        self.assertEqual(symbol_table["current_scope"], 5)
        self.assertEqual(symbol_table["scope_stack"], [1, 2, 3, 4, 5])
        self.mock_traverse_node.assert_called_once_with(child_node, symbol_table)

    def test_handle_block_no_scope_stack_field(self):
        """测试符号表没有 scope_stack 字段的情况"""
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        node = self._create_block_node(children=[])

        _handle_block(node, symbol_table)

        # 应该自动创建 scope_stack
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_block_no_current_scope_field(self):
        """测试符号表没有 current_scope 字段的情况"""
        symbol_table = {
            "variables": {},
            "scope_stack": []
        }
        node = self._create_block_node(children=[])

        _handle_block(node, symbol_table)

        # 应该默认从 0 开始
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_traverse_node_propagates_symbol_table(self):
        """测试 _traverse_node 接收正确的 symbol_table 引用"""
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])
        child_node = {"type": "statement"}
        node = self._create_block_node(children=[child_node])

        _handle_block(node, symbol_table)

        # 验证 _traverse_node 接收的是同一个 symbol_table 对象
        call_args = self.mock_traverse_node.call_args
        self.assertIs(call_args[0][1], symbol_table)

    def test_handle_block_children_missing_field(self):
        """测试 node 没有 children 字段的情况"""
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])
        node = {"type": "block"}  # 没有 children 字段

        _handle_block(node, symbol_table)

        # 不应该报错，_traverse_node 不应该被调用
        self.mock_traverse_node.assert_not_called()
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])


if __name__ == "__main__":
    unittest.main()
