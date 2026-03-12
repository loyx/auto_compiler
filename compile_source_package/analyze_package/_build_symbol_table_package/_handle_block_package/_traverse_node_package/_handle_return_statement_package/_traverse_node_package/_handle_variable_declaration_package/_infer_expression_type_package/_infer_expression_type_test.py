#!/usr/bin/env python3
"""
单元测试：_infer_expression_type 函数
测试 AST 表达式类型推断功能
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._infer_expression_type_src import _infer_expression_type


# 类型别名（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestInferExpressionType(unittest.TestCase):
    """_infer_expression_type 函数的单元测试类"""

    def test_literal_int_value(self):
        """测试字面量为整数时返回 'int'"""
        node = {"type": "literal", "value": 42}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_literal_negative_int(self):
        """测试负整数字面量返回 'int'"""
        node = {"type": "literal", "value": -100}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_literal_zero(self):
        """测试零值字面量返回 'int'"""
        node = {"type": "literal", "value": 0}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_literal_single_char_string(self):
        """测试单字符字符串字面量返回 'char'"""
        node = {"type": "literal", "value": "a"}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "char")

    def test_literal_multi_char_string(self):
        """测试多字符字符串字面量返回 'char'（视为 char 数组）"""
        node = {"type": "literal", "value": "hello"}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "char")

    def test_literal_empty_string(self):
        """测试空字符串字面量返回 'char'"""
        node = {"type": "literal", "value": ""}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "char")

    def test_literal_float_value(self):
        """测试浮点数字面量返回 'unknown'"""
        node = {"type": "literal", "value": 3.14}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_literal_none_value(self):
        """测试 None 值字面量返回 'unknown'"""
        node = {"type": "literal", "value": None}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_literal_boolean_value(self):
        """测试布尔值字面量返回 'unknown'"""
        node = {"type": "literal", "value": True}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_identifier_found_in_symbol_table(self):
        """测试在符号表中找到的标识符返回其类型"""
        node = {"type": "identifier", "name": "x"}
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            }
        }
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_identifier_char_type_in_symbol_table(self):
        """测试在符号表中找到的 char 类型标识符"""
        node = {"type": "identifier", "name": "c"}
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            }
        }
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "char")

    def test_identifier_not_found_in_symbol_table(self):
        """测试在符号表中未找到的标识符返回 'unknown'"""
        node = {"type": "identifier", "name": "undefined_var"}
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            }
        }
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_identifier_empty_symbol_table(self):
        """测试空符号表时标识符返回 'unknown'"""
        node = {"type": "identifier", "name": "x"}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_identifier_missing_variables_key(self):
        """测试符号表缺少 variables 键时标识符返回 'unknown'"""
        node = {"type": "identifier", "name": "x"}
        symbol_table = {"functions": {}}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_binary_expression_arithmetic_both_int(self):
        """测试算术运算符两边都是 int 时返回 'int'"""
        node = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_arithmetic_int_and_char(self):
        """测试算术运算符一边是 int 一边是 char 时返回 'int'（char 提升）"""
        node = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": "a"}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_arithmetic_char_and_int(self):
        """测试算术运算符一边是 char 一边是 int 时返回 'int'（char 提升）"""
        node = {
            "type": "binary_expression",
            "operator": "-",
            "left": {"type": "literal", "value": "a"},
            "right": {"type": "literal", "value": 1}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_arithmetic_both_char(self):
        """测试算术运算符两边都是 char 时返回 'int'"""
        node = {
            "type": "binary_expression",
            "operator": "*",
            "left": {"type": "literal", "value": "a"},
            "right": {"type": "literal", "value": "b"}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_comparison_returns_int(self):
        """测试比较运算符返回 'int'（布尔结果用 int 表示）"""
        node = {
            "type": "binary_expression",
            "operator": "==",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_all_comparison_operators(self):
        """测试所有比较运算符都返回 'int'"""
        comparison_ops = ["==", "!=", "<", ">", "<=", ">="]
        for op in comparison_ops:
            node = {
                "type": "binary_expression",
                "operator": op,
                "left": {"type": "literal", "value": 1},
                "right": {"type": "literal", "value": 2}
            }
            symbol_table = {}
            result = _infer_expression_type(node, symbol_table)
            self.assertEqual(result, "int", f"Operator {op} should return 'int'")

    def test_binary_expression_all_arithmetic_operators(self):
        """测试所有算术运算符都正确处理"""
        arithmetic_ops = ["+", "-", "*", "/"]
        for op in arithmetic_ops:
            node = {
                "type": "binary_expression",
                "operator": op,
                "left": {"type": "literal", "value": 10},
                "right": {"type": "literal", "value": 2}
            }
            symbol_table = {}
            result = _infer_expression_type(node, symbol_table)
            self.assertEqual(result, "int", f"Operator {op} should return 'int'")

    def test_binary_expression_unknown_operator(self):
        """测试未知运算符返回 'unknown'"""
        node = {
            "type": "binary_expression",
            "operator": "%",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 2}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_binary_expression_nested_expression(self):
        """测试嵌套表达式递归推断"""
        node = {
            "type": "binary_expression",
            "operator": "+",
            "left": {
                "type": "binary_expression",
                "operator": "*",
                "left": {"type": "literal", "value": 2},
                "right": {"type": "literal", "value": 3}
            },
            "right": {"type": "literal", "value": 4}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_with_identifier(self):
        """测试包含标识符的二元表达式"""
        node = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "identifier", "name": "x"},
            "right": {"type": "literal", "value": 5}
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            }
        }
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_binary_expression_missing_left(self):
        """测试缺少左操作数的二元表达式返回 'unknown'"""
        node = {
            "type": "binary_expression",
            "operator": "+",
            "right": {"type": "literal", "value": 5}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_binary_expression_missing_right(self):
        """测试缺少右操作数的二元表达式返回 'unknown'"""
        node = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": 5}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_node_none(self):
        """测试 None 节点返回 'unknown'"""
        result = _infer_expression_type(None, {})
        self.assertEqual(result, "unknown")

    def test_node_empty_dict(self):
        """测试空字典节点返回 'unknown'"""
        result = _infer_expression_type({}, {})
        self.assertEqual(result, "unknown")

    def test_node_missing_type(self):
        """测试缺少 type 字段的节点返回 'unknown'"""
        node = {"value": 42}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_node_with_data_type_field(self):
        """测试带有 data_type 字段的其他类型节点"""
        node = {"type": "unknown_type", "data_type": "int"}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "int")

    def test_node_with_char_data_type_field(self):
        """测试带有 char data_type 字段的其他类型节点"""
        node = {"type": "unknown_type", "data_type": "char"}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "char")

    def test_node_with_invalid_data_type_field(self):
        """测试带有无效 data_type 字段的节点返回 'unknown'"""
        node = {"type": "unknown_type", "data_type": "float"}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_node_with_none_data_type_field(self):
        """测试 data_type 为 None 的节点返回 'unknown'"""
        node = {"type": "unknown_type", "data_type": None}
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_identifier_missing_name_field(self):
        """测试缺少 name 字段的 identifier 节点返回 'unknown'"""
        node = {"type": "identifier"}
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            }
        }
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_binary_expression_missing_operator(self):
        """测试缺少 operator 字段的 binary_expression 节点返回 'unknown'"""
        node = {
            "type": "binary_expression",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        symbol_table = {}
        result = _infer_expression_type(node, symbol_table)
        self.assertEqual(result, "unknown")

    def test_symbol_table_no_side_effects(self):
        """测试函数不修改符号表"""
        node = {"type": "identifier", "name": "x"}
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            }
        }
        original_symbol_table = str(symbol_table)
        _infer_expression_type(node, symbol_table)
        self.assertEqual(str(symbol_table), original_symbol_table)


if __name__ == "__main__":
    unittest.main()
