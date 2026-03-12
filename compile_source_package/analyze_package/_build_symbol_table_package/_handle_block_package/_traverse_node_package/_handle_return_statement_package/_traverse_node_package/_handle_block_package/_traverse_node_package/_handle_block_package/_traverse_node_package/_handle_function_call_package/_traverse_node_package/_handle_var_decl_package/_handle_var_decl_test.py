# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_var_decl 函数的测试
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_var_decl_src import _handle_var_decl


# === ADT 类型定义（与被测文件保持一致）===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """_handle_var_decl 函数的测试用例类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_handle_var_decl_basic_int(self) -> None:
        """测试基本整型变量声明"""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)

    def test_handle_var_decl_basic_char(self) -> None:
        """测试基本字符型变量声明"""
        node: AST = {
            "type": "var_decl",
            "value": "ch",
            "data_type": "char",
            "line": 20,
            "column": 15
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("ch", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["ch"]["data_type"], "char")
        self.assertTrue(symbol_table["variables"]["ch"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["ch"]["line"], 20)
        self.assertEqual(symbol_table["variables"]["ch"]["column"], 15)
        self.assertEqual(symbol_table["variables"]["ch"]["scope_level"], 0)

    def test_handle_var_decl_boundary_line_column_one(self) -> None:
        """测试边界值：行号和列号为 1"""
        node: AST = {
            "type": "var_decl",
            "value": "first",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["first"]["line"], 1)
        self.assertEqual(symbol_table["variables"]["first"]["column"], 1)

    def test_handle_var_decl_boundary_large_line_column(self) -> None:
        """测试边界值：较大的行号和列号"""
        node: AST = {
            "type": "var_decl",
            "value": "large",
            "data_type": "int",
            "line": 9999,
            "column": 8888
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["large"]["line"], 9999)
        self.assertEqual(symbol_table["variables"]["large"]["column"], 8888)
        self.assertEqual(symbol_table["variables"]["large"]["scope_level"], 5)

    def test_handle_var_decl_overwrite_existing_variable(self) -> None:
        """测试重复声明：已存在的变量被覆盖"""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "char",
            "line": 30,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 1
                }
            },
            "functions": {},
            "current_scope": 2,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量被覆盖
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 30)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 2)

    def test_handle_var_decl_scope_level_captured(self) -> None:
        """测试作用域层级正确捕获"""
        node: AST = {
            "type": "var_decl",
            "value": "var",
            "data_type": "int",
            "line": 5,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 10,
            "scope_stack": [0, 1, 2]
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["var"]["scope_level"], 10)

    def test_handle_var_decl_multiple_variables(self) -> None:
        """测试多个变量声明"""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        node1: AST = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        node2: AST = {
            "type": "var_decl",
            "value": "b",
            "data_type": "char",
            "line": 2,
            "column": 2
        }
        node3: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "int",
            "line": 3,
            "column": 3
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["a"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["b"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "int")

    def test_handle_var_decl_preserves_other_symbol_table_fields(self) -> None:
        """测试不修改符号表的其他字段"""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [0],
            "current_function": "main",
            "errors": []
        }

        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        # 验证其他字段未被修改
        self.assertEqual(len(symbol_table["functions"]), 1)
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_function"], "main")
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_var_decl_empty_variable_name(self) -> None:
        """测试空变量名（边界情况）"""
        node: AST = {
            "type": "var_decl",
            "value": "",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"][""]["data_type"], "int")

    def test_handle_var_decl_special_characters_in_name(self) -> None:
        """测试变量名包含特殊字符"""
        node: AST = {
            "type": "var_decl",
            "value": "_var_123",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("_var_123", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["_var_123"]["data_type"], "int")


if __name__ == "__main__":
    unittest.main()
