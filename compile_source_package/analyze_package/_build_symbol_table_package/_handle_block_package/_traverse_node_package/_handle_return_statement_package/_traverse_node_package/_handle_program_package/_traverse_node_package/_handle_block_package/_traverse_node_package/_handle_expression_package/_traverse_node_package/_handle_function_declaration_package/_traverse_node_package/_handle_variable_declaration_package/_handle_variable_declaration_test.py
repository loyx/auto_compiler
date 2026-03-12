# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_variable_declaration
测试目标函数：_handle_variable_declaration
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_variable_declaration_src import (
    _handle_variable_declaration,
    _extract_variable_name,
    _extract_data_type,
)


class TestHandleVariableDeclaration(unittest.TestCase):
    """测试 _handle_variable_declaration 函数"""

    def setUp(self) -> None:
        """每个测试前初始化 symbol_table"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "errors": [],
        }

    def test_happy_path_basic_declaration(self) -> None:
        """测试基本变量声明 - 从 children 中提取变量名"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "identifier", "value": "x"},
            ],
            "data_type": "int",
            "line": 1,
            "column": 5,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertIn("x", self.symbol_table["variables"])
        self.assertEqual(self.symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(self.symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(self.symbol_table["variables"]["x"]["line"], 1)
        self.assertEqual(self.symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(self.symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_happy_path_char_type(self) -> None:
        """测试 char 类型变量声明"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "identifier", "value": "c"},
            ],
            "data_type": "char",
            "line": 2,
            "column": 10,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertIn("c", self.symbol_table["variables"])
        self.assertEqual(self.symbol_table["variables"]["c"]["data_type"], "char")
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_extract_var_name_from_children_identifier(self) -> None:
        """测试从 children 中提取 identifier 类型的变量名"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "int"},
                {"type": "identifier", "value": "myVar"},
            ],
            "data_type": "int",
        }

        var_name = _extract_variable_name(node)

        self.assertEqual(var_name, "myVar")

    def test_extract_var_name_from_node_value(self) -> None:
        """测试从 node['value'] 获取变量名（当 children 中没有 identifier 时）"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "int"},
            ],
            "value": "fallbackVar",
            "data_type": "int",
        }

        var_name = _extract_variable_name(node)

        self.assertEqual(var_name, "fallbackVar")

    def test_extract_var_name_returns_none_when_missing(self) -> None:
        """测试当变量名无法提取时返回 None"""
        node = {
            "type": "variable_declaration",
            "children": [],
            "data_type": "int",
        }

        var_name = _extract_variable_name(node)

        self.assertIsNone(var_name)

    def test_error_missing_variable_name(self) -> None:
        """测试变量名缺失时添加错误"""
        node = {
            "type": "variable_declaration",
            "children": [],
            "data_type": "int",
            "line": 5,
            "column": 20,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["variables"]), 0)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["type"], "error")
        self.assertIn("无法提取变量名", self.symbol_table["errors"][0]["message"])
        self.assertEqual(self.symbol_table["errors"][0]["line"], 5)
        self.assertEqual(self.symbol_table["errors"][0]["column"], 20)

    def test_error_duplicate_declaration_same_scope(self) -> None:
        """测试同一作用域内重复声明变量时添加错误"""
        node1 = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "dupVar"}],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        node2 = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "dupVar"}],
            "data_type": "int",
            "line": 2,
            "column": 1,
        }

        _handle_variable_declaration(node1, self.symbol_table)
        _handle_variable_declaration(node2, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("重复声明", self.symbol_table["errors"][0]["message"])
        self.assertIn("dupVar", self.symbol_table["errors"][0]["message"])
        self.assertEqual(self.symbol_table["errors"][0]["line"], 2)

    def test_same_var_different_scope_allowed(self) -> None:
        """测试不同作用域内允许同名变量"""
        node1 = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "scopeVar"}],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        node2 = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "scopeVar"}],
            "data_type": "char",
            "line": 2,
            "column": 1,
        }

        _handle_variable_declaration(node1, self.symbol_table)
        self.symbol_table["current_scope"] = 1
        self.symbol_table["scope_stack"].append(1)
        _handle_variable_declaration(node2, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 0)
        self.assertIn("scopeVar", self.symbol_table["variables"])
        self.assertEqual(self.symbol_table["variables"]["scopeVar"]["data_type"], "char")
        self.assertEqual(self.symbol_table["variables"]["scopeVar"]["scope_level"], 1)

    def test_extract_data_type_from_node_data_type(self) -> None:
        """测试从 node['data_type'] 提取数据类型"""
        node = {
            "type": "variable_declaration",
            "data_type": "char",
            "children": [],
        }

        data_type = _extract_data_type(node)

        self.assertEqual(data_type, "char")

    def test_extract_data_type_from_children_type(self) -> None:
        """测试从 children 中提取类型节点"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "char"},
                {"type": "identifier", "value": "x"},
            ],
        }

        data_type = _extract_data_type(node)

        self.assertEqual(data_type, "char")

    def test_extract_data_type_from_children_data_type(self) -> None:
        """测试从 children 节点的 data_type 字段提取"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "type_specifier", "data_type": "char"},
                {"type": "identifier", "value": "x"},
            ],
        }

        data_type = _extract_data_type(node)

        self.assertEqual(data_type, "char")

    def test_extract_data_type_default_to_int(self) -> None:
        """测试数据类型默认为 int"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "identifier", "value": "x"},
            ],
        }

        data_type = _extract_data_type(node)

        self.assertEqual(data_type, "int")

    def test_extract_data_type_no_data_type_field(self) -> None:
        """测试 node 没有 data_type 字段且 children 中没有类型信息"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "identifier", "value": "x"},
            ],
        }

        data_type = _extract_data_type(node)

        self.assertEqual(data_type, "int")

    def test_variable_declaration_without_line_column(self) -> None:
        """测试节点没有 line/column 字段的情况"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "x"}],
            "data_type": "int",
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertIn("x", self.symbol_table["variables"])
        self.assertIsNone(self.symbol_table["variables"]["x"]["line"])
        self.assertIsNone(self.symbol_table["variables"]["x"]["column"])

    def test_multiple_variables_sequential_declaration(self) -> None:
        """测试连续声明多个不同变量"""
        nodes = [
            {
                "type": "variable_declaration",
                "children": [{"type": "identifier", "value": "a"}],
                "data_type": "int",
                "line": 1,
                "column": 1,
            },
            {
                "type": "variable_declaration",
                "children": [{"type": "identifier", "value": "b"}],
                "data_type": "char",
                "line": 2,
                "column": 1,
            },
            {
                "type": "variable_declaration",
                "children": [{"type": "identifier", "value": "c"}],
                "data_type": "int",
                "line": 3,
                "column": 1,
            },
        ]

        for node in nodes:
            _handle_variable_declaration(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["variables"]), 3)
        self.assertIn("a", self.symbol_table["variables"])
        self.assertIn("b", self.symbol_table["variables"])
        self.assertIn("c", self.symbol_table["variables"])
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_empty_children_list(self) -> None:
        """测试 children 为空列表的情况"""
        node = {
            "type": "variable_declaration",
            "children": [],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(len(self.symbol_table["variables"]), 0)

    def test_children_with_non_dict_items(self) -> None:
        """测试 children 包含非 dict 类型项"""
        node = {
            "type": "variable_declaration",
            "children": [
                "string_item",
                123,
                None,
                {"type": "identifier", "value": "validVar"},
            ],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertIn("validVar", self.symbol_table["variables"])
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_symbol_table_without_current_scope(self) -> None:
        """测试 symbol_table 没有 current_scope 字段时使用默认值 0"""
        symbol_table_minimal = {
            "variables": {},
            "functions": {},
            "errors": [],
        }

        node = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "x"}],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        _handle_variable_declaration(node, symbol_table_minimal)

        self.assertIn("x", symbol_table_minimal["variables"])
        self.assertEqual(symbol_table_minimal["variables"]["x"]["scope_level"], 0)

    def test_identifier_with_empty_value(self) -> None:
        """测试 identifier 节点 value 为空字符串"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": ""}],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertIn("", self.symbol_table["variables"])
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_identifier_value_is_number(self) -> None:
        """测试 identifier 节点 value 是数字类型"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": 123}],
            "data_type": "int",
            "line": 1,
            "column": 1,
        }

        _handle_variable_declaration(node, self.symbol_table)

        self.assertIn("123", self.symbol_table["variables"])
        self.assertEqual(len(self.symbol_table["errors"]), 0)


class TestExtractVariableName(unittest.TestCase):
    """专门测试 _extract_variable_name 辅助函数"""

    def test_first_identifier_in_children(self) -> None:
        """测试返回 children 中第一个 identifier"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "identifier", "value": "first"},
                {"type": "identifier", "value": "second"},
            ],
        }

        result = _extract_variable_name(node)

        self.assertEqual(result, "first")

    def test_skip_non_identifier_nodes(self) -> None:
        """测试跳过非 identifier 类型的节点"""
        node = {
            "type": "variable_declaration",
            "children": [
                {"type": "int"},
                {"type": "keyword", "value": "var"},
                {"type": "identifier", "value": "target"},
            ],
        }

        result = _extract_variable_name(node)

        self.assertEqual(result, "target")

    def test_no_children_key(self) -> None:
        """测试 node 没有 children 键"""
        node = {
            "type": "variable_declaration",
            "data_type": "int",
        }

        result = _extract_variable_name(node)

        self.assertIsNone(result)

    def test_value_takes_precedence_over_none(self) -> None:
        """测试当 children 中没有 identifier 时，使用 value"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "int"}],
            "value": "fromValue",
        }

        result = _extract_variable_name(node)

        self.assertEqual(result, "fromValue")


class TestExtractDataType(unittest.TestCase):
    """专门测试 _extract_data_type 辅助函数"""

    def test_data_type_field_takes_precedence(self) -> None:
        """测试 node['data_type'] 优先于 children 中的类型"""
        node = {
            "type": "variable_declaration",
            "data_type": "char",
            "children": [
                {"type": "int"},
            ],
        }

        result = _extract_data_type(node)

        self.assertEqual(result, "char")

    def test_children_type_int(self) -> None:
        """测试从 children 中提取 int 类型"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "int"}],
        }

        result = _extract_data_type(node)

        self.assertEqual(result, "int")

    def test_children_type_char(self) -> None:
        """测试从 children 中提取 char 类型"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "char"}],
        }

        result = _extract_data_type(node)

        self.assertEqual(result, "char")

    def test_children_data_type_field(self) -> None:
        """测试从 children 的 data_type 字段提取"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "specifier", "data_type": "char"}],
        }

        result = _extract_data_type(node)

        self.assertEqual(result, "char")

    def test_no_type_info_defaults_to_int(self) -> None:
        """测试没有任何类型信息时默认为 int"""
        node = {
            "type": "variable_declaration",
            "children": [{"type": "identifier", "value": "x"}],
        }

        result = _extract_data_type(node)

        self.assertEqual(result, "int")

    def test_empty_node(self) -> None:
        """测试空节点"""
        node: Dict[str, Any] = {}

        result = _extract_data_type(node)

        self.assertEqual(result, "int")


if __name__ == "__main__":
    unittest.main()
