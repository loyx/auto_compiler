# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import for target function ===
from ._handle_var_decl_src import _handle_var_decl

# === type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """测试_handle_var_decl 函数的各种场景"""

    def test_happy_path_new_variable_int(self):
        """Happy Path: 声明新的 int 类型变量"""
        node: AST = {
            "type": "var_decl",
            "value": "count",
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

        # 验证变量已注册
        self.assertIn("count", symbol_table["variables"])
        var_info = symbol_table["variables"]["count"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_new_variable_char(self):
        """Happy Path: 声明新的 char 类型变量"""
        node: AST = {
            "type": "var_decl",
            "value": "name",
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 1,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量已注册
        self.assertIn("name", symbol_table["variables"])
        var_info = symbol_table["variables"]["name"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 15)
        self.assertEqual(var_info["column"], 8)
        self.assertEqual(var_info["scope_level"], 1)

    def test_duplicate_declaration_error(self):
        """边界值: 重复声明已存在的变量应记录错误"""
        # 先声明一个变量
        symbol_table: SymbolTable = {
            "variables": {
                "count": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 3,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }

        # 尝试重复声明
        node: AST = {
            "type": "var_decl",
            "value": "count",
            "data_type": "int",
            "line": 20,
            "column": 10
        }

        _handle_var_decl(node, symbol_table)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_declaration")
        self.assertIn("count", error["message"])
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 10)
        # 验证原有变量信息未被修改
        self.assertEqual(symbol_table["variables"]["count"]["line"], 5)

    def test_auto_initialize_missing_fields(self):
        """边界值: symbol_table 缺少 variables 和 errors 字段时自动初始化"""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        # 验证字段被自动创建
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_variables_same_scope(self):
        """多分支逻辑: 同一作用域声明多个变量"""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 2,
            "errors": []
        }

        nodes: list = [
            {"type": "var_decl", "value": "a", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "value": "b", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "value": "c", "data_type": "int", "line": 3, "column": 3}
        ]

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        # 验证所有变量都已注册
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        # 验证所有变量作用域层级相同
        for var_name in ["a", "b", "c"]:
            self.assertEqual(symbol_table["variables"][var_name]["scope_level"], 2)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_then_new_variable(self):
        """状态变化: 先重复声明（产生错误），再声明新变量"""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }

        # 重复声明 x
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        _handle_var_decl(node1, symbol_table)

        # 声明新变量 y
        node2: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 11,
            "column": 6
        }
        _handle_var_decl(node2, symbol_table)

        # 验证有一个错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        # 验证 y 已注册
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")
        # 验证 x 保持原有信息
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)

    def test_missing_current_scope_defaults_to_zero(self):
        """边界值: symbol_table 缺少 current_scope 时默认为 0"""
        node: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        # 验证 scope_level 为 0
        self.assertEqual(symbol_table["variables"]["z"]["scope_level"], 0)

    def test_error_does_not_block_new_variable_registration(self):
        """副作用验证: 记录错误后仍可注册新变量"""
        symbol_table: SymbolTable = {
            "variables": {
                "dup": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }

        # 先产生一个重复声明错误
        _handle_var_decl(
            {"type": "var_decl", "value": "dup", "data_type": "int", "line": 10, "column": 1},
            symbol_table
        )

        # 再声明新变量
        _handle_var_decl(
            {"type": "var_decl", "value": "new_var", "data_type": "char", "line": 11, "column": 2},
            symbol_table
        )

        # 验证新变量已注册
        self.assertIn("new_var", symbol_table["variables"])
        self.assertTrue(symbol_table["variables"]["new_var"]["is_declared"])
        # 验证错误仍然存在
        self.assertEqual(len(symbol_table["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
