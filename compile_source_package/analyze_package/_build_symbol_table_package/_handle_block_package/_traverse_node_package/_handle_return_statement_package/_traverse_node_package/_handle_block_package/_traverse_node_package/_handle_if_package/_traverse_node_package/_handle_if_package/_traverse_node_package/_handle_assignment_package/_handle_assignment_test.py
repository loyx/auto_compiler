# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_assignment 函数测试
测试变量赋值节点处理逻辑，包括变量声明检查和类型匹配验证。
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_assignment_src import _handle_assignment

# 类型别名（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """_handle_assignment 函数测试用例集"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_variable_declared_no_type_mismatch(self) -> None:
        """测试变量已声明且类型匹配，不产生错误"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_variable_not_declared(self) -> None:
        """测试变量未声明，记录 undeclared_variable 错误"""
        node: AST = {
            "type": "assignment",
            "value": "y",
            "data_type": "int",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")
        self.assertEqual(errors[0]["message"], "变量 'y' 未声明")
        self.assertEqual(errors[0]["line"], 15)
        self.assertEqual(errors[0]["column"], 8)

    def test_type_mismatch(self) -> None:
        """测试类型不匹配，记录 type_mismatch 错误"""
        node: AST = {
            "type": "assignment",
            "value": "z",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {
                "z": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 8,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "type_mismatch")
        self.assertEqual(
            errors[0]["message"],
            "类型不匹配：'z' 声明为 int，赋值为 char"
        )
        self.assertEqual(errors[0]["line"], 20)
        self.assertEqual(errors[0]["column"], 3)

    def test_variable_declared_no_data_type_in_node(self) -> None:
        """测试变量已声明但节点无 data_type，不产生类型错误"""
        node: AST = {
            "type": "assignment",
            "value": "a",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "a": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_empty_symbol_table_variables(self) -> None:
        """测试 symbol_table 中 variables 为空，记录未声明错误"""
        node: AST = {
            "type": "assignment",
            "value": "b",
            "data_type": "int",
            "line": 30,
            "column": 7
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")

    def test_symbol_table_without_errors_list(self) -> None:
        """测试 symbol_table 无 errors 列表，函数应自动创建"""
        node: AST = {
            "type": "assignment",
            "value": "c",
            "data_type": "int",
            "line": 35,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_symbol_table_without_variables_key(self) -> None:
        """测试 symbol_table 无 variables 键，视为空变量表"""
        node: AST = {
            "type": "assignment",
            "value": "d",
            "data_type": "int",
            "line": 40,
            "column": 15
        }
        symbol_table: SymbolTable = {
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")

    def test_node_without_line_column(self) -> None:
        """测试节点无 line/column 字段，使用默认值 0"""
        node: AST = {
            "type": "assignment",
            "value": "e",
            "data_type": "int"
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["line"], 0)
        self.assertEqual(errors[0]["column"], 0)

    def test_multiple_variables_one_undeclared(self) -> None:
        """测试多个变量中一个未声明，仅记录该变量错误"""
        node: AST = {
            "type": "assignment",
            "value": "f",
            "data_type": "int",
            "line": 45,
            "column": 20
        }
        symbol_table: SymbolTable = {
            "variables": {
                "g": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 12,
                    "column": 3,
                    "scope_level": 0
                },
                "h": {
                    "data_type": "char",
                    "is_declared": True,
                    "line": 13,
                    "column": 4,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")
        self.assertEqual(errors[0]["message"], "变量 'f' 未声明")

    def test_existing_errors_preserved(self) -> None:
        """测试已有错误列表被保留，新错误追加"""
        node: AST = {
            "type": "assignment",
            "value": "i",
            "data_type": "int",
            "line": 50,
            "column": 25
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [
                {
                    "type": "previous_error",
                    "message": "之前的错误",
                    "line": 1,
                    "column": 1
                }
            ]
        }

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0]["type"], "previous_error")
        self.assertEqual(errors[1]["type"], "undeclared_variable")

    def test_variable_declared_without_data_type(self) -> None:
        """测试变量已声明但无 data_type 字段，类型检查跳过"""
        node: AST = {
            "type": "assignment",
            "value": "j",
            "data_type": "int",
            "line": 55,
            "column": 30
        }
        symbol_table: SymbolTable = {
            "variables": {
                "j": {
                    "is_declared": True,
                    "line": 15,
                    "column": 5,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)


if __name__ == "__main__":
    unittest.main()
