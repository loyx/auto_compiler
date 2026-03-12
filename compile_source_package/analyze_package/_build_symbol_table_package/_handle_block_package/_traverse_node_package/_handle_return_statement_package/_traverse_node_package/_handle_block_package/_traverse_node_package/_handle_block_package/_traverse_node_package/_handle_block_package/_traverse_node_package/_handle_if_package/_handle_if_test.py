import unittest
from unittest.mock import patch, call

# Relative import from the same package
from ._handle_if_src import _handle_if


class TestHandleIf(unittest.TestCase):
    """单元测试：_handle_if 函数"""

    # Mock path for _traverse_node from parent package
    TRAVERSE_NODE_PATH = (
        "main_package.compile_source_package.analyze_package."
        "_build_symbol_table_package._handle_block_package."
        "_traverse_node_package._handle_return_statement_package."
        "_traverse_node_package._handle_block_package."
        "_traverse_node_package._handle_block_package."
        "_traverse_node_package._handle_block_package."
        "_traverse_node_package._traverse_node"
    )

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_with_two_children(self, mock_traverse):
        """Happy path: if 节点包含 condition 和 then_block（无 else）"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0"},
                {"type": "block", "children": []}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # 验证 _traverse_node 被调用 2 次（condition + then_block）
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call(node["children"][0], symbol_table),
            call(node["children"][1], symbol_table)
        ])
        # 不应记录错误
        self.assertNotIn("errors", symbol_table)

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_with_three_children(self, mock_traverse):
        """Happy path: if 节点包含 condition、then_block 和 else_block"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0"},
                {"type": "block", "children": []},
                {"type": "block", "children": []}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # 验证 _traverse_node 被调用 3 次
        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_has_calls([
            call(node["children"][0], symbol_table),
            call(node["children"][1], symbol_table),
            call(node["children"][2], symbol_table)
        ])
        # 不应记录错误
        self.assertNotIn("errors", symbol_table)

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_with_zero_children(self, mock_traverse):
        """边界值：if 节点没有子节点 - 应记录错误"""
        node = {
            "type": "if",
            "children": [],
            "line": 10,
            "column": 5
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # _traverse_node 不应被调用
        mock_traverse.assert_not_called()
        # 应记录错误
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("缺少必要的子节点", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_with_one_child(self, mock_traverse):
        """边界值：if 节点只有 1 个子节点 - 应记录错误"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0"}
            ],
            "line": 15,
            "column": 8
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # _traverse_node 不应被调用
        mock_traverse.assert_not_called()
        # 应记录错误
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("缺少必要的子节点", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 15)
        self.assertEqual(symbol_table["errors"][0]["column"], 8)

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_without_children_key(self, mock_traverse):
        """边界值：if 节点没有 children 键 - 应默认为空列表并记录错误"""
        node = {
            "type": "if",
            "line": 20,
            "column": 3
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # _traverse_node 不应被调用
        mock_traverse.assert_not_called()
        # 应记录错误
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("缺少必要的子节点", symbol_table["errors"][0]["message"])

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_preserves_existing_errors(self, mock_traverse):
        """副作用验证：symbol_table 中已存在的错误应被保留"""
        node = {
            "type": "if",
            "children": [],
            "line": 25,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "errors": [{"message": "previous error", "line": 1, "column": 1}]
        }

        _handle_if(node, symbol_table)

        # 应有 2 个错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "previous error")
        self.assertIn("缺少必要的子节点", symbol_table["errors"][1]["message"])

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_creates_errors_list_if_not_exists(self, mock_traverse):
        """边界值：symbol_table 没有 errors 键时应创建"""
        node = {
            "type": "if",
            "children": [],
            "line": 30,
            "column": 2
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # 应创建 errors 列表
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_with_missing_line_column(self, mock_traverse):
        """边界值：节点缺少 line/column 信息时应使用默认值 -1"""
        node = {
            "type": "if",
            "children": []
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        _handle_if(node, symbol_table)

        # 应记录错误，使用默认值 -1
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["errors"][0]["line"], -1)
        self.assertEqual(symbol_table["errors"][0]["column"], -1)

    @patch(TRAVERSE_NODE_PATH)
    def test_handle_if_traverse_node_propagates_side_effects(self, mock_traverse):
        """副作用验证：_traverse_node 的副作用应通过 symbol_table 传播"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0"},
                {"type": "block", "children": []}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}

        # 模拟 _traverse_node 修改 symbol_table
        def side_effect(child, st):
            if "modified" not in st:
                st["modified"] = True

        mock_traverse.side_effect = side_effect

        _handle_if(node, symbol_table)

        # 验证副作用已传播
        self.assertTrue(symbol_table.get("modified", False))
        self.assertEqual(mock_traverse.call_count, 2)


if __name__ == '__main__':
    unittest.main()
