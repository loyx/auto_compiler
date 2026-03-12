# === test file for _handle_block ===
import unittest
from unittest.mock import patch

# === relative import for UUT ===
from ._handle_block_src import _handle_block, AST, SymbolTable


class TestHandleBlock(unittest.TestCase):
    """单元测试：_handle_block 函数"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_handle_block_normal_with_children(self) -> None:
        """Happy Path: 正常 block 节点，包含子节点"""
        # Arrange
        node: AST = {
            "type": "block",
            "children": [
                {"type": "var_decl", "name": "x", "data_type": "int"},
                {"type": "var_decl", "name": "y", "data_type": "char"},
            ],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": [],
        }

        # Act & Assert: mock _traverse_node to verify it's called for each child
        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # Verify _traverse_node called twice (once per child)
            self.assertEqual(mock_traverse.call_count, 2)
            # Verify calls with correct arguments
            mock_traverse.assert_any_call(node["children"][0], symbol_table)
            mock_traverse.assert_any_call(node["children"][1], symbol_table)

            # Verify scope management
            self.assertEqual(symbol_table["current_scope"], 1)  # Restored to old value
            self.assertEqual(symbol_table["scope_stack"], [])  # Stack empty after pop

    def test_handle_block_empty_children(self) -> None:
        """边界值：block 节点，children 为空列表"""
        # Arrange
        node: AST = {
            "type": "block",
            "children": [],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [],
            "errors": [],
        }

        # Act
        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # Assert
            mock_traverse.assert_not_called()
            self.assertEqual(symbol_table["current_scope"], 2)  # Restored
            self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_no_children_field(self) -> None:
        """边界值：block 节点，没有 children 字段"""
        # Arrange
        node: AST = {
            "type": "block",
            "value": "some_value",
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": [],
        }

        # Act
        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # Assert
            mock_traverse.assert_not_called()
            self.assertEqual(symbol_table["current_scope"], 0)  # Restored
            self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_nested_scope_management(self) -> None:
        """多分支逻辑：嵌套 block 的作用域管理"""
        # Arrange
        outer_node: AST = {
            "type": "block",
            "children": [{"type": "block", "children": []}],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": [],
        }

        # Act: manually simulate nested block handling
        with patch("._handle_block_src._traverse_node") as mock_traverse:
            # First call handles outer block
            def traverse_side_effect(child_node: AST, sym_table: SymbolTable) -> None:
                if child_node["type"] == "block":
                    # Simulate nested block handling
                    old_scope = sym_table.get("current_scope", 0)
                    sym_table.setdefault("scope_stack", []).append(old_scope)
                    sym_table["current_scope"] = old_scope + 1
                    # Exit nested block
                    sym_table["current_scope"] = sym_table["scope_stack"].pop()

            mock_traverse.side_effect = traverse_side_effect
            _handle_block(outer_node, symbol_table)

            # Assert
            self.assertEqual(symbol_table["current_scope"], 1)  # Back to original
            self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_stack_operations(self) -> None:
        """状态变化：验证 scope_stack 的压栈和弹栈操作"""
        # Arrange
        node: AST = {
            "type": "block",
            "children": [],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": [1, 2],  # Pre-existing stack
            "errors": [],
        }

        # Act
        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

            # Assert
            # During execution: scope_stack becomes [1, 2, 5], current_scope becomes 6
            # After exit: scope_stack becomes [1, 2], current_scope restored to 5
            self.assertEqual(symbol_table["current_scope"], 5)
            self.assertEqual(symbol_table["scope_stack"], [1, 2])

    def test_handle_block_traverse_node_exception_handling(self) -> None:
        """依赖异常：_traverse_node 抛出异常时，scope 仍能正确恢复"""
        # Arrange
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl", "name": "x"}],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 3,
            "scope_stack": [],
            "errors": [],
        }

        # Act & Assert
        with patch("._handle_block_src._traverse_node") as mock_traverse:
            mock_traverse.side_effect = RuntimeError("Simulated error")

            with self.assertRaises(RuntimeError):
                _handle_block(node, symbol_table)

            # Verify scope is still restored even when exception occurs
            self.assertEqual(symbol_table["current_scope"], 3)
            self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_symbol_table_missing_optional_fields(self) -> None:
        """非法输入：symbol_table 缺少可选字段时的处理"""
        # Arrange
        node: AST = {
            "type": "block",
            "children": [],
        }
        # Minimal symbol_table without optional fields
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
        }

        # Act
        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

            # Assert
            # current_scope should default to 0, then increment to 1, then restore to 0
            self.assertEqual(symbol_table.get("current_scope"), 0)
            # scope_stack should be created and emptied
            self.assertEqual(symbol_table.get("scope_stack"), [])

    def test_handle_block_multiple_children_sequential(self) -> None:
        """Happy Path: 多个子节点按顺序遍历"""
        # Arrange
        node: AST = {
            "type": "block",
            "children": [
                {"type": "stmt", "id": 1},
                {"type": "stmt", "id": 2},
                {"type": "stmt", "id": 3},
            ],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": [],
        }

        # Act
        call_order = []
        with patch("._handle_block_src._traverse_node") as mock_traverse:
            def track_calls(child: AST, sym_table: SymbolTable) -> None:
                call_order.append(child["id"])

            mock_traverse.side_effect = track_calls
            _handle_block(node, symbol_table)

            # Assert
            self.assertEqual(call_order, [1, 2, 3])  # Sequential order
            self.assertEqual(mock_traverse.call_count, 3)


if __name__ == "__main__":
    unittest.main()