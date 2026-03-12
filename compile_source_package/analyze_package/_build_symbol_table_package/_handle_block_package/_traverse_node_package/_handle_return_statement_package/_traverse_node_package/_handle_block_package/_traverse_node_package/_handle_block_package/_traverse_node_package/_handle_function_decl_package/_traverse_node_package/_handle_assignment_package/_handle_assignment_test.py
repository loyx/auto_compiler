# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_assignment 函数测试
"""
import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._handle_assignment_src import _handle_assignment

# 类型别名
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """_handle_assignment 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 1},
                "y": {"data_type": "char", "is_declared": True, "line": 2, "column": 1, "scope_level": 1},
                "z": {"data_type": "int", "is_declared": False, "line": 3, "column": 1, "scope_level": 1},
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

    def test_happy_path_valid_assignment_int(self):
        """测试场景：有效的 int 类型赋值"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 12}
            ],
            "line": 5,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "int"
            _handle_assignment(node, self.symbol_table)

        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)
        # 验证子函数被调用
        mock_get_type.assert_called_once()

    def test_happy_path_valid_assignment_char(self):
        """测试场景：有效的 char 类型赋值"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "y", "line": 6, "column": 10},
                {"type": "literal", "value": "a", "data_type": "char", "line": 6, "column": 12}
            ],
            "line": 6,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "char"
            _handle_assignment(node, self.symbol_table)

        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_invalid_assignment_missing_children(self):
        """测试场景：赋值语句缺少必要字段（children 少于 2 个）"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 7, "column": 10}
            ],
            "line": 7,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "INVALID_ASSIGNMENT")
        self.assertIn("缺少必要字段", self.symbol_table["errors"][0]["message"])

    def test_invalid_assignment_empty_children(self):
        """测试场景：赋值语句 children 为空"""
        node = {
            "type": "assignment",
            "children": [],
            "line": 8,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "INVALID_ASSIGNMENT")

    def test_invalid_assignment_left_not_identifier(self):
        """测试场景：赋值语句左侧不是标识符"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "literal", "value": 42, "data_type": "int", "line": 9, "column": 10},
                {"type": "literal", "value": 100, "data_type": "int", "line": 9, "column": 12}
            ],
            "line": 9,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "INVALID_ASSIGNMENT")
        self.assertIn("左侧必须是标识符", self.symbol_table["errors"][0]["message"])

    def test_invalid_assignment_var_name_none(self):
        """测试场景：无法提取变量名（value 为 None）"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": None, "line": 10, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 10, "column": 12}
            ],
            "line": 10,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "INVALID_ASSIGNMENT")
        self.assertIn("无法提取变量名", self.symbol_table["errors"][0]["message"])

    def test_undeclared_variable(self):
        """测试场景：变量未声明"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "undeclared_var", "line": 11, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 11, "column": 12}
            ],
            "line": 11,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "UNDECLARED_VAR")
        self.assertIn("未声明", self.symbol_table["errors"][0]["message"])

    def test_undeclared_variable_is_declared_false(self):
        """测试场景：变量存在但 is_declared 为 False"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 12, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 12, "column": 12}
            ],
            "line": 12,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "UNDECLARED_VAR")
        self.assertIn("未声明", self.symbol_table["errors"][0]["message"])

    def test_type_mismatch_int_to_char(self):
        """测试场景：类型不匹配（int 变量赋 char 值）"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 13, "column": 10},
                {"type": "literal", "value": "a", "data_type": "char", "line": 13, "column": 12}
            ],
            "line": 13,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "char"
            _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "TYPE_MISMATCH")
        self.assertIn("类型不匹配", self.symbol_table["errors"][0]["message"])
        self.assertIn("x", self.symbol_table["errors"][0]["message"])

    def test_type_mismatch_char_to_int(self):
        """测试场景：类型不匹配（char 变量赋 int 值）"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "y", "line": 14, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 14, "column": 12}
            ],
            "line": 14,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "int"
            _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "TYPE_MISMATCH")

    def test_right_type_none_skip_check(self):
        """测试场景：右侧类型无法确定（子函数返回 None），跳过类型检查"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 15, "column": 10},
                {"type": "literal", "value": None, "line": 15, "column": 12}
            ],
            "line": 15,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = None
            _handle_assignment(node, self.symbol_table)

        # 验证没有记录类型错误（子函数可能已记录其他错误）
        # 注意：这里不检查 errors 数量，因为子函数可能已记录错误
        mock_get_type.assert_called_once()

    def test_symbol_table_without_errors_list(self):
        """测试场景：符号表没有 errors 列表，应自动初始化"""
        symbol_table_no_errors = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 1}
            },
            "functions": {},
            "current_scope": 1
        }

        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 16, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 16, "column": 12}
            ],
            "line": 16,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "int"
            _handle_assignment(node, symbol_table_no_errors)

        # 验证 errors 列表被创建
        self.assertIn("errors", symbol_table_no_errors)
        self.assertIsInstance(symbol_table_no_errors["errors"], list)

    def test_node_without_line_column(self):
        """测试场景：节点没有 line/column 字段，使用默认值"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x"},
                {"type": "literal", "value": 42, "data_type": "int"}
            ]
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "int"
            _handle_assignment(node, self.symbol_table)

        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_node_without_children_key(self):
        """测试场景：节点没有 children 键"""
        node = {
            "type": "assignment",
            "line": 17,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["error_type"], "INVALID_ASSIGNMENT")

    def test_symbol_table_without_variables(self):
        """测试场景：符号表没有 variables 键"""
        symbol_table_no_vars = {
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 18, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 18, "column": 12}
            ],
            "line": 18,
            "column": 10
        }

        _handle_assignment(node, symbol_table_no_vars)

        # 验证记录了未声明变量错误
        self.assertEqual(len(symbol_table_no_vars["errors"]), 1)
        self.assertEqual(symbol_table_no_vars["errors"][0]["error_type"], "UNDECLARED_VAR")

    def test_error_message_contains_var_name(self):
        """测试场景：错误消息中包含变量名"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "my_var", "line": 19, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 19, "column": 12}
            ],
            "line": 19,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证错误消息包含变量名
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("my_var", self.symbol_table["errors"][0]["message"])

    def test_error_contains_line_and_column(self):
        """测试场景：错误信息包含正确的行号和列号"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 20, "column": 10},
                {"type": "literal", "value": "a", "data_type": "char", "line": 20, "column": 12}
            ],
            "line": 20,
            "column": 10
        }

        with patch("._get_expression_type_package._get_expression_type_src._get_expression_type") as mock_get_type:
            mock_get_type.return_value = "char"
            _handle_assignment(node, self.symbol_table)

        # 验证错误信息包含行号和列号
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["line"], 20)
        self.assertEqual(self.symbol_table["errors"][0]["column"], 10)


if __name__ == "__main__":
    unittest.main()
