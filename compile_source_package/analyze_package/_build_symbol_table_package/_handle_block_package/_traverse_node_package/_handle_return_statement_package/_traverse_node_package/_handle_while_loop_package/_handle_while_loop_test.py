# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._handle_while_loop_src import _handle_while_loop

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhileLoop(unittest.TestCase):
    """测试 _handle_while_loop 函数。"""

    def setUp(self) -> None:
        """每个测试前的准备工作。"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_condition_and_body(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点同时包含 condition 和 body 的情况。"""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": {"type": "block", "children": []},
            "line": 1,
            "column": 1
        }

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_any_call(node["condition"], self.symbol_table)
        mock_traverse_node.assert_any_call(node["body"], self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_only_condition(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点只包含 condition 的情况。"""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "expression", "value": "x < 10"},
            "line": 1,
            "column": 1
        }

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["condition"], self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_only_body(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点只包含 body 的情况。"""
        node: AST = {
            "type": "while_loop",
            "body": {"type": "block", "children": []},
            "line": 1,
            "column": 1
        }

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["body"], self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_neither_condition_nor_body(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点既不包含 condition 也不包含 body 的情况。"""
        node: AST = {
            "type": "while_loop",
            "line": 1,
            "column": 1
        }

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_none_condition(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点的 condition 显式为 None 的情况。"""
        node: AST = {
            "type": "while_loop",
            "condition": None,
            "body": {"type": "block", "children": []},
            "line": 1,
            "column": 1
        }

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["body"], self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_none_body(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点的 body 显式为 None 的情况。"""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": None,
            "line": 1,
            "column": 1
        }

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["condition"], self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_with_empty_node(self, mock_traverse_node: MagicMock) -> None:
        """测试 while_loop 节点为空字典的情况。"""
        node: AST = {}

        result = _handle_while_loop(node, self.symbol_table)

        self.assertIsNone(result)
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_does_not_modify_symbol_table(self, mock_traverse_node: MagicMock) -> None:
        """测试 _handle_while_loop 不直接修改 symbol_table。"""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": {"type": "block", "children": []},
            "line": 1,
            "column": 1
        }

        original_symbol_table = self.symbol_table.copy()
        original_variables = self.symbol_table["variables"].copy()
        original_functions = self.symbol_table["functions"].copy()

        _handle_while_loop(node, self.symbol_table)

        self.assertEqual(self.symbol_table.keys(), original_symbol_table.keys())
        self.assertEqual(self.symbol_table["variables"], original_variables)
        self.assertEqual(self.symbol_table["functions"], original_functions)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node")
    def test_handle_while_loop_traverse_node_call_order(self, mock_traverse_node: MagicMock) -> None:
        """测试 _traverse_node 调用顺序：先 condition 后 body。"""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": {"type": "block", "children": []},
            "line": 1,
            "column": 1
        }

        _handle_while_loop(node, self.symbol_table)

        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], node["condition"])
        self.assertEqual(calls[1][0][0], node["body"])


if __name__ == "__main__":
    unittest.main()
