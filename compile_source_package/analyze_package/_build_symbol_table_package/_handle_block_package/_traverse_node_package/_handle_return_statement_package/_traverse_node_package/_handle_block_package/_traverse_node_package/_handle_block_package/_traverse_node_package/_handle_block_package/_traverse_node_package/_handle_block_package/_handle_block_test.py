# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_block 函数测试
测试 block 节点处理逻辑，包括作用域管理和子节点遍历
"""

import unittest
from unittest.mock import patch, call

# 相对导入被测模块
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """_handle_block 函数测试类"""

    def setUp(self):
        """测试前准备"""
        pass

    def tearDown(self):
        """测试后清理"""
        pass

    def test_handle_block_with_children_scope_management(self):
        """测试有子节点的 block：验证作用域正确进入和退出"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": [
                {"type": "var_decl", "name": "x"},
                {"type": "assignment", "name": "x", "value": 10}
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None

            # 执行测试
            _handle_block(node, symbol_table)

            # 验证作用域变化
            self.assertEqual(symbol_table["current_scope"], 0)  # 退出后应恢复为 0
            self.assertEqual(len(symbol_table["scope_stack"]), 0)  # 栈应为空

            # 验证 _traverse_node 被调用两次（两个子节点）
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_has_calls([
                call({"type": "var_decl", "name": "x"}, symbol_table),
                call({"type": "assignment", "name": "x", "value": 10}, symbol_table)
            ])

    def test_handle_block_without_children(self):
        """测试没有子节点的 block：作用域仍应正确管理"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            # 执行测试
            _handle_block(node, symbol_table)

            # 验证作用域变化
            self.assertEqual(symbol_table["current_scope"], 0)  # 退出后应恢复为 0
            self.assertEqual(len(symbol_table["scope_stack"]), 0)  # 栈应为空

            # 验证 _traverse_node 未被调用
            mock_traverse.assert_not_called()

    def test_handle_block_without_children_key(self):
        """测试没有 children 键的 block：应使用默认空列表"""
        # 准备测试数据
        node = {
            "type": "block"
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            # 执行测试
            _handle_block(node, symbol_table)

            # 验证作用域变化
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["scope_stack"]), 0)

            # 验证 _traverse_node 未被调用
            mock_traverse.assert_not_called()

    def test_handle_block_initializes_missing_scope_fields(self):
        """测试 symbol_table 缺少 scope 字段时：应自动初始化"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {}
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            # 执行测试
            _handle_block(node, symbol_table)

            # 验证字段被初始化
            self.assertIn("scope_stack", symbol_table)
            self.assertIn("current_scope", symbol_table)
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["scope_stack"]), 0)

    def test_handle_block_with_existing_scope_level(self):
        """测试从非零作用域层级进入 block：应正确递增和恢复"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": []
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            # 执行测试
            _handle_block(node, symbol_table)

            # 验证作用域变化
            self.assertEqual(symbol_table["current_scope"], 2)  # 退出后应恢复为 2
            self.assertEqual(len(symbol_table["scope_stack"]), 0)

    def test_handle_block_nested_scopes(self):
        """测试嵌套 block：作用域栈应正确管理"""
        # 准备测试数据
        outer_node = {
            "type": "block",
            "children": [
                {
                    "type": "block",
                    "children": []
                }
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Mock _traverse_node 以递归调用 _handle_block
        def mock_traverse_impl(node, symbol_table):
            if node["type"] == "block":
                # 递归调用 _handle_block
                from ._handle_block_src import _handle_block
                _handle_block(node, symbol_table)

        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node", side_effect=mock_traverse_impl):
            # 执行测试
            _handle_block(outer_node, symbol_table)

            # 验证最终作用域状态
            self.assertEqual(symbol_table["current_scope"], 0)  # 应恢复为 0
            self.assertEqual(len(symbol_table["scope_stack"]), 0)  # 栈应为空

    def test_handle_block_exception_during_traversal(self):
        """测试遍历子节点时抛出异常：作用域仍应正确退出"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": [
                {"type": "var_decl", "name": "x"}
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Mock _traverse_node 抛出异常
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            mock_traverse.side_effect = RuntimeError("Test exception")

            # 执行测试并捕获异常
            with self.assertRaises(RuntimeError):
                _handle_block(node, symbol_table)

            # 验证即使抛出异常，作用域仍被恢复
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["scope_stack"]), 0)

    def test_handle_block_multiple_children(self):
        """测试多个子节点：所有子节点都应被遍历"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": [
                {"type": "var_decl", "name": "a"},
                {"type": "var_decl", "name": "b"},
                {"type": "assignment", "name": "a", "value": 1},
                {"type": "assignment", "name": "b", "value": 2}
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None

            # 执行测试
            _handle_block(node, symbol_table)

            # 验证 _traverse_node 被调用 4 次
            self.assertEqual(mock_traverse.call_count, 4)

    def test_handle_block_scope_increment(self):
        """测试作用域递增逻辑：进入 block 时 current_scope 应 +1"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": []
        }

        # Mock _traverse_node 以检查中间状态
        def check_scope_during_traversal(node, symbol_table):
            # 在遍历期间，current_scope 应该是 6
            self.assertEqual(symbol_table["current_scope"], 6)

        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node", side_effect=check_scope_during_traversal):
            # 执行测试
            _handle_block(node, symbol_table)

            # 验证最终恢复
            self.assertEqual(symbol_table["current_scope"], 5)

    def test_handle_block_preserves_other_symbol_table_fields(self):
        """测试其他 symbol_table 字段不被修改"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": "main",
            "errors": []
        }

        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_src._traverse_node") as mock_traverse:
            # 执行测试
            _handle_block(node, symbol_table)

            # 验证其他字段未被修改
            self.assertEqual(symbol_table["variables"], {"x": {"data_type": "int", "is_declared": True}})
            self.assertEqual(symbol_table["functions"], {"main": {"return_type": "int"}})
            self.assertEqual(symbol_table["current_function"], "main")
            self.assertEqual(symbol_table["errors"], [])


if __name__ == "__main__":
    unittest.main()
