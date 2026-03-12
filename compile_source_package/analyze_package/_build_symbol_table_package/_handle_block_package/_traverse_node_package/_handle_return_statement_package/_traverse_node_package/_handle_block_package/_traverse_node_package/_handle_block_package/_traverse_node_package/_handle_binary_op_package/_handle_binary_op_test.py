# -*- coding: utf-8 -*-
"""单元测试文件：_handle_binary_op 函数测试"""

import unittest
from unittest.mock import patch, MagicMock, call
from typing import Any, Dict

# 相对导入被测模块
from ._handle_binary_op_src import _handle_binary_op


class TestHandleBinaryOp(unittest.TestCase):
    """_handle_binary_op 函数的单元测试类"""

    def setUp(self) -> None:
        """测试前准备：初始化符号表"""
        self.symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def _create_node(self, op: str, children: list, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建二元操作节点"""
        return {
            "type": "binary_op",
            "value": op,
            "children": children,
            "line": line,
            "column": column
        }

    def _create_operand(self, data_type: str, value: Any = None) -> Dict[str, Any]:
        """辅助函数：创建操作数节点"""
        node = {
            "type": "literal",
            "data_type": data_type,
            "line": 1,
            "column": 1
        }
        if value is not None:
            node["value"] = value
        return node

    # ==================== Happy Path Tests ====================

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_arithmetic_valid(self, mock_traverse: MagicMock) -> None:
        """测试：有效的算术操作（int + int）"""
        left = self._create_operand("int", 5)
        right = self._create_operand("int", 3)
        node = self._create_node("+", [left, right])

        _handle_binary_op(node, self.symbol_table)

        # 验证 _traverse_node 被调用两次
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([call(left, self.symbol_table), call(right, self.symbol_table)])
        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_arithmetic_all_operators(self, mock_traverse: MagicMock) -> None:
        """测试：所有算术操作符（+, -, *, /）"""
        for op in ["+", "-", "*", "/"]:
            self.symbol_table["errors"] = []
            left = self._create_operand("int", 10)
            right = self._create_operand("int", 2)
            node = self._create_node(op, [left, right])

            _handle_binary_op(node, self.symbol_table)

            self.assertEqual(len(self.symbol_table["errors"]), 0, f"Operator {op} should not produce errors")

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_comparison_valid(self, mock_traverse: MagicMock) -> None:
        """测试：有效的比较操作（类型一致）"""
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            self.symbol_table["errors"] = []
            # int 比较
            left = self._create_operand("int", 5)
            right = self._create_operand("int", 3)
            node = self._create_node(op, [left, right])

            _handle_binary_op(node, self.symbol_table)

            self.assertEqual(len(self.symbol_table["errors"]), 0, f"Operator {op} with int should not produce errors")

            # char 比较
            self.symbol_table["errors"] = []
            left = self._create_operand("char", 'a')
            right = self._create_operand("char", 'b')
            node = self._create_node(op, [left, right])

            _handle_binary_op(node, self.symbol_table)

            self.assertEqual(len(self.symbol_table["errors"]), 0, f"Operator {op} with char should not produce errors")

    # ==================== Error Cases: Invalid Operand Count ====================

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_no_operands(self, mock_traverse: MagicMock) -> None:
        """测试：没有操作数（0 个）"""
        node = self._create_node("+", [], line=5, column=10)

        _handle_binary_op(node, self.symbol_table)

        # 验证没有调用 _traverse_node
        mock_traverse.assert_not_called()
        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("requires exactly 2 operands", error["message"])
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_one_operand(self, mock_traverse: MagicMock) -> None:
        """测试：只有一个操作数"""
        left = self._create_operand("int", 5)
        node = self._create_node("+", [left], line=3, column=7)

        _handle_binary_op(node, self.symbol_table)

        mock_traverse.assert_not_called()
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("requires exactly 2 operands", error["message"])
        self.assertEqual(error["line"], 3)
        self.assertEqual(error["column"], 7)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_three_operands(self, mock_traverse: MagicMock) -> None:
        """测试：三个操作数"""
        left = self._create_operand("int", 1)
        mid = self._create_operand("int", 2)
        right = self._create_operand("int", 3)
        node = self._create_node("+", [left, mid, right], line=8, column=15)

        _handle_binary_op(node, self.symbol_table)

        mock_traverse.assert_not_called()
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("requires exactly 2 operands", error["message"])

    # ==================== Error Cases: Invalid Arithmetic Operand Types ====================

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_arithmetic_char_left(self, mock_traverse: MagicMock) -> None:
        """测试：算术操作左操作数为 char"""
        left = self._create_operand("char", 'a')
        right = self._create_operand("int", 5)
        node = self._create_node("+", [left, right], line=10, column=5)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("arithmetic operations require int operands", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_arithmetic_char_right(self, mock_traverse: MagicMock) -> None:
        """测试：算术操作右操作数为 char"""
        left = self._create_operand("int", 5)
        right = self._create_operand("char", 'b')
        node = self._create_node("-", [left, right], line=12, column=8)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("arithmetic operations require int operands", error["message"])

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_arithmetic_both_char(self, mock_traverse: MagicMock) -> None:
        """测试：算术操作两个操作数都是 char"""
        left = self._create_operand("char", 'x')
        right = self._create_operand("char", 'y')
        node = self._create_node("*", [left, right], line=15, column=20)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("arithmetic operations require int operands", error["message"])

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_arithmetic_missing_type(self, mock_traverse: MagicMock) -> None:
        """测试：算术操作操作数缺少 data_type"""
        left = {"type": "literal", "value": 5, "line": 1, "column": 1}  # 没有 data_type
        right = self._create_operand("int", 3)
        node = self._create_node("/", [left, right], line=18, column=12)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("arithmetic operations require int operands", error["message"])

    # ==================== Error Cases: Invalid Comparison Operand Types ====================

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_comparison_mixed_types(self, mock_traverse: MagicMock) -> None:
        """测试：比较操作类型不一致（int vs char）"""
        left = self._create_operand("int", 5)
        right = self._create_operand("char", 'a')
        node = self._create_node("==", [left, right], line=20, column=10)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("comparison operations require consistent types", error["message"])
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 10)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_comparison_all_operators_mixed(self, mock_traverse: MagicMock) -> None:
        """测试：所有比较操作符在类型不一致时都报错"""
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            self.symbol_table["errors"] = []
            left = self._create_operand("int", 1)
            right = self._create_operand("char", 'a')
            node = self._create_node(op, [left, right])

            _handle_binary_op(node, self.symbol_table)

            self.assertEqual(len(self.symbol_table["errors"]), 1, f"Operator {op} should produce error for mixed types")
            error = self.symbol_table["errors"][0]
            self.assertIn("comparison operations require consistent types", error["message"])

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_comparison_one_missing_type(self, mock_traverse: MagicMock) -> None:
        """测试：比较操作一个操作数缺少类型"""
        left = self._create_operand("int", 5)
        right = {"type": "literal", "value": 'a', "line": 1, "column": 1}  # 没有 data_type
        node = self._create_node("!=", [left, right], line=22, column=15)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIn("comparison operations require consistent types", error["message"])

    # ==================== Edge Cases ====================

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_empty_children_list(self, mock_traverse: MagicMock) -> None:
        """测试：children 字段为空列表"""
        node = {
            "type": "binary_op",
            "value": "+",
            "children": [],
            "line": 1,
            "column": 1
        }

        _handle_binary_op(node, self.symbol_table)

        mock_traverse.assert_not_called()
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_missing_children_field(self, mock_traverse: MagicMock) -> None:
        """测试：节点缺少 children 字段"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 1,
            "column": 1
        }

        _handle_binary_op(node, self.symbol_table)

        mock_traverse.assert_not_called()
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_missing_value_field(self, mock_traverse: MagicMock) -> None:
        """测试：节点缺少 value 字段（操作符）"""
        left = self._create_operand("int", 5)
        right = self._create_operand("int", 3)
        node = {
            "type": "binary_op",
            "children": [left, right],
            "line": 1,
            "column": 1
        }

        _handle_binary_op(node, self.symbol_table)

        # 应该仍然遍历操作数，但操作符为空字符串
        self.assertEqual(mock_traverse.call_count, 2)
        # 空字符串不是算术或比较操作符，所以不会记录类型错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_none_operands(self, mock_traverse: MagicMock) -> None:
        """测试：操作数为 None"""
        node = self._create_node("+", [None, None], line=25, column=30)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([call(None, self.symbol_table), call(None, self.symbol_table)])
        # None 操作数没有 data_type，应该报错
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_unknown_operator(self, mock_traverse: MagicMock) -> None:
        """测试：未知的操作符"""
        left = self._create_operand("int", 5)
        right = self._create_operand("int", 3)
        node = self._create_node("%", [left, right])  # % 不是支持的算术操作符

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)
        # 未知操作符不会被分类为算术或比较，所以不会记录类型错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_preserves_existing_errors(self, mock_traverse: MagicMock) -> None:
        """测试：保留符号表中已有的错误"""
        self.symbol_table["errors"] = [
            {"type": "error", "message": "Previous error", "line": 0, "column": 0}
        ]
        left = self._create_operand("char", 'a')
        right = self._create_operand("int", 5)
        node = self._create_node("+", [left, right], line=30, column=40)

        _handle_binary_op(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(self.symbol_table["errors"][0]["message"], "Previous error")

    @patch('._handle_binary_op_package._handle_binary_op_src._traverse_node')
    def test_handle_binary_op_symbol_table_without_errors_field(self, mock_traverse: MagicMock) -> None:
        """测试：符号表没有 errors 字段时自动创建"""
        symbol_table_no_errors: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0
        }
        node = self._create_node("+", [], line=1, column=1)

        _handle_binary_op(node, symbol_table_no_errors)

        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
