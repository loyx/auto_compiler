# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_var_decl 函数测试
测试变量声明节点处理逻辑
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_register_new_variable_success(self) -> None:
        """测试成功注册新变量"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_register_variable_with_char_type(self) -> None:
        """测试注册 char 类型变量"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["c"]["scope_level"], 1)

    def test_duplicate_declaration_records_error(self) -> None:
        """测试重复声明记录错误"""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 20,
            "column": 10
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "duplicate_declaration")
        self.assertEqual(symbol_table["errors"][0]["message"], "Variable 'x' already declared")
        self.assertEqual(symbol_table["errors"][0]["line"], 20)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        self.assertEqual(len(symbol_table["variables"]), 1)

    def test_symbol_table_without_variables_key(self) -> None:
        """测试符号表没有 variables 键时自动创建"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "value": "y",
            "data_type": "int",
            "line": 5,
            "column": 3
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("y", symbol_table["variables"])

    def test_symbol_table_without_errors_key_on_duplicate(self) -> None:
        """测试重复声明时符号表没有 errors 键自动创建"""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 2,
            "column": 2
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_multiple_variables_different_names(self) -> None:
        """测试注册多个不同名称的变量"""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }

        for i, var_name in enumerate(["a", "b", "c"]):
            node: Dict[str, Any] = {
                "type": "var_decl",
                "value": var_name,
                "data_type": "int",
                "line": i + 1,
                "column": i + 1
            }
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])

    def test_duplicate_in_different_scope_still_error(self) -> None:
        """测试不同作用域下同名变量也视为重复声明"""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "value": "x",
            "data_type": "char",
            "line": 20,
            "column": 10
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 2
        }

        _handle_var_decl(node1, symbol_table)
        symbol_table["current_scope"] = 3
        _handle_var_decl(node2, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(len(symbol_table["variables"]), 1)

    def test_empty_symbol_table(self) -> None:
        """测试完全空的符号表"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "value": "var1",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {}

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("var1", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["var1"]["scope_level"], 0)

    def test_multiple_duplicate_declarations(self) -> None:
        """测试多次重复声明记录多个错误"""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "value": "dup",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "value": "dup",
            "data_type": "int",
            "line": 2,
            "column": 2
        }
        node3: Dict[str, Any] = {
            "type": "var_decl",
            "value": "dup",
            "data_type": "int",
            "line": 3,
            "column": 3
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["line"], 2)
        self.assertEqual(symbol_table["errors"][1]["line"], 3)
        self.assertEqual(len(symbol_table["variables"]), 1)


if __name__ == "__main__":
    unittest.main()
