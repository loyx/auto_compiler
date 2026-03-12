# -*- coding: utf-8 -*-
"""单元测试文件：_handle_function_declaration"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._handle_function_declaration_src import _handle_function_declaration


class TestHandleFunctionDeclaration(unittest.TestCase):
    """_handle_function_declaration 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试用例前的准备工作"""
        self.symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_happy_path_basic_function(self) -> None:
        """测试基本函数声明：正常路径"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "my_function",
            "params": ["param1", "param2"],
            "return_type": "int",
            "line": 10,
            "column": 5
        }

        _handle_function_declaration(node, self.symbol_table)

        self.assertIn("my_function", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["my_function"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], ["param1", "param2"])
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)

    def test_function_with_body_calls_traverse(self) -> None:
        """测试带函数体的声明：应调用 _traverse_node"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "func_with_body",
            "params": [],
            "return_type": "void",
            "line": 15,
            "column": 0,
            "body": {
                "type": "block",
                "statements": []
            }
        }

        with patch("._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, self.symbol_table)

            mock_traverse.assert_called_once()
            call_args = mock_traverse.call_args
            self.assertEqual(call_args[0][0], node["body"])
            self.assertIs(call_args[0][1], self.symbol_table)

    def test_function_without_body_no_traverse(self) -> None:
        """测试不带函数体的声明：不应调用 _traverse_node"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "func_no_body",
            "params": [],
            "return_type": "void",
            "line": 20,
            "column": 0
        }

        with patch("._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, self.symbol_table)

            mock_traverse.assert_not_called()

    def test_function_with_none_body_no_traverse(self) -> None:
        """测试函数体为 None 的声明：不应调用 _traverse_node"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "func_none_body",
            "params": [],
            "return_type": "void",
            "line": 25,
            "column": 0,
            "body": None
        }

        with patch("._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, self.symbol_table)

            mock_traverse.assert_not_called()

    def test_function_with_empty_params(self) -> None:
        """测试空参数列表的函数声明"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "no_params_func",
            "params": [],
            "return_type": "str",
            "line": 30,
            "column": 10
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_params_func"]
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["return_type"], "str")

    def test_function_with_complex_params(self) -> None:
        """测试复杂参数列表的函数声明"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "complex_func",
            "params": [
                {"name": "x", "type": "int"},
                {"name": "y", "type": "str"},
                {"name": "z", "type": "list"}
            ],
            "return_type": "dict",
            "line": 35,
            "column": 15
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["complex_func"]
        self.assertEqual(len(func_info["params"]), 3)
        self.assertEqual(func_info["params"][0]["name"], "x")
        self.assertEqual(func_info["params"][1]["type"], "str")

    def test_function_with_various_return_types(self) -> None:
        """测试不同返回类型的函数声明"""
        test_cases = [
            ("int_func", "int"),
            ("void_func", "void"),
            ("custom_func", "MyClass"),
            ("generic_func", "List[int]"),
            ("union_func", "int | str")
        ]

        for func_name, return_type in test_cases:
            with self.subTest(func_name=func_name, return_type=return_type):
                node: Dict[str, Any] = {
                    "type": "function_declaration",
                    "name": func_name,
                    "params": [],
                    "return_type": return_type,
                    "line": 40,
                    "column": 0
                }

                _handle_function_declaration(node, self.symbol_table)

                func_info = self.symbol_table["functions"][func_name]
                self.assertEqual(func_info["return_type"], return_type)

    def test_function_preserves_existing_functions(self) -> None:
        """测试注册新函数不影响已存在的函数"""
        self.symbol_table["functions"]["existing_func"] = {
            "return_type": "bool",
            "params": [],
            "line": 1,
            "column": 0
        }

        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "new_func",
            "params": [],
            "return_type": "float",
            "line": 50,
            "column": 0
        }

        _handle_function_declaration(node, self.symbol_table)

        self.assertIn("existing_func", self.symbol_table["functions"])
        self.assertIn("new_func", self.symbol_table["functions"])
        self.assertEqual(
            self.symbol_table["functions"]["existing_func"]["return_type"],
            "bool"
        )

    def test_function_with_position_info(self) -> None:
        """测试函数位置信息（行号、列号）的正确性"""
        test_positions = [
            (1, 0),
            (100, 50),
            (999, 999),
            (0, 0)
        ]

        for line, column in test_positions:
            with self.subTest(line=line, column=column):
                node: Dict[str, Any] = {
                    "type": "function_declaration",
                    "name": f"func_{line}_{column}",
                    "params": [],
                    "return_type": "void",
                    "line": line,
                    "column": column
                }

                _handle_function_declaration(node, self.symbol_table)

                func_info = self.symbol_table["functions"][f"func_{line}_{column}"]
                self.assertEqual(func_info["line"], line)
                self.assertEqual(func_info["column"], column)

    def test_multiple_function_declarations(self) -> None:
        """测试多个函数声明的累积效果"""
        nodes = [
            {
                "type": "function_declaration",
                "name": "func1",
                "params": [],
                "return_type": "int",
                "line": 1,
                "column": 0
            },
            {
                "type": "function_declaration",
                "name": "func2",
                "params": ["x"],
                "return_type": "str",
                "line": 2,
                "column": 5
            },
            {
                "type": "function_declaration",
                "name": "func3",
                "params": ["a", "b"],
                "return_type": "void",
                "line": 3,
                "column": 10
            }
        ]

        for node in nodes:
            _handle_function_declaration(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["functions"]), 3)
        self.assertIn("func1", self.symbol_table["functions"])
        self.assertIn("func2", self.symbol_table["functions"])
        self.assertIn("func3", self.symbol_table["functions"])

    def test_traverse_node_exception_propagation(self) -> None:
        """测试 _traverse_node 抛出异常时的传播行为"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "func_with_body",
            "params": [],
            "return_type": "void",
            "line": 60,
            "column": 0,
            "body": {"type": "block", "statements": []}
        }

        with patch("._handle_function_declaration_src._traverse_node") as mock_traverse:
            mock_traverse.side_effect = RuntimeError("Traversal error")

            with self.assertRaises(RuntimeError) as context:
                _handle_function_declaration(node, self.symbol_table)

            self.assertEqual(str(context.exception), "Traversal error")
            mock_traverse.assert_called_once()

    def test_symbol_table_not_modified_on_traverse_error_before_registration(self) -> None:
        """测试在函数注册后遍历出错，函数信息仍保留在符号表中"""
        node: Dict[str, Any] = {
            "type": "function_declaration",
            "name": "func_error_body",
            "params": [],
            "return_type": "void",
            "line": 70,
            "column": 0,
            "body": {"type": "block", "statements": []}
        }

        with patch("._handle_function_declaration_src._traverse_node") as mock_traverse:
            mock_traverse.side_effect = ValueError("Body traversal failed")

            with self.assertRaises(ValueError):
                _handle_function_declaration(node, self.symbol_table)

            self.assertIn("func_error_body", self.symbol_table["functions"])
            func_info = self.symbol_table["functions"]["func_error_body"]
            self.assertEqual(func_info["return_type"], "void")


if __name__ == "__main__":
    unittest.main()
