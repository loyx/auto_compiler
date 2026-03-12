# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of target function ===
from ._handle_var_decl_src import _handle_var_decl


# === Type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数的各种场景"""

    def test_happy_path_basic_declaration(self):
        """Happy Path: 基本变量声明成功"""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
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

    def test_happy_path_default_data_type(self):
        """Happy Path: 未指定数据类型时默认为 int"""
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "int")

    def test_happy_path_char_type(self):
        """Happy Path: 字符类型变量声明"""
        node: AST = {
            "type": "var_decl",
            "value": "ch",
            "data_type": "char",
            "line": 20,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 1
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("ch", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["ch"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["ch"]["scope_level"], 1)

    def test_boundary_missing_variable_name(self):
        """边界值: 变量名为 None"""
        node: AST = {
            "type": "var_decl",
            "value": None,
            "data_type": "int",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        # 验证没有变量被注册
        self.assertEqual(len(symbol_table["variables"]), 0)
        # 验证错误被记录
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Variable declaration missing name")
        self.assertEqual(error["line"], 25)
        self.assertEqual(error["column"], 10)

    def test_boundary_duplicate_declaration_same_scope(self):
        """边界值: 同一作用域内重复声明"""
        # 先声明一次
        node1: AST = {
            "type": "var_decl",
            "value": "dup_var",
            "data_type": "int",
            "line": 30,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node1, symbol_table)
        
        # 再次声明同一变量
        node2: AST = {
            "type": "var_decl",
            "value": "dup_var",
            "data_type": "int",
            "line": 35,
            "column": 5
        }
        
        _handle_var_decl(node2, symbol_table)
        
        # 验证只注册了一次
        self.assertEqual(len(symbol_table["variables"]), 1)
        # 验证错误被记录
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Variable 'dup_var' already declared")
        self.assertEqual(error["line"], 35)
        self.assertEqual(error["column"], 5)

    def test_boundary_duplicate_declaration_different_scope(self):
        """边界值: 不同作用域内可以声明同名变量"""
        # 在 scope 0 声明
        node1: AST = {
            "type": "var_decl",
            "value": "scope_var",
            "data_type": "int",
            "line": 40,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node1, symbol_table)
        
        # 切换到 scope 1
        symbol_table["current_scope"] = 1
        
        # 在 scope 1 声明同名变量
        node2: AST = {
            "type": "var_decl",
            "value": "scope_var",
            "data_type": "char",
            "line": 45,
            "column": 5
        }
        
        _handle_var_decl(node2, symbol_table)
        
        # 验证变量被更新（或覆盖）
        self.assertEqual(len(symbol_table["variables"]), 1)
        self.assertEqual(symbol_table["variables"]["scope_var"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["scope_var"]["scope_level"], 1)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_boundary_missing_symbol_table_fields(self):
        """边界值: symbol_table 缺少 variables 和 errors 字段"""
        node: AST = {
            "type": "var_decl",
            "value": "auto_init",
            "data_type": "int",
            "line": 50,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        # 验证字段被自动初始化
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("auto_init", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_boundary_missing_line_column_info(self):
        """边界值: 节点缺少行号列号信息"""
        node: AST = {
            "type": "var_decl",
            "value": "no_location",
            "data_type": "int"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("no_location", symbol_table["variables"])
        var_info = symbol_table["variables"]["no_location"]
        self.assertEqual(var_info["line"], -1)
        self.assertEqual(var_info["column"], -1)

    def test_boundary_missing_current_scope(self):
        """边界值: symbol_table 缺少 current_scope"""
        node: AST = {
            "type": "var_decl",
            "value": "no_scope",
            "data_type": "int",
            "line": 55,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("no_scope", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["no_scope"]["scope_level"], 0)

    def test_illegal_input_empty_node(self):
        """非法输入: 空节点字典"""
        node: AST = {}
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        # 验证没有变量被注册（value 为 None）
        self.assertEqual(len(symbol_table["variables"]), 0)
        # 验证错误被记录
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Variable declaration missing name")

    def test_state_change_multiple_declarations(self):
        """状态变化: 多次声明不同变量"""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        nodes = [
            {"type": "var_decl", "value": "a", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "value": "b", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "value": "c", "data_type": "int", "line": 3, "column": 3},
        ]
        
        for node in nodes:
            _handle_var_decl(node, symbol_table)
        
        # 验证所有变量都被注册
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_side_effect_symbol_table_modified_in_place(self):
        """副作用: symbol_table 被原地修改"""
        node: AST = {
            "type": "var_decl",
            "value": "inplace",
            "data_type": "int",
            "line": 100,
            "column": 100
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 5
        }
        
        original_id = id(symbol_table)
        _handle_var_decl(node, symbol_table)
        
        # 验证是同一个对象
        self.assertEqual(id(symbol_table), original_id)
        # 验证内容被修改
        self.assertIn("inplace", symbol_table["variables"])


class TestHandleVarDeclEdgeCases(unittest.TestCase):
    """额外边界情况测试"""

    def test_empty_string_variable_name(self):
        """边界值: 空字符串变量名（应视为有效）"""
        node: AST = {
            "type": "var_decl",
            "value": "",
            "data_type": "int",
            "line": 60,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        # 空字符串是有效的 value，不应触发 missing name 错误
        self.assertIn("", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_special_characters_in_variable_name(self):
        """边界值: 变量名包含特殊字符"""
        node: AST = {
            "type": "var_decl",
            "value": "_private_var",
            "data_type": "int",
            "line": 65,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("_private_var", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_error_preserves_existing_errors(self):
        """验证: 错误记录不会覆盖已有错误"""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [{"type": "error", "message": "Previous error"}],
            "current_scope": 0
        }
        
        node: AST = {
            "type": "var_decl",
            "value": None,
            "data_type": "int",
            "line": 70,
            "column": 5
        }
        
        _handle_var_decl(node, symbol_table)
        
        # 验证已有错误保留
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "Previous error")
        self.assertEqual(symbol_table["errors"][1]["message"], "Variable declaration missing name")


if __name__ == "__main__":
    unittest.main()
