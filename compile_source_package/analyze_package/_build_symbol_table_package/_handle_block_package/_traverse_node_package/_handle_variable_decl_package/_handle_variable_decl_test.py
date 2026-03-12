# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_variable_decl 函数的测试
"""

import unittest

from ._handle_variable_decl_src import _handle_variable_decl, AST, SymbolTable


class TestHandleVariableDecl(unittest.TestCase):
    """测试 _handle_variable_decl 函数"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_happy_path_value_field(self) -> None:
        """测试变量名在 value 字段的正常情况"""
        node: AST = {
            "type": "variable_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }

        _handle_variable_decl(node, self.symbol_table)

        self.assertIn("x", self.symbol_table["variables"])
        var_record = self.symbol_table["variables"]["x"]
        self.assertEqual(var_record["data_type"], "int")
        self.assertEqual(var_record["is_declared"], True)
        self.assertEqual(var_record["line"], 10)
        self.assertEqual(var_record["column"], 5)
        self.assertEqual(var_record["scope_level"], 0)

    def test_happy_path_name_field(self) -> None:
        """测试变量名在 name 字段的正常情况"""
        node: AST = {
            "type": "variable_decl",
            "name": "y",
            "data_type": "char",
            "line": 20,
            "column": 15
        }

        _handle_variable_decl(node, self.symbol_table)

        self.assertIn("y", self.symbol_table["variables"])
        var_record = self.symbol_table["variables"]["y"]
        self.assertEqual(var_record["data_type"], "char")
        self.assertEqual(var_record["is_declared"], True)
        self.assertEqual(var_record["line"], 20)
        self.assertEqual(var_record["column"], 15)
        self.assertEqual(var_record["scope_level"], 0)

    def test_value_takes_priority_over_name(self) -> None:
        """测试 value 字段优先于 name 字段"""
        node: AST = {
            "type": "variable_decl",
            "value": "priority_var",
            "name": "ignored_var",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_variable_decl(node, self.symbol_table)

        self.assertIn("priority_var", self.symbol_table["variables"])
        self.assertNotIn("ignored_var", self.symbol_table["variables"])

    def test_default_data_type_int(self) -> None:
        """测试缺失 data_type 时默认为 int"""
        node: AST = {
            "type": "variable_decl",
            "value": "default_type",
            "line": 1,
            "column": 1
        }

        _handle_variable_decl(node, self.symbol_table)

        var_record = self.symbol_table["variables"]["default_type"]
        self.assertEqual(var_record["data_type"], "int")

    def test_default_line_column_zero(self) -> None:
        """测试缺失 line/column 时默认为 0"""
        node: AST = {
            "type": "variable_decl",
            "value": "no_position"
        }

        _handle_variable_decl(node, self.symbol_table)

        var_record = self.symbol_table["variables"]["no_position"]
        self.assertEqual(var_record["line"], 0)
        self.assertEqual(var_record["column"], 0)

    def test_current_scope_extraction(self) -> None:
        """测试从 symbol_table 提取 current_scope"""
        self.symbol_table["current_scope"] = 3
        node: AST = {
            "type": "variable_decl",
            "value": "scoped_var",
            "data_type": "int"
        }

        _handle_variable_decl(node, self.symbol_table)

        var_record = self.symbol_table["variables"]["scoped_var"]
        self.assertEqual(var_record["scope_level"], 3)

    def test_default_scope_level_zero(self) -> None:
        """测试缺失 current_scope 时默认为 0"""
        del self.symbol_table["current_scope"]
        node: AST = {
            "type": "variable_decl",
            "value": "no_scope"
        }

        _handle_variable_decl(node, self.symbol_table)

        var_record = self.symbol_table["variables"]["no_scope"]
        self.assertEqual(var_record["scope_level"], 0)

    def test_var_name_none_skips(self) -> None:
        """测试变量名为 None 时跳过处理"""
        node: AST = {
            "type": "variable_decl",
            "data_type": "int"
        }

        _handle_variable_decl(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["variables"]), 0)

    def test_var_name_empty_string(self) -> None:
        """测试变量名为空字符串时的处理"""
        node: AST = {
            "type": "variable_decl",
            "value": "",
            "data_type": "int"
        }

        _handle_variable_decl(node, self.symbol_table)

        # 空字符串是有效值，应该被注册
        self.assertIn("", self.symbol_table["variables"])

    def test_overwrite_existing_variable(self) -> None:
        """测试已存在变量时覆盖"""
        # 先注册一个变量
        self.symbol_table["variables"]["existing"] = {
            "data_type": "char",
            "is_declared": True,
            "line": 1,
            "column": 1,
            "scope_level": 0
        }

        node: AST = {
            "type": "variable_decl",
            "value": "existing",
            "data_type": "int",
            "line": 100,
            "column": 50
        }

        _handle_variable_decl(node, self.symbol_table)

        var_record = self.symbol_table["variables"]["existing"]
        self.assertEqual(var_record["data_type"], "int")
        self.assertEqual(var_record["line"], 100)
        self.assertEqual(var_record["column"], 50)

    def test_multiple_variables(self) -> None:
        """测试多个变量声明"""
        nodes: list[AST] = [
            {"type": "variable_decl", "value": "a", "data_type": "int", "line": 1},
            {"type": "variable_decl", "value": "b", "data_type": "char", "line": 2},
            {"type": "variable_decl", "value": "c", "data_type": "int", "line": 3},
        ]

        for node in nodes:
            _handle_variable_decl(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["variables"]), 3)
        self.assertIn("a", self.symbol_table["variables"])
        self.assertIn("b", self.symbol_table["variables"])
        self.assertIn("c", self.symbol_table["variables"])
        self.assertEqual(self.symbol_table["variables"]["a"]["data_type"], "int")
        self.assertEqual(self.symbol_table["variables"]["b"]["data_type"], "char")
        self.assertEqual(self.symbol_table["variables"]["c"]["data_type"], "int")

    def test_empty_symbol_table_variables(self) -> None:
        """测试 symbol_table 中 variables 为空字典的情况"""
        self.symbol_table["variables"] = {}
        node: AST = {
            "type": "variable_decl",
            "value": "first_var",
            "data_type": "int"
        }

        _handle_variable_decl(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["variables"]), 1)
        self.assertIn("first_var", self.symbol_table["variables"])

    def test_is_declared_always_true(self) -> None:
        """测试 is_declared 始终为 True"""
        node: AST = {
            "type": "variable_decl",
            "value": "declared_var",
            "data_type": "int"
        }

        _handle_variable_decl(node, self.symbol_table)

        var_record = self.symbol_table["variables"]["declared_var"]
        self.assertEqual(var_record["is_declared"], True)


if __name__ == "__main__":
    unittest.main()
