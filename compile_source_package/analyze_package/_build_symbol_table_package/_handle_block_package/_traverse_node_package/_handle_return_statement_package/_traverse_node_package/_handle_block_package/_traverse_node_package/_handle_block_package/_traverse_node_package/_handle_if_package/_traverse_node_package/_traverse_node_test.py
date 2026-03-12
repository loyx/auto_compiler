import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._traverse_node_src import _traverse_node

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """单元测试：_traverse_node 函数 - AST 遍历核心分发器"""

    def setUp(self):
        """设置测试夹具"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

    def test_node_without_type_returns_early(self):
        """测试：节点没有 type 字段时直接返回，不做任何处理"""
        node = {"value": "something"}
        symbol_table = {}

        _traverse_node(node, symbol_table)

        self.assertEqual(symbol_table, {})

    def test_node_with_none_type_returns_early(self):
        """测试：节点 type 为 None 时直接返回"""
        node = {"type": None}
        symbol_table = {}

        _traverse_node(node, symbol_table)

        self.assertEqual(symbol_table, {})

    def test_node_with_empty_string_type_returns_early(self):
        """测试：节点 type 为空字符串时直接返回"""
        node = {"type": ""}
        symbol_table = {}

        _traverse_node(node, symbol_table)

        self.assertEqual(symbol_table, {})

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._handle_block_src._handle_block")
    def test_block_node_calls_handler(self, mock_handle_block):
        """测试：block 类型节点调用 _handle_block 处理器"""
        node = {"type": "block", "children": []}

        _traverse_node(node, self.symbol_table)

        mock_handle_block.assert_called_once_with(node, self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_var_decl_package._handle_var_decl_src._handle_var_decl")
    def test_var_decl_node_calls_handler(self, mock_handle_var_decl):
        """测试：var_decl 类型节点调用 _handle_var_decl 处理器"""
        node = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_var_decl.assert_called_once_with(node, self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_assignment_package._handle_assignment_src._handle_assignment")
    def test_assignment_node_calls_handler(self, mock_handle_assignment):
        """测试：assignment 类型节点调用 _handle_assignment 处理器"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 5},
            "line": 2,
            "column": 5,
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_assignment.assert_called_once_with(node, self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_if_package._handle_if_src._handle_if")
    def test_if_node_calls_handler(self, mock_handle_if):
        """测试：if 类型节点调用 _handle_if 处理器"""
        node = {
            "type": "if",
            "condition": {"type": "binary_op", "op": ">"},
            "then_block": {"type": "block"},
            "line": 3,
            "column": 1,
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_if.assert_called_once_with(node, self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_while_package._handle_while_src._handle_while")
    def test_while_node_calls_handler(self, mock_handle_while):
        """测试：while 类型节点调用 _handle_while 处理器"""
        node = {
            "type": "while",
            "condition": {"type": "binary_op", "op": "<"},
            "body": {"type": "block"},
            "line": 10,
            "column": 1,
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_while.assert_called_once_with(node, self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_function_call_package._handle_function_call_src._handle_function_call")
    def test_function_call_node_calls_handler(self, mock_handle_function_call):
        """测试：function_call 类型节点调用 _handle_function_call 处理器"""
        node = {
            "type": "function_call",
            "name": "foo",
            "args": [{"type": "literal", "value": 42}],
            "line": 5,
            "column": 10,
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_function_call.assert_called_once_with(node, self.symbol_table)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_return_package._handle_return_src._handle_return")
    def test_return_node_calls_handler(self, mock_handle_return):
        """测试：return 类型节点调用 _handle_return 处理器"""
        node = {
            "type": "return",
            "value": {"type": "literal", "value": 0},
            "line": 20,
            "column": 5,
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_return.assert_called_once_with(node, self.symbol_table)

    def test_unknown_node_type_records_warning(self):
        """测试：未知节点类型记录警告到 symbol_table['errors']"""
        node = {"type": "unknown_type", "line": 10, "column": 5}

        _traverse_node(node, self.symbol_table)

        self.assertIn("errors", self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "warning")
        self.assertIn("Unknown node type: unknown_type", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

    def test_unknown_node_type_without_line_column(self):
        """测试：未知节点类型在没有 line/column 时使用默认值 '?'"""
        node = {"type": "another_unknown"}

        _traverse_node(node, self.symbol_table)

        self.assertIn("errors", self.symbol_table)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], "?")
        self.assertEqual(error["column"], "?")

    def test_unknown_node_type_preserves_existing_errors(self):
        """测试：记录未知类型警告时保留已有错误"""
        self.symbol_table["errors"] = [
            {"type": "error", "message": "Previous error", "line": 1, "column": 1}
        ]
        node = {"type": "unknown_type", "line": 10, "column": 5}

        _traverse_node(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(
            self.symbol_table["errors"][0]["message"], "Previous error"
        )
        self.assertEqual(
            self.symbol_table["errors"][1]["message"],
            "Unknown node type: unknown_type",
        )

    def test_unknown_node_type_initializes_errors_if_not_present(self):
        """测试：如果 symbol_table 没有 errors 字段，会自动初始化"""
        symbol_table = {"variables": {}, "current_scope": 0}
        node = {"type": "unknown_type", "line": 1, "column": 1}

        _traverse_node(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._handle_block_src._handle_block")
    def test_handler_receives_original_node_and_symbol_table(
        self, mock_handle_block
    ):
        """测试：处理器接收到原始的 node 和 symbol_table 引用"""
        node = {"type": "block", "children": [], "custom_field": "test"}
        symbol_table = {"custom_key": "custom_value"}

        _traverse_node(node, symbol_table)

        call_args = mock_handle_block.call_args
        self.assertIs(call_args[0][0], node)
        self.assertIs(call_args[0][1], symbol_table)

    def test_multiple_different_node_types(self):
        """测试：遍历多个不同类型的节点"""
        nodes = [
            {"type": "var_decl", "name": "x"},
            {"type": "assignment", "target": "x", "value": 5},
            {"type": "unknown"},
            {"type": "block", "children": []},
        ]

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_var_decl_package._handle_var_decl_src._handle_var_decl"
        ) as mock_var_decl, patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_assignment_package._handle_assignment_src._handle_assignment"
        ) as mock_assignment, patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._handle_block_src._handle_block"
        ) as mock_block:

            for node in nodes:
                _traverse_node(node, self.symbol_table)

            self.assertEqual(mock_var_decl.call_count, 1)
            self.assertEqual(mock_assignment.call_count, 1)
            self.assertEqual(mock_block.call_count, 1)
            self.assertEqual(len(self.symbol_table.get("errors", [])), 1)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._handle_block_src._handle_block")
    def test_node_with_extra_fields(self, mock_handle_block):
        """测试：节点包含额外字段时正常处理"""
        node = {
            "type": "block",
            "children": [],
            "extra_field": "should_be_passed_to_handler",
            "line": 1,
            "column": 1,
            "metadata": {"key": "value"},
        }

        _traverse_node(node, self.symbol_table)

        mock_handle_block.assert_called_once()
        called_node = mock_handle_block.call_args[0][0]
        self.assertEqual(called_node["extra_field"], "should_be_passed_to_handler")
        self.assertEqual(called_node["metadata"], {"key": "value"})

    def test_all_supported_node_types(self):
        """测试：所有支持的节点类型都能正确分发"""
        supported_types = [
            "block",
            "var_decl",
            "assignment",
            "if",
            "while",
            "function_call",
            "return",
        ]

        for node_type in supported_types:
            with self.subTest(node_type=node_type):
                symbol_table = {"variables": {}, "current_scope": 0}
                node = {"type": node_type}

                _traverse_node(node, symbol_table)

                self.assertNotIn("errors", symbol_table)


if __name__ == "__main__":
    unittest.main()
