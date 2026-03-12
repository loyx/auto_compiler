# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === sub function imports ===
from ._handle_binary_op_src import _handle_binary_op, _get_operand_type, _check_type_compatibility

# === Type Aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBinaryOp(unittest.TestCase):
    """测试 _handle_binary_op 函数"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

    def test_arithmetic_op_compatible_types(self):
        """测试算术运算符：两个 int 类型兼容"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 10, "column": 5},
                {"type": "literal", "value": 3, "data_type": "int", "line": 10, "column": 7}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_arithmetic_op_incompatible_types(self):
        """测试算术运算符：int 和 char 类型不兼容"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 10, "column": 5},
                {"type": "literal", "value": 'a', "data_type": "char", "line": 10, "column": 7}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Cannot apply '+' to types 'int' and 'char'", 
                     self.symbol_table["errors"][0]["message"])
        self.assertEqual(self.symbol_table["errors"][0]["line"], 10)
        self.assertEqual(self.symbol_table["errors"][0]["column"], 5)

    def test_comparison_op_same_types(self):
        """测试比较运算符：相同类型兼容"""
        node = {
            "type": "binary_op",
            "value": "==",
            "line": 15,
            "column": 10,
            "children": [
                {"type": "literal", "value": 'a', "data_type": "char", "line": 15, "column": 10},
                {"type": "literal", "value": 'b', "data_type": "char", "line": 15, "column": 12}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_comparison_op_different_types(self):
        """测试比较运算符：不同类型不兼容"""
        node = {
            "type": "binary_op",
            "value": "!=",
            "line": 20,
            "column": 3,
            "children": [
                {"type": "literal", "value": 10, "data_type": "int", "line": 20, "column": 3},
                {"type": "literal", "value": 'x', "data_type": "char", "line": 20, "column": 6}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Cannot apply '!=' to types 'int' and 'char'", 
                     self.symbol_table["errors"][0]["message"])

    def test_logical_op_compatible_types(self):
        """测试逻辑运算符：两个 int 类型兼容"""
        node = {
            "type": "binary_op",
            "value": "&&",
            "line": 25,
            "column": 8,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 25, "column": 8},
                {"type": "literal", "value": 0, "data_type": "int", "line": 25, "column": 11}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_logical_op_incompatible_types(self):
        """测试逻辑运算符：char 类型不兼容"""
        node = {
            "type": "binary_op",
            "value": "||",
            "line": 30,
            "column": 12,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 30, "column": 12},
                {"type": "literal", "value": 'a', "data_type": "char", "line": 30, "column": 15}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Cannot apply '||' to types 'int' and 'char'", 
                     self.symbol_table["errors"][0]["message"])

    def test_identifier_operands_from_symbol_table(self):
        """测试操作数为变量时从符号表获取类型"""
        self.symbol_table["variables"] = {
            "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 1},
            "y": {"data_type": "int", "is_declared": True, "line": 2, "column": 1, "scope_level": 1}
        }
        
        node = {
            "type": "binary_op",
            "value": "-",
            "line": 35,
            "column": 5,
            "children": [
                {"type": "identifier", "value": "x", "line": 35, "column": 5},
                {"type": "identifier", "value": "y", "line": 35, "column": 7}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_identifier_operands_incompatible_types(self):
        """测试操作数为变量时类型不兼容"""
        self.symbol_table["variables"] = {
            "a": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 1},
            "b": {"data_type": "char", "is_declared": True, "line": 2, "column": 1, "scope_level": 1}
        }
        
        node = {
            "type": "binary_op",
            "value": "*",
            "line": 40,
            "column": 10,
            "children": [
                {"type": "identifier", "value": "a", "line": 40, "column": 10},
                {"type": "identifier", "value": "b", "line": 40, "column": 12}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Cannot apply '*' to types 'int' and 'char'", 
                     self.symbol_table["errors"][0]["message"])

    def test_no_children(self):
        """测试没有子节点的情况"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 45,
            "column": 5
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        # 没有操作数，不应该记录错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_one_child_only(self):
        """测试只有一个子节点的情况"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 50,
            "column": 5,
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 50, "column": 5}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        # 只有一个操作数，不应该记录错误（因为 left_type 或 right_type 为 None）
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_errors_list_initialized_if_not_present(self):
        """测试 symbol_table 没有 errors 字段时自动初始化"""
        symbol_table_no_errors = {
            "variables": {},
            "functions": {},
            "current_scope": 1
        }
        
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 55,
            "column": 5,
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 55, "column": 5},
                {"type": "literal", "value": 'a', "data_type": "char", "line": 55, "column": 7}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, symbol_table_no_errors)
        
        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)

    def test_traverse_node_called_for_children(self):
        """测试 _traverse_node 被正确调用处理子节点"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 60,
            "column": 5,
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 60, "column": 5},
                {"type": "literal", "value": 3, "data_type": "int", "line": 60, "column": 7}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node") as mock_traverse:
            _handle_binary_op(node, self.symbol_table)
            
            # 验证 _traverse_node 被调用了 2 次（左右操作数）
            self.assertEqual(mock_traverse.call_count, 2)
            # 验证调用参数
            mock_traverse.assert_any_call(node["children"][0], self.symbol_table)
            mock_traverse.assert_any_call(node["children"][1], self.symbol_table)

    def test_nested_binary_op(self):
        """测试嵌套二元操作"""
        node = {
            "type": "binary_op",
            "value": "+",
            "line": 65,
            "column": 5,
            "children": [
                {
                    "type": "binary_op",
                    "value": "*",
                    "children": [
                        {"type": "literal", "value": 2, "data_type": "int"},
                        {"type": "literal", "value": 3, "data_type": "int"}
                    ]
                },
                {"type": "literal", "value": 4, "data_type": "int"}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        # 嵌套操作应该能正确获取类型
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_unknown_operator(self):
        """测试未知运算符（应该不报错）"""
        node = {
            "type": "binary_op",
            "value": "**",
            "line": 70,
            "column": 5,
            "children": [
                {"type": "literal", "value": 2, "data_type": "int"},
                {"type": "literal", "value": 'a', "data_type": "char"}
            ]
        }
        
        with patch(".._traverse_node_src._traverse_node"):
            _handle_binary_op(node, self.symbol_table)
        
        # 未知运算符不报错（根据实现返回 True）
        self.assertEqual(len(self.symbol_table["errors"]), 0)


class TestGetOperandType(unittest.TestCase):
    """测试 _get_operand_type helper 函数"""

    def test_literal_with_data_type(self):
        """测试字面量节点有 data_type 字段"""
        node = {"type": "literal", "value": 5, "data_type": "int"}
        symbol_table = {"variables": {}}
        
        result = _get_operand_type(node, symbol_table)
        
        self.assertEqual(result, "int")

    def test_identifier_from_symbol_table(self):
        """测试标识符从符号表获取类型"""
        node = {"type": "identifier", "value": "x"}
        symbol_table = {
            "variables": {
                "x": {"data_type": "char", "is_declared": True, "line": 1, "column": 1, "scope_level": 1}
            }
        }
        
        result = _get_operand_type(node, symbol_table)
        
        self.assertEqual(result, "char")

    def test_identifier_not_in_symbol_table(self):
        """测试标识符不在符号表中"""
        node = {"type": "identifier", "value": "unknown"}
        symbol_table = {"variables": {}}
        
        result = _get_operand_type(node, symbol_table)
        
        self.assertIsNone(result)

    def test_nested_binary_op(self):
        """测试嵌套二元操作节点"""
        node = {
            "type": "binary_op",
            "value": "+",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int"},
                {"type": "literal", "value": 3, "data_type": "int"}
            ]
        }
        symbol_table = {"variables": {}}
        
        result = _get_operand_type(node, symbol_table)
        
        self.assertEqual(result, "int")

    def test_no_data_type_no_identifier(self):
        """测试节点没有 data_type 也不是标识符"""
        node = {"type": "unknown_type", "value": "something"}
        symbol_table = {"variables": {}}
        
        result = _get_operand_type(node, symbol_table)
        
        self.assertIsNone(result)


class TestCheckTypeCompatibility(unittest.TestCase):
    """测试 _check_type_compatibility helper 函数"""

    def test_arithmetic_both_int(self):
        """测试算术运算：两个 int"""
        for op in ["+", "-", "*", "/"]:
            result = _check_type_compatibility(op, "int", "int")
            self.assertTrue(result, f"Operator {op} should be compatible with int, int")

    def test_arithmetic_mixed_types(self):
        """测试算术运算：混合类型"""
        for op in ["+", "-", "*", "/"]:
            result = _check_type_compatibility(op, "int", "char")
            self.assertFalse(result, f"Operator {op} should not be compatible with int, char")
            
            result = _check_type_compatibility(op, "char", "int")
            self.assertFalse(result, f"Operator {op} should not be compatible with char, int")

    def test_arithmetic_both_char(self):
        """测试算术运算：两个 char"""
        for op in ["+", "-", "*", "/"]:
            result = _check_type_compatibility(op, "char", "char")
            self.assertFalse(result, f"Operator {op} should not be compatible with char, char")

    def test_comparison_same_types(self):
        """测试比较运算：相同类型"""
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            result_int = _check_type_compatibility(op, "int", "int")
            self.assertTrue(result_int, f"Operator {op} should be compatible with int, int")
            
            result_char = _check_type_compatibility(op, "char", "char")
            self.assertTrue(result_char, f"Operator {op} should be compatible with char, char")

    def test_comparison_different_types(self):
        """测试比较运算：不同类型"""
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            result = _check_type_compatibility(op, "int", "char")
            self.assertFalse(result, f"Operator {op} should not be compatible with int, char")

    def test_logical_both_int(self):
        """测试逻辑运算：两个 int"""
        for op in ["&&", "||"]:
            result = _check_type_compatibility(op, "int", "int")
            self.assertTrue(result, f"Operator {op} should be compatible with int, int")

    def test_logical_mixed_types(self):
        """测试逻辑运算：混合类型"""
        for op in ["&&", "||"]:
            result = _check_type_compatibility(op, "int", "char")
            self.assertFalse(result, f"Operator {op} should not be compatible with int, char")
            
            result = _check_type_compatibility(op, "char", "int")
            self.assertFalse(result, f"Operator {op} should not be compatible with char, int")

    def test_logical_both_char(self):
        """测试逻辑运算：两个 char"""
        for op in ["&&", "||"]:
            result = _check_type_compatibility(op, "char", "char")
            self.assertFalse(result, f"Operator {op} should not be compatible with char, char")

    def test_unknown_operator(self):
        """测试未知运算符"""
        result = _check_type_compatibility("**", "int", "char")
        self.assertTrue(result, "Unknown operator should return True (no error)")


if __name__ == "__main__":
    unittest.main()
