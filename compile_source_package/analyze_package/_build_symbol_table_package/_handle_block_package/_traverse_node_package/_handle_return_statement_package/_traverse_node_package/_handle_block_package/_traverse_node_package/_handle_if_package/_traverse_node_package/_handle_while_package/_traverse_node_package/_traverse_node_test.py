# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch, MagicMock

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]

# === target module imports ===
from ._traverse_node_src import _traverse_node


class TestTraverseNode(unittest.TestCase):
    """测试 _traverse_node 函数的节点分发逻辑。"""

    def setUp(self) -> None:
        """每个测试前初始化符号表。"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": [],
        }

    # ==================== 空节点/边界测试 ====================

    def test_traverse_none_node(self) -> None:
        """测试 node 为 None 时直接返回，不报错。"""
        result = _traverse_node(None, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_traverse_empty_dict_node(self) -> None:
        """测试 node 为空字典时直接返回，不报错。"""
        result = _traverse_node({}, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_traverse_node_without_type(self) -> None:
        """测试 node 没有 type 字段时直接返回，不报错。"""
        node: AST = {"value": 42, "line": 1, "column": 0}
        result = _traverse_node(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_traverse_node_with_none_type(self) -> None:
        """测试 node 的 type 字段为 None 时直接返回，不报错。"""
        node: AST = {"type": None, "value": 42}
        result = _traverse_node(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(self.symbol_table["errors"], [])

    # ==================== 已知节点类型分发测试 ====================

    @patch("._traverse_node_src._handle_block")
    def test_traverse_block_node(self, mock_handler: MagicMock) -> None:
        """测试 block 类型节点正确分发到 _handle_block。"""
        node: AST = {"type": "block", "children": [], "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_var_decl")
    def test_traverse_var_decl_node(self, mock_handler: MagicMock) -> None:
        """测试 var_decl 类型节点正确分发到 _handle_var_decl。"""
        node: AST = {"type": "var_decl", "value": "x", "data_type": "int", "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_assignment")
    def test_traverse_assignment_node(self, mock_handler: MagicMock) -> None:
        """测试 assignment 类型节点正确分发到 _handle_assignment。"""
        node: AST = {"type": "assignment", "value": "x = 5", "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_if")
    def test_traverse_if_node(self, mock_handler: MagicMock) -> None:
        """测试 if 类型节点正确分发到 _handle_if。"""
        node: AST = {"type": "if", "children": [], "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_while")
    def test_traverse_while_node(self, mock_handler: MagicMock) -> None:
        """测试 while 类型节点正确分发到 _handle_while。"""
        node: AST = {"type": "while", "children": [], "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_function_call")
    def test_traverse_function_call_node(self, mock_handler: MagicMock) -> None:
        """测试 function_call 类型节点正确分发到 _handle_function_call。"""
        node: AST = {"type": "function_call", "value": "foo()", "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_function_decl")
    def test_traverse_function_decl_node(self, mock_handler: MagicMock) -> None:
        """测试 function_decl 类型节点正确分发到 _handle_function_decl。"""
        node: AST = {"type": "function_decl", "value": "def foo():", "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    @patch("._traverse_node_src._handle_return")
    def test_traverse_return_node(self, mock_handler: MagicMock) -> None:
        """测试 return 类型节点正确分发到 _handle_return。"""
        node: AST = {"type": "return", "value": "return 42", "line": 1, "column": 0}
        _traverse_node(node, self.symbol_table)
        mock_handler.assert_called_once_with(node, self.symbol_table)

    # ==================== 未知节点类型测试 ====================

    def test_traverse_unknown_node_type(self) -> None:
        """测试未知节点类型记录警告到 errors。"""
        node: AST = {"type": "unknown_type", "value": "something", "line": 5, "column": 10}
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
        self.assertIn("unknown node type: unknown_type", error["message"])

    def test_traverse_unknown_node_type_without_line_column(self) -> None:
        """测试未知节点类型没有 line/column 时使用默认值 0。"""
        node: AST = {"type": "another_unknown"}
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)

    # ==================== 符号表 errors 初始化测试 ====================

    def test_traverse_initializes_errors_if_missing(self) -> None:
        """测试当 symbol_table 没有 errors 字段时自动初始化。"""
        symbol_table_no_errors: SymbolTable = {
            "variables": {},
            "functions": {},
        }
        node: AST = {"type": "unknown_type"}
        _traverse_node(node, symbol_table_no_errors)
        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)

    # ==================== 多次调用测试 ====================

    @patch("._traverse_node_src._handle_block")
    def test_traverse_multiple_nodes(self, mock_handler: MagicMock) -> None:
        """测试多次调用正确分发多个节点。"""
        node1: AST = {"type": "block", "line": 1}
        node2: AST = {"type": "block", "line": 2}
        node3: AST = {"type": "block", "line": 3}

        _traverse_node(node1, self.symbol_table)
        _traverse_node(node2, self.symbol_table)
        _traverse_node(node3, self.symbol_table)

        self.assertEqual(mock_handler.call_count, 3)

    # ==================== handler 异常传播测试 ====================

    @patch("._traverse_node_src._handle_block")
    def test_traverse_handler_exception_propagates(self, mock_handler: MagicMock) -> None:
        """测试 handler 抛出的异常会向上 propagation。"""
        mock_handler.side_effect = ValueError("handler error")
        node: AST = {"type": "block"}

        with self.assertRaises(ValueError) as context:
            _traverse_node(node, self.symbol_table)

        self.assertEqual(str(context.exception), "handler error")


if __name__ == "__main__":
    unittest.main()
