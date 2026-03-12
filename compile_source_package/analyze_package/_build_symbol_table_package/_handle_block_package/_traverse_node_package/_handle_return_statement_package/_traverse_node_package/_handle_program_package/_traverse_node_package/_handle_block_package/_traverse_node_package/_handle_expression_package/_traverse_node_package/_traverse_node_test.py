# -*- coding: utf-8 -*-
"""单元测试：_traverse_node 函数"""

import unittest
from unittest.mock import patch, MagicMock, call


# 被测函数及依赖的相对导入
from ._traverse_node_src import _traverse_node, AST, SymbolTable


class TestTraverseNode(unittest.TestCase):
    """_traverse_node 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    # ==================== 防御性初始化测试 ====================

    def test_init_missing_errors_field(self) -> None:
        """测试 symbol_table 缺少 errors 字段时的防御性初始化"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["errors"], [])

    def test_init_missing_variables_field(self) -> None:
        """测试 symbol_table 缺少 variables 字段时的防御性初始化"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertEqual(symbol_table["variables"], {})

    def test_init_missing_functions_field(self) -> None:
        """测试 symbol_table 缺少 functions 字段时的防御性初始化"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertIn("functions", symbol_table)
        self.assertEqual(symbol_table["functions"], {})

    def test_init_missing_current_scope_field(self) -> None:
        """测试 symbol_table 缺少 current_scope 字段时的防御性初始化"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertIn("current_scope", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_init_missing_scope_stack_field(self) -> None:
        """测试 symbol_table 缺少 scope_stack 字段时的防御性初始化"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_init_all_fields_missing(self) -> None:
        """测试 symbol_table 所有必需字段都缺失时的防御性初始化"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIn("variables", symbol_table)
        self.assertIn("functions", symbol_table)
        self.assertIn("current_scope", symbol_table)
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["errors"], [])
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_init_preserves_existing_fields(self) -> None:
        """测试 symbol_table 已有字段不会被覆盖"""
        symbol_table: SymbolTable = {
            "errors": ["existing error"],
            "variables": {"x": {"data_type": "int"}},
            "functions": {"foo": {"return_type": "int"}},
            "current_scope": 2,
            "scope_stack": [0, 1],
        }
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        self.assertEqual(symbol_table["errors"], ["existing error"])
        self.assertEqual(symbol_table["variables"], {"x": {"data_type": "int"}})
        self.assertEqual(symbol_table["functions"], {"foo": {"return_type": "int"}})
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [0, 1])

    # ==================== 已知节点类型分发测试 ====================

    @patch("_traverse_node_src._handle_program")
    def test_dispatch_program_node(self, mock_handle_program: MagicMock) -> None:
        """测试 program 节点类型正确分发到 _handle_program"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "program", "children": []}

        _traverse_node(node, symbol_table)

        mock_handle_program.assert_called_once_with(node, symbol_table)

    @patch("_traverse_node_src._handle_function_declaration")
    def test_dispatch_function_declaration_node(self, mock_handle_func_decl: MagicMock) -> None:
        """测试 function_declaration 节点类型正确分发到 _handle_function_declaration"""
        symbol_table: SymbolTable = {}
        node: AST = {
            "type": "function_declaration",
            "data_type": "int",
            "children": [],
        }

        _traverse_node(node, symbol_table)

        mock_handle_func_decl.assert_called_once_with(node, symbol_table)

    @patch("_traverse_node_src._handle_block")
    def test_dispatch_block_node(self, mock_handle_block: MagicMock) -> None:
        """测试 block 节点类型正确分发到 _handle_block"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "block", "children": []}

        _traverse_node(node, symbol_table)

        mock_handle_block.assert_called_once_with(node, symbol_table)

    @patch("_traverse_node_src._handle_expression")
    def test_dispatch_expression_node(self, mock_handle_expression: MagicMock) -> None:
        """测试 expression 节点类型正确分发到 _handle_expression"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "expression", "children": []}

        _traverse_node(node, symbol_table)

        mock_handle_expression.assert_called_once_with(node, symbol_table)

    @patch("_traverse_node_src._handle_identifier")
    def test_dispatch_identifier_node(self, mock_handle_identifier: MagicMock) -> None:
        """测试 identifier 节点类型正确分发到 _handle_identifier"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "identifier", "value": "x"}

        _traverse_node(node, symbol_table)

        mock_handle_identifier.assert_called_once_with(node, symbol_table)

    @patch("_traverse_node_src._handle_literal")
    def test_dispatch_literal_node(self, mock_handle_literal: MagicMock) -> None:
        """测试 literal 节点类型正确分发到 _handle_literal"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "literal", "value": 42}

        _traverse_node(node, symbol_table)

        mock_handle_literal.assert_called_once_with(node, symbol_table)

    # ==================== 未知节点类型测试 ====================

    @patch("_traverse_node_src._traverse_node")
    def test_unknown_node_type_with_children(self, mock_traverse: MagicMock) -> None:
        """测试未知节点类型时递归遍历子节点"""
        symbol_table: SymbolTable = {}
        node: AST = {
            "type": "unknown_type",
            "children": [
                {"type": "literal", "value": 1},
                {"type": "identifier", "value": "x"},
            ],
        }

        # 排除自身递归调用，只统计对子节点的调用
        mock_traverse.side_effect = lambda n, st: None

        _traverse_node(node, symbol_table)

        # 验证对两个子节点的递归调用
        self.assertEqual(mock_traverse.call_count, 2)
        expected_calls = [
            call({"type": "literal", "value": 1}, symbol_table),
            call({"type": "identifier", "value": "x"}, symbol_table),
        ]
        mock_traverse.assert_has_calls(expected_calls)

    @patch("_traverse_node_src._traverse_node")
    def test_unknown_node_type_without_children(self, mock_traverse: MagicMock) -> None:
        """测试未知节点类型且没有子节点时不执行任何操作"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "unknown_type"}

        _traverse_node(node, symbol_table)

        mock_traverse.assert_not_called()

    @patch("_traverse_node_src._traverse_node")
    def test_unknown_node_type_with_empty_children_list(
        self, mock_traverse: MagicMock
    ) -> None:
        """测试未知节点类型且子节点列表为空时不执行任何操作"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "unknown_type", "children": []}

        _traverse_node(node, symbol_table)

        mock_traverse.assert_not_called()

    # ==================== 边界值测试 ====================

    def test_node_missing_type_field(self) -> None:
        """测试节点缺少 type 字段时的处理（应视为未知类型）"""
        symbol_table: SymbolTable = {}
        node: AST = {"value": 42, "children": []}

        # 不应抛出异常
        _traverse_node(node, symbol_table)

        # 验证 symbol_table 被正确初始化
        self.assertIn("errors", symbol_table)
        self.assertIn("variables", symbol_table)

    def test_node_empty_dict(self) -> None:
        """测试节点为空字典时的处理"""
        symbol_table: SymbolTable = {}
        node: AST = {}

        # 不应抛出异常
        _traverse_node(node, symbol_table)

        # 验证 symbol_table 被正确初始化
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_node_with_type_empty_string(self) -> None:
        """测试节点 type 字段为空字符串时的处理（应视为未知类型）"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "", "children": []}

        # 不应抛出异常
        _traverse_node(node, symbol_table)

    # ==================== 多节点类型混合测试 ====================

    @patch("_traverse_node_src._handle_program")
    @patch("_traverse_node_src._handle_function_declaration")
    @patch("_traverse_node_src._handle_block")
    def test_multiple_node_types_in_sequence(
        self,
        mock_handle_block: MagicMock,
        mock_handle_func_decl: MagicMock,
        mock_handle_program: MagicMock,
    ) -> None:
        """测试连续处理多个不同类型的节点"""
        symbol_table: SymbolTable = {}

        program_node: AST = {"type": "program", "children": []}
        func_node: AST = {"type": "function_declaration", "data_type": "int", "children": []}
        block_node: AST = {"type": "block", "children": []}

        _traverse_node(program_node, symbol_table)
        _traverse_node(func_node, symbol_table)
        _traverse_node(block_node, symbol_table)

        mock_handle_program.assert_called_once_with(program_node, symbol_table)
        mock_handle_func_decl.assert_called_once_with(func_node, symbol_table)
        mock_handle_block.assert_called_once_with(block_node, symbol_table)

    # ==================== symbol_table 副作用测试 ====================

    @patch("_traverse_node_src._handle_program")
    def test_symbol_table_passed_to_handler(self, mock_handle_program: MagicMock) -> None:
        """验证 symbol_table 正确传递给 handler 函数"""
        symbol_table: SymbolTable = {"custom_field": "custom_value"}
        node: AST = {"type": "program", "children": []}

        _traverse_node(node, symbol_table)

        # 验证 handler 接收到的是同一个 symbol_table 对象
        _, passed_symbol_table = mock_handle_program.call_args[0]
        self.assertIs(passed_symbol_table, symbol_table)
        self.assertEqual(passed_symbol_table["custom_field"], "custom_value")

    @patch("_traverse_node_src._handle_identifier")
    def test_handler_can_modify_symbol_table(
        self, mock_handle_identifier: MagicMock
    ) -> None:
        """验证 handler 函数可以修改 symbol_table"""
        symbol_table: SymbolTable = {}
        node: AST = {"type": "identifier", "value": "x"}

        # 模拟 handler 修改 symbol_table
        def side_effect(n: AST, st: SymbolTable) -> None:
            st["errors"].append("test error")
            st["variables"]["x"] = {"data_type": "int"}

        mock_handle_identifier.side_effect = side_effect

        _traverse_node(node, symbol_table)

        self.assertEqual(symbol_table["errors"], ["test error"])
        self.assertIn("x", symbol_table["variables"])


class TestTraverseNodeIntegration(unittest.TestCase):
    """_traverse_node 集成测试（使用真实 handler 函数）"""

    def test_full_traversal_with_nested_structure(self) -> None:
        """测试完整遍历嵌套的 AST 结构"""
        symbol_table: SymbolTable = {}

        # 构建一个包含多种节点类型的嵌套 AST
        ast: AST = {
            "type": "program",
            "children": [
                {
                    "type": "function_declaration",
                    "data_type": "int",
                    "children": [
                        {"type": "identifier", "value": "main"},
                        {
                            "type": "block",
                            "children": [
                                {
                                    "type": "expression",
                                    "children": [
                                        {"type": "identifier", "value": "x"},
                                        {"type": "literal", "value": 10},
                                    ],
                                },
                                {"type": "literal", "value": 0},
                            ],
                        },
                    ],
                }
            ],
        }

        # 不应抛出异常
        _traverse_node(ast, symbol_table)

        # 验证 symbol_table 被正确初始化
        self.assertIn("errors", symbol_table)
        self.assertIn("variables", symbol_table)
        self.assertIn("functions", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])


if __name__ == "__main__":
    unittest.main()
