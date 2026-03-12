# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_assignment 函数的测试
"""

import unittest
from typing import Any, Dict

from ._handle_assignment_src import _handle_assignment, _extract_left_variable

# ADT 类型定义（与被测代码保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """测试 _handle_assignment 函数"""

    def test_variable_exists_mark_as_used(self):
        """测试变量已声明时，标记为已使用"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertTrue(symbol_table["variables"]["x"].get("is_used", False))
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_variable_not_defined_records_error(self):
        """测试变量未声明时，记录错误"""
        node: AST = {
            "type": "assignment",
            "value": "y",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Undefined variable: y")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)

    def test_variable_not_defined_appends_to_existing_errors(self):
        """测试变量未声明时，错误追加到已有错误列表"""
        node: AST = {
            "type": "assignment",
            "value": "z",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [{"type": "error", "message": "Previous error", "line": 1, "column": 1}]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1]["message"], "Undefined variable: z")

    def test_no_variables_key_creates_errors_list(self):
        """测试符号表没有 variables 键时，自动创建 errors 列表"""
        node: AST = {
            "type": "assignment",
            "value": "undefined_var",
            "line": 5,
            "column": 2
        }
        symbol_table: SymbolTable = {}

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: undefined_var")

    def test_node_without_line_column_uses_defaults(self):
        """测试节点没有 line/column 时使用默认值 0"""
        node: AST = {
            "type": "assignment",
            "value": "missing_info"
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_var_name_none_returns_early(self):
        """测试变量名为 None 时，函数提前返回"""
        node: AST = {
            "type": "assignment",
            "value": None,
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_extract_from_value_field_string(self):
        """测试从 value 字段（字符串）提取变量名"""
        node: AST = {
            "type": "assignment",
            "value": "my_var",
            "children": []
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "my_var")

    def test_extract_from_children_zero_dict(self):
        """测试从 children[0]（字典）的 value 字段提取变量名"""
        node: AST = {
            "type": "assignment",
            "value": None,
            "children": [
                {"type": "identifier", "value": "child_var"}
            ]
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "child_var")

    def test_extract_from_children_zero_string(self):
        """测试从 children[0]（字符串）直接提取变量名"""
        node: AST = {
            "type": "assignment",
            "value": None,
            "children": ["string_var"]
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "string_var")

    def test_extract_from_children_zero_dict_no_value(self):
        """测试 children[0] 字典没有 value 字段时返回空字符串"""
        node: AST = {
            "type": "assignment",
            "value": None,
            "children": [
                {"type": "identifier"}
            ]
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "")

    def test_extract_empty_children_returns_empty(self):
        """测试 children 为空时返回空字符串"""
        node: AST = {
            "type": "assignment",
            "value": None,
            "children": []
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "")

    def test_extract_no_children_key_returns_empty(self):
        """测试没有 children 键时返回空字符串"""
        node: AST = {
            "type": "assignment",
            "value": None
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "")

    def test_extract_no_value_no_children_returns_empty(self):
        """测试既没有 value 也没有 children 时返回空字符串"""
        node: AST = {
            "type": "assignment"
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "")

    def test_extract_value_not_string_uses_children(self):
        """测试 value 不是字符串时使用 children 提取"""
        node: AST = {
            "type": "assignment",
            "value": 123,  # 非字符串
            "children": [
                {"type": "identifier", "value": "fallback_var"}
            ]
        }

        var_name = _extract_left_variable(node)

        self.assertEqual(var_name, "fallback_var")


class TestHandleAssignmentIntegration(unittest.TestCase):
    """_handle_assignment 集成测试"""

    def test_multiple_assignments_same_variable(self):
        """测试同一变量多次赋值"""
        symbol_table: SymbolTable = {
            "variables": {
                "counter": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        node1: AST = {"type": "assignment", "value": "counter", "line": 10, "column": 5}
        node2: AST = {"type": "assignment", "value": "counter", "line": 11, "column": 5}

        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)

        self.assertTrue(symbol_table["variables"]["counter"].get("is_used", False))
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_mixed_defined_and_undefined_variables(self):
        """测试混合已定义和未定义变量"""
        symbol_table: SymbolTable = {
            "variables": {
                "defined": {"data_type": "str", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        node1: AST = {"type": "assignment", "value": "defined", "line": 10, "column": 1}
        node2: AST = {"type": "assignment", "value": "undefined", "line": 11, "column": 1}

        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)

        self.assertTrue(symbol_table["variables"]["defined"].get("is_used", False))
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: undefined")


if __name__ == "__main__":
    unittest.main()
