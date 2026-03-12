# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_block 函数测试
"""

import unittest
from unittest.mock import patch

# 相对导入被测模块
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """_handle_block 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_handle_block_with_children_scope_management(self):
        """测试 block 有子节点时的作用域管理"""
        # 准备测试数据
        node = {
            "type": "block",
            "children": [
                {"type": "var_decl", "value": "x"},
                {"type": "assignment", "value": "y"}
            ],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        # 执行测试
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)  # 最终应恢复为 0
        self.assertEqual(symbol_table["scope_stack"], [])  # 栈应为空
        # 验证 _traverse_node 被调用了 2 次（每个子节点一次）
        self.assertEqual(mock_traverse.call_count, 2)
        # 验证调用参数
        mock_traverse.assert_any_call({"type": "var_decl", "value": "x"}, symbol_table)
        mock_traverse.assert_any_call({"type": "assignment", "value": "y"}, symbol_table)

    def test_handle_block_empty_children(self):
        """测试 block 子节点为空列表的情况"""
        node = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        # 验证 _traverse_node 未被调用
        self.assertEqual(mock_traverse.call_count, 0)

    def test_handle_block_missing_children_key(self):
        """测试 node 没有 children 键的情况（应使用默认空列表）"""
        node = {
            "type": "block",
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        # 验证 _traverse_node 未被调用
        self.assertEqual(mock_traverse.call_count, 0)

    def test_handle_block_missing_current_scope(self):
        """测试 symbol_table 没有 current_scope 键的情况（应默认为 0）"""
        node = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "x"}],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "scope_stack": [],
            "errors": []
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理：从 0 到 1 再回到 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(mock_traverse.call_count, 1)

    def test_handle_block_missing_scope_stack(self):
        """测试 symbol_table 没有 scope_stack 键的情况（应使用默认空列表）"""
        node = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "errors": []
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)
        # scope_stack 应该被创建并添加了值，然后弹出
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(mock_traverse.call_count, 0)

    def test_handle_block_nested_scope_restoration(self):
        """测试作用域层级正确恢复（验证栈操作）"""
        node = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 5,  # 从层级 5 开始
            "scope_stack": [0, 1, 2],  # 已有栈内容
            "errors": []
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node'):
            _handle_block(node, symbol_table)

        # 验证：进入 block 时 scope 变为 6，退出时恢复为 5
        self.assertEqual(symbol_table["current_scope"], 5)
        # 栈应该恢复原状
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2])

    def test_handle_block_scope_increment_during_execution(self):
        """测试执行过程中作用域层级确实增加了（通过 side_effect 验证）"""
        node = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "x"}],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        # 使用 side_effect 来验证 _traverse_node 被调用时的作用域层级
        def check_scope_side_effect(child_node, sym_table):
            # 在遍历子节点时，作用域应该是 1
            self.assertEqual(sym_table["current_scope"], 1)

        with patch('._traverse_node_package._traverse_node_src._traverse_node', side_effect=check_scope_side_effect):
            _handle_block(node, symbol_table)

        # 验证最终作用域恢复为 0
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_block_multiple_children_order(self):
        """测试多个子节点按顺序遍历"""
        children = [
            {"type": "var_decl", "value": "a"},
            {"type": "var_decl", "value": "b"},
            {"type": "var_decl", "value": "c"}
        ]
        node = {
            "type": "block",
            "children": children,
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证调用顺序
        self.assertEqual(mock_traverse.call_count, 3)
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0]["value"], "a")
        self.assertEqual(calls[1][0][0]["value"], "b")
        self.assertEqual(calls[2][0][0]["value"], "c")

    def test_handle_block_no_exception_on_error(self):
        """测试函数不抛出异常，即使遇到错误情况"""
        node = {
            "type": "block",
            "children": None,  # 异常情况
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        # 应该不会抛出异常
        try:
            with patch('._traverse_node_package._traverse_node_src._traverse_node'):
                _handle_block(node, symbol_table)
        except Exception as e:
            self.fail(f"_handle_block 不应抛出异常：{e}")

    def test_handle_block_preserves_other_symbol_table_fields(self):
        """测试不修改 symbol_table 的其他字段"""
        node = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": "main",
            "errors": ["some error"]
        }

        with patch('._traverse_node_package._traverse_node_src._traverse_node'):
            _handle_block(node, symbol_table)

        # 验证其他字段未被修改
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "int")
        self.assertEqual(symbol_table["current_function"], "main")
        self.assertEqual(symbol_table["errors"], ["some error"])


if __name__ == "__main__":
    unittest.main()
