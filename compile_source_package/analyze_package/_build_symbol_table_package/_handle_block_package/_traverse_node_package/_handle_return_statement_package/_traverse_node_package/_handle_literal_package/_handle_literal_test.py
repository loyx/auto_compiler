# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_literal 函数测试
测试模块：main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_literal_package._handle_literal_src
"""

import unittest
from typing import Any

# 相对导入被测模块
from ._handle_literal_src import (
    _handle_literal,
    _infer_data_type,
    _validate_literal,
    _record_error,
    AST,
    SymbolTable,
)


class TestHandleLiteral(unittest.TestCase):
    """_handle_literal 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "errors": [],
        }

    def _create_node(
        self,
        value: Any = None,
        data_type: str = None,
        line: int = 1,
        column: int = 1,
    ) -> AST:
        """辅助函数：创建 AST 节点"""
        node: AST = {
            "type": "literal",
            "children": [],
            "line": line,
            "column": column,
        }
        if value is not None:
            node["value"] = value
        if data_type is not None:
            node["data_type"] = data_type
        return node

    # ==================== Happy Path 测试 ====================

    def test_handle_literal_valid_int_with_type(self) -> None:
        """测试：有效的整数字面量（已指定类型）"""
        node = self._create_node(value=42, data_type="int", line=1, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(node.get("data_type"), "int")
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_valid_int_inferred(self) -> None:
        """测试：有效的整数字面量（推断类型）"""
        node = self._create_node(value=100, data_type=None, line=2, column=5)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(node.get("data_type"), "int")
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_valid_char_with_type(self) -> None:
        """测试：有效的字符字面量（已指定类型）"""
        node = self._create_node(value="a", data_type="char", line=3, column=10)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(node.get("data_type"), "char")
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_valid_char_inferred(self) -> None:
        """测试：有效的字符字面量（推断类型）"""
        node = self._create_node(value="X", data_type=None, line=4, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(node.get("data_type"), "char")
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_valid_string_inferred(self) -> None:
        """测试：有效的字符串字面量（推断类型）"""
        node = self._create_node(value="hello", data_type=None, line=5, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(node.get("data_type"), "string")
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    # ==================== 边界值测试 ====================

    def test_handle_literal_int_min_boundary(self) -> None:
        """测试：整数最小值边界（-2147483648）"""
        node = self._create_node(value=-2147483648, data_type="int", line=1, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_int_max_boundary(self) -> None:
        """测试：整数最大值边界（2147483647）"""
        node = self._create_node(value=2147483647, data_type="int", line=1, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_int_min_boundary_minus_one(self) -> None:
        """测试：整数最小值减一（-2147483649，应报错）"""
        node = self._create_node(value=-2147483649, data_type="int", line=10, column=5)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("out of range", errors[0])

    def test_handle_literal_int_max_boundary_plus_one(self) -> None:
        """测试：整数最大值加一（2147483648，应报错）"""
        node = self._create_node(value=2147483648, data_type="int", line=10, column=5)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("out of range", errors[0])

    def test_handle_literal_zero(self) -> None:
        """测试：零值"""
        node = self._create_node(value=0, data_type="int", line=1, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    def test_handle_literal_negative_int(self) -> None:
        """测试：负整数"""
        node = self._create_node(value=-100, data_type="int", line=1, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        self.assertEqual(len(self.symbol_table.get("errors", [])), 0)

    # ==================== 非法输入测试 ====================

    def test_handle_literal_none_value(self) -> None:
        """测试：None 值（应报错）"""
        node = self._create_node(value=None, data_type="int", line=7, column=3)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("None", errors[0])

    def test_handle_literal_invalid_char_too_long(self) -> None:
        """测试：无效的字符字面量（多个字符，应报错）"""
        node = self._create_node(value="ab", data_type="char", line=8, column=2)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid char literal", errors[0])

    def test_handle_literal_invalid_char_empty_string(self) -> None:
        """测试：无效的字符字面量（空字符串，应报错）"""
        node = self._create_node(value="", data_type="char", line=8, column=2)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid char literal", errors[0])

    def test_handle_literal_int_type_with_string_value(self) -> None:
        """测试：int 类型但值为字符串（应报错）"""
        node = self._create_node(value="not_a_number", data_type="int", line=9, column=1)
        result = _handle_literal(node, self.symbol_table)
        self.assertIsNone(result)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid literal value", errors[0])

    # ==================== 类型推断测试 ====================

    def test_handle_literal_type_inference_int(self) -> None:
        """测试：类型推断 - 整数"""
        node = self._create_node(value=42, data_type=None)
        _handle_literal(node, self.symbol_table)
        self.assertEqual(node.get("data_type"), "int")

    def test_handle_literal_type_inference_char(self) -> None:
        """测试：类型推断 - 单字符"""
        node = self._create_node(value="c", data_type=None)
        _handle_literal(node, self.symbol_table)
        self.assertEqual(node.get("data_type"), "char")

    def test_handle_literal_type_inference_string(self) -> None:
        """测试：类型推断 - 多字符字符串"""
        node = self._create_node(value="test", data_type=None)
        _handle_literal(node, self.symbol_table)
        self.assertEqual(node.get("data_type"), "string")

    def test_handle_literal_type_inference_unknown(self) -> None:
        """测试：类型推断 - 未知类型（如 float）"""
        node = self._create_node(value=3.14, data_type=None)
        _handle_literal(node, self.symbol_table)
        self.assertEqual(node.get("data_type"), "unknown")

    def test_handle_literal_type_inference_list(self) -> None:
        """测试：类型推断 - 列表类型"""
        node = self._create_node(value=[1, 2, 3], data_type=None)
        _handle_literal(node, self.symbol_table)
        self.assertEqual(node.get("data_type"), "unknown")

    # ==================== 错误记录测试 ====================

    def test_handle_literal_error_recording_multiple_errors(self) -> None:
        """测试：错误记录 - 多个错误"""
        # 第一个错误
        node1 = self._create_node(value=None, data_type="int", line=1, column=1)
        _handle_literal(node1, self.symbol_table)
        
        # 第二个错误
        node2 = self._create_node(value=9999999999999, data_type="int", line=2, column=2)
        _handle_literal(node2, self.symbol_table)
        
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 2)

    def test_handle_literal_error_message_contains_location(self) -> None:
        """测试：错误消息包含位置信息"""
        node = self._create_node(value=None, data_type="int", line=15, column=20)
        _handle_literal(node, self.symbol_table)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 15", errors[0])
        self.assertIn("column 20", errors[0])

    def test_handle_literal_no_errors_key_initialized(self) -> None:
        """测试：符号表没有 errors 键时自动初始化"""
        symbol_table_no_errors: SymbolTable = {
            "variables": {},
            "functions": {},
        }
        node = self._create_node(value=None, data_type="int")
        _handle_literal(node, symbol_table_no_errors)
        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)

    # ==================== 默认值测试 ====================

    def test_handle_literal_missing_line_column(self) -> None:
        """测试：缺少 line 和 column 字段时使用默认值"""
        node: AST = {
            "type": "literal",
            "value": None,
            "data_type": "int",
        }
        _handle_literal(node, self.symbol_table)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 0", errors[0])
        self.assertIn("column 0", errors[0])

    def test_handle_literal_missing_value_key(self) -> None:
        """测试：缺少 value 字段时视为 None"""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "line": 1,
            "column": 1,
        }
        _handle_literal(node, self.symbol_table)
        errors = self.symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("None", errors[0])


class TestInferDataType(unittest.TestCase):
    """_infer_data_type 辅助函数的单元测试类"""

    def test_infer_data_type_int_positive(self) -> None:
        """测试：推断正整数类型"""
        self.assertEqual(_infer_data_type(42), "int")

    def test_infer_data_type_int_negative(self) -> None:
        """测试：推断负整数类型"""
        self.assertEqual(_infer_data_type(-100), "int")

    def test_infer_data_type_int_zero(self) -> None:
        """测试：推断零的类型"""
        self.assertEqual(_infer_data_type(0), "int")

    def test_infer_data_type_char_single(self) -> None:
        """测试：推断单字符类型"""
        self.assertEqual(_infer_data_type("a"), "char")

    def test_infer_data_type_char_special(self) -> None:
        """测试：推断特殊字符类型"""
        self.assertEqual(_infer_data_type("@"), "char")

    def test_infer_data_type_string_multiple(self) -> None:
        """测试：推断多字符字符串类型"""
        self.assertEqual(_infer_data_type("hello"), "string")

    def test_infer_data_type_string_empty(self) -> None:
        """测试：推断空字符串类型"""
        self.assertEqual(_infer_data_type(""), "string")

    def test_infer_data_type_float(self) -> None:
        """测试：推断浮点数类型"""
        self.assertEqual(_infer_data_type(3.14), "unknown")

    def test_infer_data_type_bool(self) -> None:
        """测试：推断布尔类型"""
        self.assertEqual(_infer_data_type(True), "unknown")

    def test_infer_data_type_none(self) -> None:
        """测试：推断 None 类型"""
        self.assertEqual(_infer_data_type(None), "unknown")

    def test_infer_data_type_list(self) -> None:
        """测试：推断列表类型"""
        self.assertEqual(_infer_data_type([1, 2, 3]), "unknown")

    def test_infer_data_type_dict(self) -> None:
        """测试：推断字典类型"""
        self.assertEqual(_infer_data_type({"key": "value"}), "unknown")


class TestValidateLiteral(unittest.TestCase):
    """_validate_literal 辅助函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {"errors": []}

    def test_validate_literal_valid_int(self) -> None:
        """测试：验证有效整数"""
        result = _validate_literal(42, "int", 1, 1, self.symbol_table)
        self.assertTrue(result)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_validate_literal_valid_char(self) -> None:
        """测试：验证有效字符"""
        result = _validate_literal("a", "char", 1, 1, self.symbol_table)
        self.assertTrue(result)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_validate_literal_valid_string(self) -> None:
        """测试：验证有效字符串"""
        result = _validate_literal("hello", "string", 1, 1, self.symbol_table)
        self.assertTrue(result)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_validate_literal_none_value(self) -> None:
        """测试：验证 None 值"""
        result = _validate_literal(None, "int", 5, 10, self.symbol_table)
        self.assertFalse(result)
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    def test_validate_literal_int_out_of_range_low(self) -> None:
        """测试：验证整数超出下限"""
        result = _validate_literal(-2147483649, "int", 1, 1, self.symbol_table)
        self.assertFalse(result)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("out of range", self.symbol_table["errors"][0])

    def test_validate_literal_int_out_of_range_high(self) -> None:
        """测试：验证整数超出上限"""
        result = _validate_literal(2147483648, "int", 1, 1, self.symbol_table)
        self.assertFalse(result)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("out of range", self.symbol_table["errors"][0])

    def test_validate_literal_char_too_long(self) -> None:
        """测试：验证字符太长"""
        result = _validate_literal("abc", "char", 1, 1, self.symbol_table)
        self.assertFalse(result)
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    def test_validate_literal_char_empty(self) -> None:
        """测试：验证字符为空"""
        result = _validate_literal("", "char", 1, 1, self.symbol_table)
        self.assertFalse(result)
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    def test_validate_literal_int_type_string_value(self) -> None:
        """测试：int 类型但值为字符串"""
        result = _validate_literal("not_int", "int", 1, 1, self.symbol_table)
        self.assertFalse(result)
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    def test_validate_literal_unknown_type(self) -> None:
        """测试：未知类型总是有效"""
        result = _validate_literal([1, 2, 3], "unknown", 1, 1, self.symbol_table)
        self.assertTrue(result)
        self.assertEqual(len(self.symbol_table["errors"]), 0)


class TestRecordError(unittest.TestCase):
    """_record_error 辅助函数的单元测试类"""

    def test_record_error_initializes_list(self) -> None:
        """测试：记录错误时初始化 errors 列表"""
        symbol_table: SymbolTable = {}
        _record_error(symbol_table, "Test error message")
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0], "Test error message")

    def test_record_error_appends_to_existing(self) -> None:
        """测试：记录错误时追加到现有列表"""
        symbol_table: SymbolTable = {"errors": ["Existing error"]}
        _record_error(symbol_table, "New error message")
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1], "New error message")

    def test_record_error_multiple_errors(self) -> None:
        """测试：记录多个错误"""
        symbol_table: SymbolTable = {}
        _record_error(symbol_table, "Error 1")
        _record_error(symbol_table, "Error 2")
        _record_error(symbol_table, "Error 3")
        self.assertEqual(len(symbol_table["errors"]), 3)


if __name__ == "__main__":
    unittest.main()
