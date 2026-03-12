# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._handle_var_decl_src import _handle_var_decl

# === Type aliases for clarity ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数处理变量声明节点。"""

    def test_happy_path_new_variable_int(self):
        """测试正常路径：声明新的 int 类型变量。"""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["is_declared"], True)
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_new_variable_char(self):
        """测试正常路径：声明新的 char 类型变量。"""
        node: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("c", symbol_table["variables"])
        var_info = symbol_table["variables"]["c"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertEqual(var_info["line"], 15)
        self.assertEqual(var_info["column"], 8)

    def test_duplicate_declaration_same_scope(self):
        """测试重复声明：同一作用域内重复声明变量应记录错误。"""
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 12,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "scope_error")
        self.assertEqual(error["line"], 12)
        self.assertEqual(error["column"], 5)
        self.assertIn("already declared", error["message"])
        self.assertIn("x", error["message"])

    def test_same_name_different_scope_allowed(self):
        """测试不同作用域：相同变量名在不同作用域应允许。"""
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "char",
            "line": 20,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node1, symbol_table)
        symbol_table["current_scope"] = 1
        _handle_var_decl(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["scope_level"], 1)
        self.assertEqual(var_info["data_type"], "char")

    def test_missing_variables_in_symbol_table(self):
        """测试边界：symbol_table 缺少 variables 字段时应自动创建。"""
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": "int",
            "line": 5,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("y", symbol_table["variables"])

    def test_missing_errors_in_symbol_table(self):
        """测试边界：symbol_table 缺少 errors 字段时应自动创建。"""
        node1: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 3
        }
        node2: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 6,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_line_column_defaults_to_zero(self):
        """测试边界：node 缺少 line/column 时应默认为 0。"""
        node: AST = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["a"]
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_missing_current_scope_defaults_to_zero(self):
        """测试边界：symbol_table 缺少 current_scope 时应默认为 0。"""
        node: AST = {
            "type": "var_decl",
            "value": "b",
            "data_type": "char",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["b"]
        self.assertEqual(var_info["scope_level"], 0)

    def test_multiple_variables_same_scope(self):
        """测试多变量：同一作用域声明多个不同变量。"""
        nodes: list = [
            {"type": "var_decl", "value": "a", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "value": "b", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "value": "c", "data_type": "int", "line": 3, "column": 3}
        ]
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_then_new_variable(self):
        """测试混合场景：重复声明后仍可声明新变量。"""
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 11,
            "column": 5
        }
        node3: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 12,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(len(symbol_table["variables"]), 2)


if __name__ == "__main__":
    unittest.main()
