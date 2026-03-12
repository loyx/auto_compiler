#!/usr/bin/env python3
"""
单元测试文件：_handle_function_decl 函数测试
"""

import unittest

# 相对导入被测模块
from ._handle_function_decl_src import _handle_function_decl, AST, SymbolTable


class TestHandleFunctionDecl(unittest.TestCase):
    """测试 _handle_function_decl 函数的各种场景"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_happy_path_simple_function(self):
        """测试简单函数声明（无参数）"""
        node: AST = {
            "type": "function_decl",
            "value": "main",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # 验证函数已注册
        self.assertIn("main", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["main"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 1)
        self.assertEqual(func_info["column"], 0)

        # 验证 current_function 已更新
        self.assertEqual(self.symbol_table["current_function"], "main")

        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_happy_path_function_with_params(self):
        """测试带参数的函数声明"""
        node: AST = {
            "type": "function_decl",
            "value": "add",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "a",
                            "data_type": "int"
                        },
                        {
                            "type": "param",
                            "value": "b",
                            "data_type": "int"
                        }
                    ]
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        # 验证函数已注册
        self.assertIn("add", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["add"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "a")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "b")
        self.assertEqual(func_info["params"][1]["data_type"], "int")
        self.assertEqual(func_info["line"], 5)
        self.assertEqual(func_info["column"], 10)

        # 验证 current_function 已更新
        self.assertEqual(self.symbol_table["current_function"], "add")

    def test_happy_path_function_with_char_param(self):
        """测试带 char 类型参数的函数声明"""
        node: AST = {
            "type": "function_decl",
            "value": "print_char",
            "data_type": "void",
            "line": 10,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "c",
                            "data_type": "char"
                        }
                    ]
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["print_char"]
        self.assertEqual(func_info["return_type"], "void")
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "c")
        self.assertEqual(func_info["params"][0]["data_type"], "char")

    def test_edge_case_missing_function_name(self):
        """测试缺少函数名的情况"""
        node: AST = {
            "type": "function_decl",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # 验证没有函数被注册
        self.assertEqual(len(self.symbol_table["functions"]), 0)

        # 验证错误被记录
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "函数声明缺少函数名")
        self.assertEqual(error["line"], 1)
        self.assertEqual(error["column"], 0)

    def test_edge_case_missing_return_type(self):
        """测试缺少返回类型的情况"""
        node: AST = {
            "type": "function_decl",
            "value": "test_func",
            "line": 2,
            "column": 5,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # 验证没有函数被注册
        self.assertEqual(len(self.symbol_table["functions"]), 0)

        # 验证错误被记录
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "函数声明缺少返回类型")
        self.assertEqual(error["line"], 2)
        self.assertEqual(error["column"], 5)

    def test_edge_case_duplicate_function_declaration(self):
        """测试重复函数声明的情况"""
        # 先注册一个函数
        self.symbol_table["functions"]["duplicate_func"] = {
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 0
        }

        # 尝试再次声明同名函数
        node: AST = {
            "type": "function_decl",
            "value": "duplicate_func",
            "data_type": "void",
            "line": 10,
            "column": 0,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # 验证函数信息没有被更新（保持原来的）
        func_info = self.symbol_table["functions"]["duplicate_func"]
        self.assertEqual(func_info["return_type"], "int")  # 仍然是原来的返回类型

        # 验证错误被记录
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "重复函数声明：duplicate_func")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 0)

    def test_edge_case_empty_symbol_table(self):
        """测试符号表为空的情况（没有 functions 键）"""
        empty_symbol_table: SymbolTable = {}

        node: AST = {
            "type": "function_decl",
            "value": "new_func",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_function_decl(node, empty_symbol_table)

        # 验证 functions 被自动创建
        self.assertIn("functions", empty_symbol_table)
        self.assertIn("new_func", empty_symbol_table["functions"])

    def test_edge_case_missing_line_column(self):
        """测试缺少行号和列号的情况"""
        node: AST = {
            "type": "function_decl",
            "value": "no_location",
            "data_type": "int",
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_location"]
        self.assertEqual(func_info["line"], 0)
        self.assertEqual(func_info["column"], 0)

    def test_edge_case_param_list_without_params(self):
        """测试 param_list 为空的情况"""
        node: AST = {
            "type": "function_decl",
            "value": "empty_params",
            "data_type": "void",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": []
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["empty_params"]
        self.assertEqual(func_info["params"], [])

    def test_edge_case_children_without_param_list(self):
        """测试 children 中没有 param_list 的情况"""
        node: AST = {
            "type": "function_decl",
            "value": "no_param_list",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "other_node",
                    "value": "something"
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_param_list"]
        self.assertEqual(func_info["params"], [])

    def test_edge_case_param_without_data_type(self):
        """测试参数缺少 data_type 的情况（应使用默认值 int）"""
        node: AST = {
            "type": "function_decl",
            "value": "func_with_default_type",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "x"
                            # 缺少 data_type
                        }
                    ]
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["func_with_default_type"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "x")
        self.assertEqual(func_info["params"][0]["data_type"], "int")  # 默认值

    def test_edge_case_param_without_value(self):
        """测试参数缺少 value 的情况（应被忽略）"""
        node: AST = {
            "type": "function_decl",
            "value": "func_with_invalid_param",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "data_type": "int"
                            # 缺少 value
                        },
                        {
                            "type": "param",
                            "value": "valid_param",
                            "data_type": "int"
                        }
                    ]
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["func_with_invalid_param"]
        # 只有有效参数被添加
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "valid_param")

    def test_multiple_errors_accumulation(self):
        """测试多个错误累积的情况"""
        # 先添加一个错误
        self.symbol_table["errors"] = [{"message": "previous error", "line": 0, "column": 0}]

        # 声明一个已存在的函数（产生重复声明错误）
        self.symbol_table["functions"]["existing"] = {
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 0
        }

        node: AST = {
            "type": "function_decl",
            "value": "existing",
            "data_type": "void",
            "line": 5,
            "column": 10,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # 验证错误累积
        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(self.symbol_table["errors"][1]["message"], "重复函数声明：existing")


class TestHandleFunctionDeclNoErrorsKey(unittest.TestCase):
    """测试 symbol_table 没有 errors 键的情况"""

    def test_error_recording_without_errors_key(self):
        """测试当 symbol_table 没有 errors 键时，函数能自动创建"""
        symbol_table: SymbolTable = {
            "functions": {}
        }

        node: AST = {
            "type": "function_decl",
            # 缺少 value，会触发错误
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_function_decl(node, symbol_table)

        # 验证 errors 被自动创建
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
