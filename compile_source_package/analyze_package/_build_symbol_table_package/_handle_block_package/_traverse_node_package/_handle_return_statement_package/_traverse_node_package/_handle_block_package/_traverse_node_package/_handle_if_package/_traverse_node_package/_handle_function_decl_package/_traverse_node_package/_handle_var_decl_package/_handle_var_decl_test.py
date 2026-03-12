# -*- coding: utf-8 -*-
"""单元测试：_handle_var_decl 函数"""

import unittest

from ._handle_var_decl_src import _handle_var_decl, AST, SymbolTable


class TestHandleVarDecl(unittest.TestCase):
    """_handle_var_decl 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_normal_var_decl_with_name_field(self) -> None:
        """测试正常变量声明（使用 name 字段）"""
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_normal_var_decl_with_value_field(self) -> None:
        """测试正常变量声明（使用 value 字段作为 fallback）"""
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("y", symbol_table["variables"])
        var_info = symbol_table["variables"]["y"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 15)
        self.assertEqual(var_info["column"], 3)
        self.assertEqual(var_info["scope_level"], 0)

    def test_default_data_type(self) -> None:
        """测试默认数据类型为 int"""
        node: AST = {
            "type": "var_decl",
            "name": "z",
            "line": 20,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["z"]["data_type"], "int")

    def test_duplicate_declaration_same_scope(self) -> None:
        """测试同一作用域内重复声明应记录错误"""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "char",
            "line": 10,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        # 应记录错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Duplicate declaration", error["message"])
        self.assertIn("x", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

        # 原有变量记录不应被修改
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 5)

    def test_variable_shadowing_different_scope(self) -> None:
        """测试不同作用域允许变量遮蔽"""
        symbol_table: SymbolTable = {
            "current_scope": 1,
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "char",
            "line": 10,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        # 不应有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

        # 变量记录应被更新为新作用域的信息
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 1)

    def test_initialize_missing_variables_field(self) -> None:
        """测试自动初始化缺失的 variables 字段"""
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])

    def test_initialize_missing_errors_field(self) -> None:
        """测试自动初始化缺失的 errors 字段"""
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_initialize_missing_current_scope(self) -> None:
        """测试自动初始化缺失的 current_scope 字段（默认为 0）"""
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("current_scope", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_missing_node_fields_with_defaults(self) -> None:
        """测试节点缺失字段时使用默认值"""
        node: AST = {
            "type": "var_decl",
            "name": "x"
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_empty_symbol_table(self) -> None:
        """测试空符号表的情况"""
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {}

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("current_scope", symbol_table)
        self.assertIn("x", symbol_table["variables"])

    def test_multiple_declarations_different_variables(self) -> None:
        """测试多个不同变量的声明"""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        nodes: list = [
            {"type": "var_decl", "name": "a", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "name": "b", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "name": "c", "data_type": "int", "line": 3, "column": 3},
        ]

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_declarations_with_duplicates(self) -> None:
        """测试多个声明中包含重复变量"""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        nodes: list = [
            {"type": "var_decl", "name": "x", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "name": "x", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "name": "y", "data_type": "int", "line": 3, "column": 3},
            {"type": "var_decl", "name": "x", "data_type": "int", "line": 4, "column": 4},
        ]

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        # 应有两个错误（第 2 和第 4 个声明）
        self.assertEqual(len(symbol_table["errors"]), 2)
        # 变量记录应保持第一次声明的信息
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)
        # y 应该正常添加
        self.assertIn("y", symbol_table["variables"])


if __name__ == "__main__":
    unittest.main()
