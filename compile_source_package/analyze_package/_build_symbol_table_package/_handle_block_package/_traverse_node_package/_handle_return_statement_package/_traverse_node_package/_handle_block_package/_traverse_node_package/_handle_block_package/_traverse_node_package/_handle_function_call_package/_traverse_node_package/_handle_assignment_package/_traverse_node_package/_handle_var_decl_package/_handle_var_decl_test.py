#!/usr/bin/env python3
"""
单元测试文件：_handle_var_decl 函数测试
测试变量声明处理逻辑，包括新变量注册、重复声明检测、错误记录等
"""

import unittest
from typing import Any, Dict

# 相对导入被测试模块
from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """_handle_var_decl 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_new_variable_declaration(self) -> None:
        """测试新变量声明 - Happy Path"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
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
        self.assertEqual(var_info["scope_level"], 1)
        # 验证没有错误记录
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_declaration(self) -> None:
        """测试重复变量声明 - 应记录错误"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "int",
            "line": 15,
            "column": 8
        }
        symbol_table: Dict[str, Any] = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 1
                }
            },
            "current_scope": 1,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证错误已记录
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["error"], "duplicate declaration")
        self.assertEqual(error["name"], "x")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        # 验证原变量信息未被修改
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)

    def test_variable_not_declared_flag_false(self) -> None:
        """测试变量存在但 is_declared=False - 应允许重新声明"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "y",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: Dict[str, Any] = {
            "variables": {
                "y": {
                    "data_type": "int",
                    "is_declared": False,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "current_scope": 2,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量信息被更新
        var_info = symbol_table["variables"]["y"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 20)
        self.assertEqual(var_info["column"], 3)
        self.assertEqual(var_info["scope_level"], 2)
        # 验证没有错误记录
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_errors_list_initialization(self) -> None:
        """测试 symbol_table 缺少 errors 列表 - 应自动初始化"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "z",
            "data_type": "int",
            "line": 25,
            "column": 10
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        # 验证 errors 列表已创建
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        # 验证变量已注册
        self.assertIn("z", symbol_table["variables"])

    def test_missing_variables_dict_initialization(self) -> None:
        """测试 symbol_table 缺少 variables 字典 - 应自动初始化"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "a",
            "data_type": "char",
            "line": 30,
            "column": 12
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 1,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证 variables 字典已创建
        self.assertIn("variables", symbol_table)
        self.assertIsInstance(symbol_table["variables"], dict)
        # 验证变量已注册
        self.assertIn("a", symbol_table["variables"])

    def test_missing_current_scope_default(self) -> None:
        """测试 symbol_table 缺少 current_scope - 应使用默认值 0"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "b",
            "data_type": "int",
            "line": 35,
            "column": 7
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证 scope_level 为默认值 0
        var_info = symbol_table["variables"]["b"]
        self.assertEqual(var_info["scope_level"], 0)

    def test_multiple_variables_declaration(self) -> None:
        """测试多个变量连续声明"""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": []
        }

        nodes = [
            {"type": "var_decl", "var_name": "x", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "var_name": "y", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "var_name": "z", "data_type": "int", "line": 3, "column": 3}
        ]

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        # 验证所有变量都已注册
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertIn("z", symbol_table["variables"])
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_among_multiple_declarations(self) -> None:
        """测试多个声明中包含重复变量"""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": []
        }

        nodes = [
            {"type": "var_decl", "var_name": "x", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "var_name": "y", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "var_name": "x", "data_type": "int", "line": 3, "column": 3}  # 重复
        ]

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        # 验证有 1 个错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["name"], "x")
        # 验证 x 的信息保持第一次声明的值
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)

    def test_node_missing_var_name(self) -> None:
        """测试 node 缺少 var_name 字段 - 边界情况"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "data_type": "int",
            "line": 40,
            "column": 5
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": []
        }

        # 不应抛出异常
        _handle_var_decl(node, symbol_table)

        # var_name 为 None，应作为键存入
        self.assertIn(None, symbol_table["variables"])

    def test_node_missing_optional_fields(self) -> None:
        """测试 node 缺少可选字段 - 应使用 None"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "test_var"
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量已注册，缺失字段为 None
        var_info = symbol_table["variables"]["test_var"]
        self.assertIsNone(var_info["data_type"])
        self.assertIsNone(var_info["line"])
        self.assertIsNone(var_info["column"])

    def test_different_scope_levels(self) -> None:
        """测试不同作用域层级的变量声明"""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        # 在 scope 0 声明
        node1 = {"type": "var_decl", "var_name": "a", "data_type": "int", "line": 1, "column": 1}
        _handle_var_decl(node1, symbol_table)

        # 切换到 scope 1
        symbol_table["current_scope"] = 1

        # 在 scope 1 声明同名变量（应允许，因为 scope 不同但变量名相同会被视为重复）
        node2 = {"type": "var_decl", "var_name": "a", "data_type": "char", "line": 2, "column": 2}
        _handle_var_decl(node2, symbol_table)

        # 验证记录了重复声明错误（因为变量名相同）
        self.assertEqual(len(symbol_table["errors"]), 1)
        # 验证 a 的信息保持第一次声明的值
        self.assertEqual(symbol_table["variables"]["a"]["scope_level"], 0)

    def test_empty_symbol_table(self) -> None:
        """测试完全空的 symbol_table - 应初始化所有必需字段"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "init_var",
            "data_type": "int",
            "line": 50,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {}

        _handle_var_decl(node, symbol_table)

        # 验证所有必需字段都已初始化
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("init_var", symbol_table["variables"])


if __name__ == "__main__":
    unittest.main()
