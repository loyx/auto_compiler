# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_loop_statement
被测模块：_handle_loop_statement_src
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Create mock modules to prevent import errors in the dependency chain
# We need to mock the missing _handle_assignment_package
_mock_assignment_pkg = MagicMock()
_mock_assignment_pkg._handle_assignment_src = MagicMock()
_mock_assignment_pkg._handle_assignment_src._handle_assignment = MagicMock()
sys.modules['main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package'] = _mock_assignment_pkg
sys.modules['main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._handle_assignment_src'] = _mock_assignment_pkg._handle_assignment_src

# Now import the function under test
from ._handle_loop_statement_src import _handle_loop_statement


class TestHandleLoopStatement(unittest.TestCase):
    """_handle_loop_statement 函数的单元测试类"""

    def setUp(self) -> None:
        """测试前准备"""
        self.symbol_table: Dict[str, Any] = {
            "variables": {"x": {"type": "int", "scope": 0}},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

    def test_handle_loop_statement_with_condition_and_body(self) -> None:
        """测试：节点同时包含 condition 和 body"""
        node = {
            "type": "loop_statement",
            "loop_type": "while",
            "condition": {"type": "binary_op", "op": "<", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": {"type": "block", "statements": []},
            "line": 1,
            "column": 0
        }

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(node["condition"], self.symbol_table)
            mock_traverse.assert_any_call(node["body"], self.symbol_table)

    def test_handle_loop_statement_with_only_condition(self) -> None:
        """测试：节点仅包含 condition，body 为 None"""
        node = {
            "type": "loop_statement",
            "loop_type": "while",
            "condition": {"type": "binary_op", "op": "<", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": None,
            "line": 1,
            "column": 0
        }

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 1)
            mock_traverse.assert_called_once_with(node["condition"], self.symbol_table)

    def test_handle_loop_statement_with_only_body(self) -> None:
        """测试：节点仅包含 body，condition 为 None"""
        node = {
            "type": "loop_statement",
            "loop_type": "for",
            "condition": None,
            "body": {"type": "block", "statements": []},
            "line": 1,
            "column": 0
        }

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 1)
            mock_traverse.assert_called_once_with(node["body"], self.symbol_table)

    def test_handle_loop_statement_with_neither_condition_nor_body(self) -> None:
        """测试：节点 condition 和 body 均为 None"""
        node = {
            "type": "loop_statement",
            "loop_type": "while",
            "condition": None,
            "body": None,
            "line": 1,
            "column": 0
        }

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 0)

    def test_handle_loop_statement_with_empty_node(self) -> None:
        """测试：空节点（空字典）"""
        node: Dict[str, Any] = {}

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 0)

    def test_handle_loop_statement_symbol_table_not_modified(self) -> None:
        """测试：symbol_table 不被修改"""
        node = {
            "type": "loop_statement",
            "loop_type": "while",
            "condition": {"type": "binary_op", "op": "<", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": {"type": "block", "statements": []},
            "line": 1,
            "column": 0
        }

        original_symbol_table = {
            "variables": {"x": {"type": "int", "scope": 0}},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

        with patch("_handle_loop_statement_src._traverse_node"):
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(self.symbol_table, original_symbol_table)

    def test_handle_loop_statement_for_loop_type(self) -> None:
        """测试：for 类型的循环语句"""
        node = {
            "type": "loop_statement",
            "loop_type": "for",
            "condition": {"type": "binary_op", "op": "in", "left": {"type": "identifier", "name": "i"}, "right": {"type": "identifier", "name": "range"}},
            "body": {"type": "block", "statements": []},
            "line": 5,
            "column": 4
        }

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)

    def test_handle_loop_statement_nested_condition(self) -> None:
        """测试：嵌套的条件表达式"""
        node = {
            "type": "loop_statement",
            "loop_type": "while",
            "condition": {
                "type": "binary_op",
                "op": "and",
                "left": {"type": "binary_op", "op": "<", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 10}},
                "right": {"type": "binary_op", "op": ">", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 0}}
            },
            "body": {"type": "block", "statements": []},
            "line": 1,
            "column": 0
        }

        with patch("_handle_loop_statement_src._traverse_node") as mock_traverse:
            _handle_loop_statement(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(node["condition"], self.symbol_table)
            mock_traverse.assert_any_call(node["body"], self.symbol_table)


if __name__ == "__main__":
    unittest.main()