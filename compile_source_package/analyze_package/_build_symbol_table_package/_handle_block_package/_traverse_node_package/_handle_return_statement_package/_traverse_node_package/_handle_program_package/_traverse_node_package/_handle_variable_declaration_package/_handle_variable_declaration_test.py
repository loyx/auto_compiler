# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._handle_variable_declaration_src import _handle_variable_declaration

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]

# === Test Class ===
class TestHandleVariableDeclaration(unittest.TestCase):
    """测试 _handle_variable_declaration 函数"""

    def test_new_variable_declaration(self):
        """Happy Path: 新变量声明应成功注册到符号表"""
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["is_declared"], True)
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_with_value_field(self):
        """变量名在 value 字段的情况"""
        node: AST = {
            "type": "variable_declaration",
            "value": "y",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")

    def test_duplicate_declaration_same_scope(self):
        """同一作用域内重复声明应记录错误"""
        node1: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)

        # 应只注册一次
        self.assertIn("x", symbol_table["variables"])
        # 应记录一个错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_declaration")
        self.assertIn("Duplicate declaration of variable 'x'", error["message"])
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)

    def test_duplicate_declaration_different_scope(self):
        """不同作用域内同名变量不应视为重复声明"""
        node1: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        # 第一次声明在 scope 0
        _handle_variable_declaration(node1, symbol_table)

        # 切换到 scope 1
        symbol_table["current_scope"] = 1

        # 第二次声明在 scope 1
        _handle_variable_declaration(node2, symbol_table)

        # 不应有错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 变量应被更新为新作用域的信息
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")

    def test_missing_variable_name(self):
        """变量名缺失时应直接返回，不修改符号表"""
        node: AST = {
            "type": "variable_declaration",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }
        original_variables = symbol_table["variables"].copy()

        _handle_variable_declaration(node, symbol_table)

        # 符号表不应被修改
        self.assertEqual(symbol_table["variables"], original_variables)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_default_data_type(self):
        """未指定数据类型时应默认为 int"""
        node: AST = {
            "type": "variable_declaration",
            "name": "z",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["z"]["data_type"], "int")

    def test_default_line_column(self):
        """未指定行列号时应默认为 0"""
        node: AST = {
            "type": "variable_declaration",
            "name": "w"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["w"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["w"]["column"], 0)

    def test_missing_errors_list(self):
        """符号表缺少 errors 列表时应自动创建"""
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_missing_variables_dict(self):
        """符号表缺少 variables 字典时应能处理"""
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])

    def test_missing_current_scope(self):
        """符号表缺少 current_scope 时应默认为 0"""
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_error_structure(self):
        """重复声明错误的结构应完整"""
        node1: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)

        error = symbol_table["errors"][0]
        self.assertIn("type", error)
        self.assertIn("message", error)
        self.assertIn("line", error)
        self.assertIn("column", error)
        self.assertIn("variable", error)
        self.assertEqual(error["variable"], "x")


# === Main ===
if __name__ == "__main__":
    unittest.main()
