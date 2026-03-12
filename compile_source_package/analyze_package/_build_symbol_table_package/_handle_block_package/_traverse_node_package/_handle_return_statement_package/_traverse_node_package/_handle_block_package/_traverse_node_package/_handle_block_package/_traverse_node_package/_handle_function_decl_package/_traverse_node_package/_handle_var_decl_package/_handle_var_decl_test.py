# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of UUT ===
from ._handle_var_decl_src import _handle_var_decl

# === Type aliases (matching UUT) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数的各种场景"""

    def test_happy_path_int_type(self):
        """测试正常声明 int 类型变量"""
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

        # 验证变量已注册
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_char_type(self):
        """测试正常声明 char 类型变量"""
        node: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 20,
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
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_value_field(self):
        """测试缺少 value 字段时的错误处理"""
        node: AST = {
            "type": "var_decl",
            "data_type": "int",
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证没有变量被注册
        self.assertEqual(len(symbol_table["variables"]), 0)
        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "MISSING_FIELD")
        self.assertIn("value", error["message"])
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 3)

    def test_missing_data_type_field(self):
        """测试缺少 data_type 字段时的错误处理"""
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 0)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "MISSING_FIELD")
        self.assertIn("data_type", error["message"])

    def test_invalid_data_type(self):
        """测试无效数据类型时的错误处理"""
        node: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "float",
            "line": 30,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 0)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "INVALID_TYPE")
        self.assertIn("float", error["message"])

    def test_duplicate_declaration_same_scope(self):
        """测试同一作用域内重复声明变量"""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 15,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        # 验证没有更新变量信息（保持原样）
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        # 验证记录了重复声明错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "DUPLICATE_DECL")
        self.assertIn("x", error["message"])

    def test_declaration_different_scope_no_error(self):
        """测试不同作用域声明同名变量（不应报错）"""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 0
                }
            },
            "current_scope": 1,  # 不同作用域
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "char",
            "line": 20,
            "column": 8
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量被更新为新作用域的声明
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 20)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_auto_init_errors_list(self):
        """测试 symbol_table 没有 errors 列表时自动初始化"""
        node: AST = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
            # 没有 errors 字段
        }

        _handle_var_decl(node, symbol_table)

        # 验证 errors 被自动创建
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_auto_init_variables_dict(self):
        """测试 symbol_table 没有 variables 字典时自动初始化"""
        node: AST = {
            "type": "var_decl",
            "value": "b",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "errors": []
            # 没有 variables 字段
        }

        _handle_var_decl(node, symbol_table)

        # 验证 variables 被自动创建
        self.assertIn("variables", symbol_table)
        self.assertIn("b", symbol_table["variables"])

    def test_default_scope_level(self):
        """测试 current_scope 缺失时使用默认值 0"""
        node: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
            # 没有 current_scope 字段
        }

        _handle_var_decl(node, symbol_table)

        # 验证 scope_level 为默认值 0
        self.assertEqual(symbol_table["variables"]["c"]["scope_level"], 0)

    def test_default_line_column(self):
        """测试 line 和 column 缺失时使用默认值 0"""
        node: AST = {
            "type": "var_decl",
            "value": "d",
            "data_type": "int"
            # 没有 line 和 column 字段
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证 line 和 column 为默认值 0
        self.assertEqual(symbol_table["variables"]["d"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["d"]["column"], 0)


if __name__ == "__main__":
    unittest.main()
