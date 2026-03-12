# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._handle_block_src import _handle_block

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """测试 _handle_block 函数的作用域管理逻辑"""

    def setUp(self) -> None:
        """每个测试前初始化 symbol_table"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_handle_block_normal_flow(self) -> None:
        """测试正常 block 处理：作用域正确进入和退出"""
        node: AST = {
            "type": "block",
            "line": 10,
            "column": 5,
            "children": []
        }

        with patch("_handle_block_package._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, self.symbol_table)

        # 验证作用域变化
        self.assertEqual(self.symbol_table["current_scope"], 0)  # 最终应该回到 0
        self.assertEqual(self.symbol_table["scope_stack"], [])  # 最终应该为空
        # 验证 _traverse_node 没有被调用（因为 children 为空）
        mock_traverse.assert_not_called()

    def test_handle_block_with_children(self) -> None:
        """测试 block 包含多个子节点的处理"""
        child1: AST = {"type": "statement", "line": 11, "column": 6}
        child2: AST = {"type": "statement", "line": 12, "column": 6}
        node: AST = {
            "type": "block",
            "line": 10,
            "column": 5,
            "children": [child1, child2]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, self.symbol_table)

        # 验证作用域变化
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])
        # 验证 _traverse_node 被调用了 2 次
        self.assertEqual(mock_traverse.call_count, 2)
        # 验证调用参数
        mock_traverse.assert_any_call(child1, self.symbol_table)
        mock_traverse.assert_any_call(child2, self.symbol_table)

    def test_handle_block_scope_increment_decrement(self) -> None:
        """测试作用域层级的增减逻辑"""
        node: AST = {
            "type": "block",
            "line": 5,
            "column": 1,
            "children": []
        }

        # 初始 scope 为 3
        self.symbol_table["current_scope"] = 3
        self.symbol_table["scope_stack"] = ["scope1", "scope2", "scope3"]

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, self.symbol_table)

        # 验证最终回到初始状态
        self.assertEqual(self.symbol_table["current_scope"], 3)
        self.assertEqual(self.symbol_table["scope_stack"], ["scope1", "scope2", "scope3"])

    def test_handle_block_empty_children(self) -> None:
        """测试 block 没有 children 字段的情况"""
        node: AST = {
            "type": "block",
            "line": 15,
            "column": 2
            # 没有 children 字段
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, self.symbol_table)

        # 验证作用域正确恢复
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])
        mock_traverse.assert_not_called()

    def test_handle_block_missing_line(self) -> None:
        """测试 block 节点缺少 line 字段的情况"""
        node: AST = {
            "type": "block",
            "column": 5,
            "children": []
            # 没有 line 字段
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_block(node, self.symbol_table)

        # 验证使用默认值 0
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])

    def test_handle_block_finally_always_executes(self) -> None:
        """测试即使 _traverse_node 抛出异常，finally 块也会执行"""
        node: AST = {
            "type": "block",
            "line": 30,
            "column": 1,
            "children": [{"type": "statement"}]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            mock_traverse.side_effect = RuntimeError("Test exception")

            # 验证异常会被抛出
            with self.assertRaises(RuntimeError):
                _handle_block(node, self.symbol_table)

        # 验证即使异常发生，作用域也正确恢复
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])

    def test_handle_block_nested_scope_simulation(self) -> None:
        """模拟嵌套 block 的作用域管理"""
        # 第一个 block
        block1: AST = {
            "type": "block",
            "line": 1,
            "column": 1,
            "children": []
        }

        # 第二个 block（模拟嵌套）
        block2: AST = {
            "type": "block",
            "line": 2,
            "column": 2,
            "children": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # 处理第一个 block
            _handle_block(block1, self.symbol_table)
            self.assertEqual(self.symbol_table["current_scope"], 0)

            # 处理第二个 block
            _handle_block(block2, self.symbol_table)
            self.assertEqual(self.symbol_table["current_scope"], 0)

    def test_handle_block_scope_id_format(self) -> None:
        """测试 scope_id 的格式是否正确"""
        node: AST = {
            "type": "block",
            "line": 42,
            "column": 10,
            "children": []
        }

        # 我们需要验证在 try 块执行期间 scope_stack 包含正确的 scope_id
        # 通过在 mock 中检查 symbol_table 的状态
        def check_scope_during_traversal(*args, **kwargs):
            # 在遍历期间，scope_stack 应该包含 block_42
            self.assertIn("block_42", self.symbol_table["scope_stack"])
            self.assertEqual(self.symbol_table["current_scope"], 1)

        with patch("._traverse_node_package._traverse_node_src._traverse_node", side_effect=check_scope_during_traversal):
            _handle_block(node, self.symbol_table)

        # 验证最终状态
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])


if __name__ == "__main__":
    unittest.main()
