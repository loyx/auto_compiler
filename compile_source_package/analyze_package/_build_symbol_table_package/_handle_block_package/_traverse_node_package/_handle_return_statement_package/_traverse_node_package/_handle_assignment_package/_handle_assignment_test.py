# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_assignment 函数测试
测试赋值语句处理逻辑，包括变量声明检查和类型匹配验证
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """_handle_assignment 函数测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.base_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "errors": []
        }

    def _create_var(self, name: str, data_type: str, is_declared: bool = True) -> Dict[str, Any]:
        """辅助函数：创建变量信息"""
        return {
            "data_type": data_type,
            "is_declared": is_declared,
            "line": 1,
            "column": 1,
            "scope_level": 0
        }

    # ==================== Happy Path 测试 ====================

    def test_valid_assignment_int_type(self) -> None:
        """测试：有效的 int 类型赋值"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "x": self._create_var("x", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_assignment_char_type(self) -> None:
        """测试：有效的 char 类型赋值"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "c": self._create_var("c", "char")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "c",
            "data_type": "char",
            "line": 3,
            "column": 5,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_assignment_from_identifier_expression(self) -> None:
        """测试：从 identifier 表达式推断类型并成功赋值"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "a": self._create_var("a", "int"),
            "b": self._create_var("b", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "a",
            "line": 7,
            "column": 2,
            "children": [
                {"type": "identifier", "value": "b", "data_type": "int"}
            ]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 变量未声明错误测试 ====================

    def test_error_variable_not_declared(self) -> None:
        """测试：变量未声明时记录错误"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "undeclared_var",
            "data_type": "int",
            "line": 10,
            "column": 15,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("undeclared_var", symbol_table["errors"][0])
        self.assertIn("line 10", symbol_table["errors"][0])
        self.assertIn("column 15", symbol_table["errors"][0])

    def test_error_variable_declared_false(self) -> None:
        """测试：变量存在但 is_declared=False 时记录错误"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "y": self._create_var("y", "int", is_declared=False)
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "y",
            "data_type": "int",
            "line": 12,
            "column": 3,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("not declared", symbol_table["errors"][0])

    # ==================== 类型不匹配错误测试 ====================

    def test_error_type_mismatch_int_to_char(self) -> None:
        """测试：int 类型变量被赋予 char 类型值"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "num": self._create_var("num", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "num",
            "data_type": "char",
            "line": 20,
            "column": 8,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch", symbol_table["errors"][0])
        self.assertIn("'int'", symbol_table["errors"][0])
        self.assertIn("'char'", symbol_table["errors"][0])

    def test_error_type_mismatch_char_to_int(self) -> None:
        """测试：char 类型变量被赋予 int 类型值"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "ch": self._create_var("ch", "char")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "ch",
            "data_type": "int",
            "line": 25,
            "column": 12,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch", symbol_table["errors"][0])

    # ==================== 无法确定变量名错误测试 ====================

    def test_error_cannot_determine_variable_name(self) -> None:
        """测试：无法从节点提取变量名时记录错误"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "line": 30,
            "column": 5,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Cannot determine variable name", symbol_table["errors"][0])
        self.assertIn("line 30", symbol_table["errors"][0])

    def test_extract_variable_name_from_children_identifier(self) -> None:
        """测试：从 children 中的 identifier 节点提取变量名"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "z": self._create_var("z", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "line": 35,
            "column": 7,
            "children": [
                {"type": "identifier", "value": "z"},
                {"type": "literal", "value": 42, "data_type": "int"}
            ]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 边界值测试 ====================

    def test_missing_line_column_info(self) -> None:
        """测试：节点缺少行号列号信息时的处理"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "missing_pos"
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 0", symbol_table["errors"][0])
        self.assertIn("column 0", symbol_table["errors"][0])

    def test_empty_symbol_table(self) -> None:
        """测试：空符号表时的处理"""
        symbol_table: Dict[str, Any] = {}

        node = {
            "type": "assignment",
            "variable": "test_var",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("not declared", symbol_table["errors"][0])

    def test_no_variables_key_in_symbol_table(self) -> None:
        """测试：符号表缺少 variables 键时的处理"""
        symbol_table = {
            "errors": [],
            "current_scope": 0
        }

        node = {
            "type": "assignment",
            "variable": "no_vars",
            "data_type": "int",
            "line": 2,
            "column": 3
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)

    # ==================== 表达式类型推断测试 ====================

    def test_expression_type_from_literal(self) -> None:
        """测试：从 literal 节点推断表达式类型"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "val": self._create_var("val", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "val",
            "line": 40,
            "column": 1,
            "children": [
                {"type": "literal", "value": 100, "data_type": "int"}
            ]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_expression_type_mismatch_from_literal(self) -> None:
        """测试：literal 类型与变量类型不匹配"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "char_var": self._create_var("char_var", "char")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "char_var",
            "line": 45,
            "column": 6,
            "children": [
                {"type": "literal", "value": 99, "data_type": "int"}
            ]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch", symbol_table["errors"][0])

    def test_expression_type_from_unknown_identifier(self) -> None:
        """测试：表达式引用未声明的 identifier 变量"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "target": self._create_var("target", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "target",
            "line": 50,
            "column": 4,
            "children": [
                {"type": "identifier", "value": "unknown_var"}
            ]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 多错误场景测试 ====================

    def test_multiple_assignments_accumulate_errors(self) -> None:
        """测试：多次调用累积错误"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "a": self._create_var("a", "int")
        }
        symbol_table["errors"] = []

        node1 = {
            "type": "assignment",
            "variable": "undeclared1",
            "data_type": "int",
            "line": 60,
            "column": 1
        }

        node2 = {
            "type": "assignment",
            "variable": "a",
            "data_type": "char",
            "line": 61,
            "column": 2
        }

        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)

    # ==================== 特殊场景测试 ====================

    def test_no_data_type_no_error(self) -> None:
        """测试：变量和表达式都无 data_type 时不报错"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "no_type": self._create_var("no_type", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "no_type",
            "line": 70,
            "column": 5,
            "children": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_children_not_dict(self) -> None:
        """测试：children 包含非 dict 元素时的处理"""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {
            "x": self._create_var("x", "int")
        }
        symbol_table["errors"] = []

        node = {
            "type": "assignment",
            "variable": "x",
            "line": 75,
            "column": 8,
            "children": [
                "not_a_dict",
                123,
                None,
                {"type": "literal", "value": 5, "data_type": "int"}
            ]
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
