# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# === relative imports ===
from ._handle_if_src import _handle_if

# === type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIf(unittest.TestCase):
    """单元测试：_handle_if 函数"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def _create_mock_traverse_node(self) -> MagicMock:
        """创建 _traverse_node 的 mock 对象"""
        mock = MagicMock()
        mock.return_value = None
        return mock

    def test_handle_if_with_all_branches(self) -> None:
        """测试：if 语句包含条件、then 分支和 else 分支"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "binary_op", "value": "==", "line": 1, "column": 5},
                {"type": "block", "line": 1, "column": 10},
                {"type": "block", "line": 1, "column": 20}
            ],
            "line": 1,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 3)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_if_without_else(self) -> None:
        """测试：if 语句只有条件和 then 分支（无 else）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "binary_op", "value": ">", "line": 2, "column": 5},
                {"type": "block", "line": 2, "column": 10}
            ],
            "line": 2,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_if_no_children(self) -> None:
        """测试：if 语句没有子节点（应记录错误）"""
        node: AST = {
            "type": "if",
            "children": [],
            "line": 3,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 0)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("if 语句缺少子节点", self.symbol_table["errors"][0])
        self.assertIn("line 3", self.symbol_table["errors"][0])

    def test_handle_if_insufficient_children(self) -> None:
        """测试：if 语句只有 1 个子节点（应记录错误）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "binary_op", "value": "<", "line": 4, "column": 5}
            ],
            "line": 4,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 0)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("if 语句子节点不足", self.symbol_table["errors"][0])
        self.assertIn("line 4", self.symbol_table["errors"][0])

    def test_handle_if_with_extra_children(self) -> None:
        """测试：if 语句有超过 3 个子节点（只处理前 3 个）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "binary_op", "value": "==", "line": 5, "column": 5},
                {"type": "block", "line": 5, "column": 10},
                {"type": "block", "line": 5, "column": 20},
                {"type": "extra", "line": 5, "column": 30}
            ],
            "line": 5,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 3)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_if_missing_line_column(self) -> None:
        """测试：if 语句缺少 line/column 信息（错误消息应处理）"""
        node: AST = {
            "type": "if",
            "children": []
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 0)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("unknown", self.symbol_table["errors"][0])

    def test_handle_if_missing_children_key(self) -> None:
        """测试：if 语句缺少 children 键（应使用默认空列表）"""
        node: AST = {
            "type": "if",
            "line": 6,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 0)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("if 语句缺少子节点", self.symbol_table["errors"][0])

    def test_handle_if_traverse_node_called_with_correct_args(self) -> None:
        """测试：_traverse_node 被正确的参数调用"""
        condition_node = {"type": "binary_op", "value": "==", "line": 7, "column": 5}
        then_node = {"type": "block", "line": 7, "column": 10}
        else_node = {"type": "block", "line": 7, "column": 20}

        node: AST = {
            "type": "if",
            "children": [condition_node, then_node, else_node],
            "line": 7,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        mock_traverse.assert_any_call(then_node, self.symbol_table)
        mock_traverse.assert_any_call(else_node, self.symbol_table)

    def test_handle_if_errors_appended_not_replaced(self) -> None:
        """测试：错误被追加到 errors 列表而不是替换"""
        self.symbol_table["errors"] = ["existing error"]

        node: AST = {
            "type": "if",
            "children": [],
            "line": 8,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(self.symbol_table["errors"][0], "existing error")
        self.assertIn("if 语句缺少子节点", self.symbol_table["errors"][1])

    def test_handle_if_empty_symbol_table(self) -> None:
        """测试：使用空的 symbol_table（应自动初始化 errors）"""
        empty_symbol_table: SymbolTable = {}

        node: AST = {
            "type": "if",
            "children": [],
            "line": 9,
            "column": 1
        }

        with patch("._handle_if_src._traverse_node") as mock_traverse:
            mock_traverse.return_value = None
            _handle_if(node, empty_symbol_table)

        self.assertEqual(len(empty_symbol_table["errors"]), 1)
        self.assertIn("if 语句缺少子节点", empty_symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()
