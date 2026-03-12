# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_literal 函数测试
"""

import unittest
from typing import Any, Dict

from ._handle_literal_src import _handle_literal


# Type aliases for clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleLiteral(unittest.TestCase):
    """测试 _handle_literal 函数的各种场景"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "errors": []
        }

    def _create_literal_node(
        self,
        value: Any,
        data_type: str,
        line: int = 1,
        column: int = 1
    ) -> AST:
        """辅助函数：创建 literal 类型的 AST 节点"""
        return {
            "type": "literal",
            "value": value,
            "data_type": data_type,
            "line": line,
            "column": column
        }

    def _create_non_literal_node(self, node_type: str = "identifier") -> AST:
        """辅助函数：创建非 literal 类型的 AST 节点"""
        return {
            "type": node_type,
            "value": "some_value",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

    # ==================== Happy Path 测试 ====================

    def test_valid_int_literal(self) -> None:
        """测试有效的整数字面量"""
        node = self._create_literal_node(value=42, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_valid_char_literal_single_char(self) -> None:
        """测试有效的字符字面量（单个字符）"""
        node = self._create_literal_node(value="a", data_type="char")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_valid_char_literal_special_char(self) -> None:
        """测试有效的特殊字符字面量"""
        node = self._create_literal_node(value="\n", data_type="char")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_valid_int_literal_zero(self) -> None:
        """测试有效的整数字面量（零）"""
        node = self._create_literal_node(value=0, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_valid_int_literal_negative(self) -> None:
        """测试有效的负整数字面量"""
        node = self._create_literal_node(value=-100, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    # ==================== 边界值测试 ====================

    def test_int_literal_large_value(self) -> None:
        """测试大整数值"""
        node = self._create_literal_node(value=2147483647, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_char_literal_whitespace(self) -> None:
        """测试空白字符作为字面量"""
        node = self._create_literal_node(value=" ", data_type="char")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    # ==================== 非法输入测试 ====================

    def test_invalid_int_literal_float_value(self) -> None:
        """测试无效的整数字面量（浮点数值）"""
        node = self._create_literal_node(value=3.14, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_error")
        self.assertIn("Expected int literal", error["message"])
        self.assertEqual(error["line"], 1)
        self.assertEqual(error["column"], 1)

    def test_invalid_int_literal_string_value(self) -> None:
        """测试无效的整数字面量（字符串值）"""
        node = self._create_literal_node(value="42", data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_error")
        self.assertIn("Expected int literal", error["message"])

    def test_invalid_int_literal_none_value(self) -> None:
        """测试无效的整数字面量（None 值）"""
        node = self._create_literal_node(value=None, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        # None value should not produce error (early return in _validate_literal_value)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_invalid_char_literal_empty_string(self) -> None:
        """测试无效的字符字面量（空字符串）"""
        node = self._create_literal_node(value="", data_type="char")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_error")
        self.assertIn("Expected char literal", error["message"])

    def test_invalid_char_literal_multiple_chars(self) -> None:
        """测试无效的字符字面量（多个字符）"""
        node = self._create_literal_node(value="ab", data_type="char")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_error")
        self.assertIn("Expected char literal", error["message"])

    def test_invalid_char_literal_int_value(self) -> None:
        """测试无效的字符字面量（整数值）"""
        node = self._create_literal_node(value=97, data_type="char")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_error")
        self.assertIn("Expected char literal", error["message"])

    # ==================== 多分支逻辑测试 ====================

    def test_invalid_data_type(self) -> None:
        """测试无效的数据类型"""
        node = self._create_literal_node(value=42, data_type="float")
        _handle_literal(node, self.symbol_table)
        
        # Invalid data type should not produce error (early return)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_invalid_data_type_none(self) -> None:
        """测试 None 数据类型"""
        node = self._create_literal_node(value=42, data_type=None)
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_non_literal_node_type(self) -> None:
        """测试非 literal 类型的节点"""
        node = self._create_non_literal_node("identifier")
        _handle_literal(node, self.symbol_table)
        
        # Should return early without processing
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_node_missing_type_field(self) -> None:
        """测试缺少 type 字段的节点"""
        node = {
            "value": 42,
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        _handle_literal(node, self.symbol_table)
        
        # node.get("type") returns None, which != "literal", so early return
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    # ==================== 错误位置信息测试 ====================

    def test_error_reports_correct_location(self) -> None:
        """测试错误报告正确的位置信息"""
        node = self._create_literal_node(
            value="invalid",
            data_type="int",
            line=10,
            column=25
        )
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 25)

    # ==================== 符号表状态测试 ====================

    def test_symbol_table_not_modified_on_valid_literal(self) -> None:
        """测试有效字面量不修改符号表（除了 errors）"""
        original_variables = self.symbol_table["variables"].copy()
        original_functions = self.symbol_table["functions"].copy()
        original_scope = self.symbol_table["current_scope"]
        
        node = self._create_literal_node(value=42, data_type="int")
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(self.symbol_table["variables"], original_variables)
        self.assertEqual(self.symbol_table["functions"], original_functions)
        self.assertEqual(self.symbol_table["current_scope"], original_scope)

    def test_multiple_errors_accumulated(self) -> None:
        """测试多个错误能够累积"""
        node1 = self._create_literal_node(value=3.14, data_type="int", line=1, column=1)
        node2 = self._create_literal_node(value="ab", data_type="char", line=2, column=2)
        
        _handle_literal(node1, self.symbol_table)
        _handle_literal(node2, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 2)

    def test_symbol_table_without_errors_list(self) -> None:
        """测试符号表没有 errors 列表时的处理"""
        symbol_table_no_errors: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        
        node = self._create_literal_node(value=3.14, data_type="int")
        # Should not raise exception
        _handle_literal(node, symbol_table_no_errors)
        
        # errors list should be created and contain the error
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)

    # ==================== 节点字段缺失测试 ====================

    def test_node_missing_value_field(self) -> None:
        """测试缺少 value 字段的节点"""
        node = {
            "type": "literal",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        _handle_literal(node, self.symbol_table)
        
        # value is None, should not produce error
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_node_missing_data_type_field(self) -> None:
        """测试缺少 data_type 字段的节点"""
        node = {
            "type": "literal",
            "value": 42,
            "line": 1,
            "column": 1
        }
        _handle_literal(node, self.symbol_table)
        
        # data_type is None, _is_valid_data_type returns False, early return
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_node_missing_line_column_fields(self) -> None:
        """测试缺少 line/column 字段的节点"""
        node = {
            "type": "literal",
            "value": 3.14,
            "data_type": "int"
        }
        _handle_literal(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertIsNone(error["line"])
        self.assertIsNone(error["column"])


if __name__ == "__main__":
    unittest.main()
