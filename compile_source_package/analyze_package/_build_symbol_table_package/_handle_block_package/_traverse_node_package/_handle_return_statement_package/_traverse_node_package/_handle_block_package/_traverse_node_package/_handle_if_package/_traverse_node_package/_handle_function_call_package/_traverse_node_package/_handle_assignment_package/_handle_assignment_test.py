# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._handle_assignment_src import _handle_assignment

# === Type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """测试 _handle_assignment 函数的语义分析行为。"""

    def setUp(self):
        """为每个测试准备干净的符号表。"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_happy_path_valid_assignment_matching_types(self):
        """测试：有效赋值，变量已声明且类型匹配。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "value": 10, "data_type": "int"},
            "line": 5,
            "column": 10
        }
        self.symbol_table["variables"] = {
            "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)

        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)
        # 验证 traverse_node 被调用
        mock_traverse.assert_called_once_with(
            {"type": "literal", "value": 10, "data_type": "int"},
            self.symbol_table
        )

    def test_missing_target(self):
        """测试：assignment 节点缺少 target 字段。"""
        node = {
            "type": "assignment",
            "value": {"type": "literal", "value": 10},
            "line": 5,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证产生错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Assignment target missing")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)

    def test_target_without_name(self):
        """测试：target 节点缺少 name 字段。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier"},
            "value": {"type": "literal", "value": 10},
            "line": 5,
            "column": 10
        }

        _handle_assignment(node, self.symbol_table)

        # 验证产生错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Assignment target has no name")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)

    def test_assignment_to_undeclared_variable(self):
        """测试：向未声明的变量赋值。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "y"},
            "value": {"type": "literal", "value": 20},
            "line": 7,
            "column": 15
        }
        # 符号表中没有变量 y

        _handle_assignment(node, self.symbol_table)

        # 验证产生错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Assignment to undeclared variable: y")
        self.assertEqual(error["line"], 7)
        self.assertEqual(error["column"], 15)

    def test_type_mismatch_int_to_char(self):
        """测试：类型不匹配，将 int 赋值给 char 变量。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "c"},
            "value": {"type": "literal", "value": 65, "data_type": "int"},
            "line": 10,
            "column": 5
        }
        self.symbol_table["variables"] = {
            "c": {"data_type": "char", "is_declared": True, "line": 2, "column": 1, "scope_level": 0}
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)

        # 验证产生类型不匹配错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Type mismatch", error["message"])
        self.assertIn("int", error["message"])
        self.assertIn("char", error["message"])
        self.assertIn("c", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        # 验证 traverse_node 仍被调用
        mock_traverse.assert_called_once()

    def test_no_value_node(self):
        """测试：assignment 节点没有 value 字段。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "line": 3,
            "column": 8
        }
        self.symbol_table["variables"] = {
            "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
        }

        _handle_assignment(node, self.symbol_table)

        # 验证没有错误（没有 value 就不检查类型）
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_value_node_without_data_type(self):
        """测试：value 节点存在但没有 data_type 字段。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "value": 10},
            "line": 4,
            "column": 12
        }
        self.symbol_table["variables"] = {
            "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)

        # 验证没有类型错误（value 没有 data_type 就不检查）
        self.assertEqual(len(self.symbol_table["errors"]), 0)
        mock_traverse.assert_called_once()

    def test_variable_without_data_type(self):
        """测试：变量声明没有 data_type 字段。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "value": 10, "data_type": "int"},
            "line": 6,
            "column": 20
        }
        self.symbol_table["variables"] = {
            "x": {"is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            # 没有 data_type
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)

        # 验证没有类型错误（变量没有 declared_type 就不检查）
        self.assertEqual(len(self.symbol_table["errors"]), 0)
        mock_traverse.assert_called_once()

    def test_multiple_errors_accumulated(self):
        """测试：符号表中已有错误时，新错误能正确累积。"""
        self.symbol_table["errors"] = [
            {"type": "error", "message": "Previous error", "line": 1, "column": 1}
        ]
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "z"},
            "value": {"type": "literal", "value": 30},
            "line": 8,
            "column": 25
        }
        # 变量 z 未声明

        _handle_assignment(node, self.symbol_table)

        # 验证错误累积
        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(self.symbol_table["errors"][0]["message"], "Previous error")
        self.assertEqual(self.symbol_table["errors"][1]["message"], "Assignment to undeclared variable: z")

    def test_default_line_column_when_missing(self):
        """测试：节点缺少 line/column 时使用默认值 0。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"}
        }
        # 变量 x 未声明

        _handle_assignment(node, self.symbol_table)

        # 验证错误使用默认行号列号
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)


if __name__ == "__main__":
    unittest.main()
