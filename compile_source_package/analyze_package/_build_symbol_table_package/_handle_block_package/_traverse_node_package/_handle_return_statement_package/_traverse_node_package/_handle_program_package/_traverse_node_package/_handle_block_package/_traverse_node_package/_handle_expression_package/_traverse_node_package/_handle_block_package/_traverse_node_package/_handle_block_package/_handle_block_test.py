# === std / third-party imports ===
import unittest
from unittest.mock import patch
from copy import deepcopy

# === sub function imports ===
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """测试 _handle_block 函数的作用域管理和子节点遍历"""

    def setUp(self):
        """准备测试夹具"""
        self.base_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

    def test_handle_block_with_children(self):
        """测试处理带有子节点的 block - 正常路径"""
        node = {
            "type": "block",
            "children": [
                {"type": "statement", "value": "stmt1"},
                {"type": "statement", "value": "stmt2"},
            ],
        }
        symbol_table = deepcopy(self.base_symbol_table)

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 被调用
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call({"type": "statement", "value": "stmt1"}, symbol_table)
        mock_traverse.assert_any_call({"type": "statement", "value": "stmt2"}, symbol_table)

    def test_handle_block_empty_children(self):
        """测试处理空 block（无子节点）"""
        node = {
            "type": "block",
            "children": [],
        }
        symbol_table = deepcopy(self.base_symbol_table)

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 未被调用
        mock_traverse.assert_not_called()

    def test_handle_block_no_children_key(self):
        """测试处理没有 children 键的 node"""
        node = {
            "type": "block",
        }
        symbol_table = deepcopy(self.base_symbol_table)

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 未被调用
        mock_traverse.assert_not_called()

    def test_handle_block_scope_management(self):
        """测试作用域的正确进入和退出"""
        node = {
            "type": "block",
            "children": [],
        }
        symbol_table = deepcopy(self.base_symbol_table)

        # 初始状态
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        with patch("._handle_block_src._traverse_node"):
            # 在函数执行过程中检查作用域状态
            def check_scope_during(child, st):
                self.assertEqual(st["current_scope"], 1)
                self.assertEqual(st["scope_stack"], [1])
                return None

            with patch("._handle_block_src._traverse_node", side_effect=check_scope_during):
                _handle_block(node, symbol_table)

        # 退出后应恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_exit_on_exception(self):
        """测试即使子节点处理抛出异常，作用域也能正确退出（finally 块）"""
        node = {
            "type": "block",
            "children": [
                {"type": "statement", "value": "stmt1"},
            ],
        }
        symbol_table = deepcopy(self.base_symbol_table)

        with patch("._handle_block_src._traverse_node", side_effect=Exception("Test exception")):
            with self.assertRaises(Exception):
                _handle_block(node, symbol_table)

        # 即使抛出异常，finally 块也应执行，作用域应恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_nested_scope_start(self):
        """测试从非零作用域开始的情况"""
        node = {
            "type": "block",
            "children": [],
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [1, 2],
        }

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [1, 2])

    def test_handle_block_multiple_children_order(self):
        """测试多个子节点按顺序处理"""
        node = {
            "type": "block",
            "children": [
                {"type": "statement", "value": "first"},
                {"type": "statement", "value": "second"},
                {"type": "statement", "value": "third"},
            ],
        }
        symbol_table = deepcopy(self.base_symbol_table)
        call_order = []

        def track_calls(child, st):
            call_order.append(child["value"])
            return None

        with patch("._handle_block_src._traverse_node", side_effect=track_calls):
            _handle_block(node, symbol_table)

        # 验证调用顺序
        self.assertEqual(call_order, ["first", "second", "third"])

    def test_handle_block_scope_stack_growth(self):
        """测试 scope_stack 的增长和收缩"""
        node = {
            "type": "block",
            "children": [],
        }
        symbol_table = deepcopy(self.base_symbol_table)

        # 初始状态
        initial_stack_len = len(symbol_table["scope_stack"])

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证 stack 长度恢复
        self.assertEqual(len(symbol_table["scope_stack"]), initial_stack_len)


if __name__ == "__main__":
    unittest.main()
