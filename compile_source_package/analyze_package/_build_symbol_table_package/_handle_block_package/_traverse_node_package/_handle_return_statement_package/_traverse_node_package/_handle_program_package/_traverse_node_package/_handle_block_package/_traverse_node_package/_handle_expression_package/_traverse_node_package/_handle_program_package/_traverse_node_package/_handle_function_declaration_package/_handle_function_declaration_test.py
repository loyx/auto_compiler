#!/usr/bin/env python3
"""
单元测试文件：_handle_function_declaration 函数测试
"""

import unittest
from typing import Any, Dict

# 相对导入被测试模块
from ._handle_function_declaration_src import _handle_function_declaration


class TestHandleFunctionDeclaration(unittest.TestCase):
    """_handle_function_declaration 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def _create_symbol_table(self) -> Dict[str, Any]:
        """创建初始符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_new_function_no_params(self) -> None:
        """测试：新函数声明，无参数"""
        symbol_table = self._create_symbol_table()
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "myFunction"}
            ],
            "data_type": "int",
            "line": 10,
            "column": 5
        }

        _handle_function_declaration(node, symbol_table)

        # 验证函数已注册
        self.assertIn("myFunction", symbol_table["functions"])
        func_info = symbol_table["functions"]["myFunction"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)

        # 验证 current_function 更新
        self.assertEqual(symbol_table["current_function"], "myFunction")

        # 验证作用域更新
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [1])

        # 验证无错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_new_function_with_params(self) -> None:
        """测试：新函数声明，带参数"""
        symbol_table = self._create_symbol_table()
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "add"},
                {
                    "type": "parameter_list",
                    "children": [
                        {
                            "type": "parameter",
                            "children": [
                                {"type": "identifier", "value": "a"}
                            ],
                            "data_type": "int"
                        },
                        {
                            "type": "parameter",
                            "children": [
                                {"type": "identifier", "value": "b"}
                            ],
                            "data_type": "int"
                        }
                    ]
                }
            ],
            "data_type": "int",
            "line": 20,
            "column": 3
        }

        _handle_function_declaration(node, symbol_table)

        # 验证函数已注册
        self.assertIn("add", symbol_table["functions"])
        func_info = symbol_table["functions"]["add"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "a")
        self.assertEqual(func_info["params"][0]["type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "b")
        self.assertEqual(func_info["params"][1]["type"], "int")

        # 验证作用域更新
        self.assertEqual(symbol_table["current_scope"], 1)

    def test_new_function_default_return_type(self) -> None:
        """测试：新函数声明，无返回类型（默认 void）"""
        symbol_table = self._create_symbol_table()
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "printMessage"}
            ],
            "line": 30,
            "column": 1
        }

        _handle_function_declaration(node, symbol_table)

        # 验证返回类型默认为 void
        func_info = symbol_table["functions"]["printMessage"]
        self.assertEqual(func_info["return_type"], "void")

    def test_function_redefinition(self) -> None:
        """测试：函数重定义错误"""
        symbol_table = self._create_symbol_table()
        
        # 先注册一个函数
        symbol_table["functions"]["duplicateFunc"] = {
            "return_type": "int",
            "params": [],
            "line": 5,
            "column": 1
        }

        # 尝试重定义
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "duplicateFunc"}
            ],
            "data_type": "string",
            "line": 50,
            "column": 10
        }

        _handle_function_declaration(node, symbol_table)

        # 验证原有函数信息未被覆盖
        func_info = symbol_table["functions"]["duplicateFunc"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 5)

        # 验证错误已记录
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "function_redefined")
        self.assertIn("duplicateFunc", error["message"])
        self.assertEqual(error["line"], 50)
        self.assertEqual(error["column"], 10)

        # 验证 current_function 仍被更新
        self.assertEqual(symbol_table["current_function"], "duplicateFunc")

    def test_function_no_line_column(self) -> None:
        """测试：节点无 line/column 信息"""
        symbol_table = self._create_symbol_table()
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "noLocation"}
            ]
        }

        _handle_function_declaration(node, symbol_table)

        # 验证函数已注册
        self.assertIn("noLocation", symbol_table["functions"])
        func_info = symbol_table["functions"]["noLocation"]
        self.assertIsNone(func_info["line"])
        self.assertIsNone(func_info["column"])

    def test_function_empty_parameter_list(self) -> None:
        """测试：函数有空参数列表"""
        symbol_table = self._create_symbol_table()
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "emptyParams"},
                {
                    "type": "parameter_list",
                    "children": []
                }
            ],
            "data_type": "void"
        }

        _handle_function_declaration(node, symbol_table)

        # 验证参数列表为空
        func_info = symbol_table["functions"]["emptyParams"]
        self.assertEqual(func_info["params"], [])

    def test_function_mixed_parameter_types(self) -> None:
        """测试：函数带多种类型的参数"""
        symbol_table = self._create_symbol_table()
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "mixedParams"},
                {
                    "type": "parameter_list",
                    "children": [
                        {
                            "type": "parameter",
                            "children": [
                                {"type": "identifier", "value": "x"}
                            ],
                            "data_type": "int"
                        },
                        {
                            "type": "parameter",
                            "children": [
                                {"type": "identifier", "value": "y"}
                            ],
                            "data_type": "float"
                        },
                        {
                            "type": "parameter",
                            "children": [
                                {"type": "identifier", "value": "name"}
                            ],
                            "data_type": "string"
                        }
                    ]
                }
            ],
            "data_type": "bool"
        }

        _handle_function_declaration(node, symbol_table)

        # 验证所有参数
        func_info = symbol_table["functions"]["mixedParams"]
        self.assertEqual(len(func_info["params"]), 3)
        self.assertEqual(func_info["params"][0]["name"], "x")
        self.assertEqual(func_info["params"][0]["type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "y")
        self.assertEqual(func_info["params"][1]["type"], "float")
        self.assertEqual(func_info["params"][2]["name"], "name")
        self.assertEqual(func_info["params"][2]["type"], "string")
        self.assertEqual(func_info["return_type"], "bool")

    def test_multiple_function_declarations(self) -> None:
        """测试：多个函数声明（作用域累加）"""
        symbol_table = self._create_symbol_table()

        # 第一个函数
        node1 = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "func1"}
            ],
            "line": 1
        }
        _handle_function_declaration(node1, symbol_table)
        self.assertEqual(symbol_table["current_scope"], 1)

        # 第二个函数
        node2 = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "func2"}
            ],
            "line": 10
        }
        _handle_function_declaration(node2, symbol_table)
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [1, 2])
        self.assertEqual(symbol_table["current_function"], "func2")

        # 验证两个函数都已注册
        self.assertIn("func1", symbol_table["functions"])
        self.assertIn("func2", symbol_table["functions"])

    def test_symbol_table_minimal(self) -> None:
        """测试：最小符号表（缺少某些字段）"""
        symbol_table: Dict[str, Any] = {}
        node = {
            "type": "function_declaration",
            "children": [
                {"type": "identifier", "value": "minimalTest"}
            ],
            "line": 100
        }

        _handle_function_declaration(node, symbol_table)

        # 验证 setdefault 正常工作
        self.assertIn("functions", symbol_table)
        self.assertIn("minimalTest", symbol_table["functions"])
        self.assertIn("errors", symbol_table)
        self.assertIn("scope_stack", symbol_table)


if __name__ == "__main__":
    unittest.main()
