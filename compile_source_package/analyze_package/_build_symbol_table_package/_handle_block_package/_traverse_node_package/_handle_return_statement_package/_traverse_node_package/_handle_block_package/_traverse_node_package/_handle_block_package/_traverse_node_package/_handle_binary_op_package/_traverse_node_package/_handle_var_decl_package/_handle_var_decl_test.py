# -*- coding: utf-8 -*-
"""
单元测试：_handle_var_decl 函数
测试变量声明节点处理逻辑
"""

import unittest

# 相对导入被测模块
from ._handle_var_decl_src import _handle_var_decl, AST, SymbolTable


class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数的各种场景"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.base_node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }

    def _create_symbol_table(self, current_scope: int = 0) -> SymbolTable:
        """创建基础符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": [],
            "errors": []
        }

    # ==================== Happy Path ====================

    def test_valid_var_decl_basic(self) -> None:
        """测试基本的有效变量声明"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()

        _handle_var_decl(node, symbol_table)

        # 验证变量被记录
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)

        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_var_decl_char_type(self) -> None:
        """测试 char 类型的变量声明"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()
        node["value"] = "c"
        node["data_type"] = "char"

        _handle_var_decl(node, symbol_table)

        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_var_decl_in_nested_scope(self) -> None:
        """测试在嵌套作用域中的变量声明"""
        symbol_table = self._create_symbol_table(current_scope=2)
        node = self.base_node.copy()

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 2)

    # ==================== Boundary Cases ====================

    def test_var_decl_same_name_different_scope(self) -> None:
        """测试相同变量名在不同作用域（允许）"""
        symbol_table = self._create_symbol_table(current_scope=0)
        
        # 先在 scope 0 声明
        node1 = self.base_node.copy()
        _handle_var_decl(node1, symbol_table)
        
        # 在 scope 1 再次声明相同变量名（允许）
        symbol_table["current_scope"] = 1
        node2 = self.base_node.copy()
        node2["line"] = 20
        _handle_var_decl(node2, symbol_table)

        # 应该没有错误，变量被更新或保留
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_var_decl_missing_line_info(self) -> None:
        """测试缺少行号信息的情况"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int"
            # 缺少 line 和 column
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], -1)
        self.assertEqual(symbol_table["variables"]["x"]["column"], -1)

    def test_var_decl_symbol_table_missing_errors_key(self) -> None:
        """测试符号表缺少 errors 键的情况"""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
            # 缺少 errors 键
        }
        node = self.base_node.copy()
        node["value"] = None  # 触发错误

        _handle_var_decl(node, symbol_table)

        # 应该自动创建 errors 列表
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_var_decl_symbol_table_missing_variables_key(self) -> None:
        """测试符号表缺少 variables 键的情况"""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "errors": []
            # 缺少 variables 键
        }
        node = self.base_node.copy()

        _handle_var_decl(node, symbol_table)

        # 应该自动创建 variables 字典
        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])

    def test_var_decl_symbol_table_missing_current_scope(self) -> None:
        """测试符号表缺少 current_scope 键的情况"""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
            # 缺少 current_scope 键
        }
        node = self.base_node.copy()

        _handle_var_decl(node, symbol_table)

        # 应该默认使用 scope 0
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    # ==================== Error Cases ====================

    def test_var_decl_missing_variable_name(self) -> None:
        """测试缺少变量名的情况"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()
        node["value"] = None

        _handle_var_decl(node, symbol_table)

        # 变量不应被记录
        self.assertNotIn("x", symbol_table["variables"])
        self.assertEqual(len(symbol_table["variables"]), 0)

        # 应该记录错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Missing variable name", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

    def test_var_decl_missing_data_type(self) -> None:
        """测试缺少数据类型的情况"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()
        node["data_type"] = None

        _handle_var_decl(node, symbol_table)

        # 变量不应被记录
        self.assertEqual(len(symbol_table["variables"]), 0)

        # 应该记录错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Missing data type", error["message"])

    def test_var_decl_duplicate_in_same_scope(self) -> None:
        """测试同一作用域内重复声明"""
        symbol_table = self._create_symbol_table(current_scope=0)
        
        # 第一次声明
        node1 = self.base_node.copy()
        _handle_var_decl(node1, symbol_table)
        
        # 第二次声明相同变量
        node2 = self.base_node.copy()
        node2["line"] = 15
        node2["column"] = 10
        _handle_var_decl(node2, symbol_table)

        # 应该记录重复声明错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("Duplicate variable declaration", error["message"])
        self.assertIn("x", error["message"])
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 10)

        # 变量信息应保持第一次声明的值
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)

    def test_var_decl_multiple_errors_accumulated(self) -> None:
        """测试多个错误累积"""
        symbol_table = self._create_symbol_table()
        
        # 第一次：缺少变量名
        node1: AST = {
            "type": "var_decl",
            "value": None,
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        _handle_var_decl(node1, symbol_table)
        
        # 第二次：缺少数据类型
        node2: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": None,
            "line": 2,
            "column": 2
        }
        _handle_var_decl(node2, symbol_table)

        # 应该有 2 个错误
        self.assertEqual(len(symbol_table["errors"]), 2)

    # ==================== Edge Cases ====================

    def test_var_decl_empty_string_name(self) -> None:
        """测试空字符串变量名"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()
        node["value"] = ""

        _handle_var_decl(node, symbol_table)

        # 空字符串也是有效的值，应该被记录
        self.assertIn("", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_var_decl_special_characters_in_name(self) -> None:
        """测试变量名包含特殊字符"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()
        node["value"] = "_var123"

        _handle_var_decl(node, symbol_table)

        self.assertIn("_var123", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_var_decl_does_not_modify_other_symbol_table_fields(self) -> None:
        """测试不修改符号表的其他字段"""
        symbol_table = self._create_symbol_table()
        symbol_table["functions"] = {"main": {"return_type": "int", "params": []}}
        symbol_table["scope_stack"] = [0, 1]
        symbol_table["current_function"] = "main"

        original_functions = symbol_table["functions"].copy()
        original_scope_stack = symbol_table["scope_stack"].copy()

        _handle_var_decl(self.base_node, symbol_table)

        # 验证其他字段未被修改
        self.assertEqual(symbol_table["functions"], original_functions)
        self.assertEqual(symbol_table["scope_stack"], original_scope_stack)
        self.assertEqual(symbol_table["current_function"], "main")

    def test_var_decl_return_type_is_none(self) -> None:
        """测试函数返回类型为 None（无返回值）"""
        symbol_table = self._create_symbol_table()
        node = self.base_node.copy()

        result = _handle_var_decl(node, symbol_table)

        # 函数应该返回 None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
