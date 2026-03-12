# === std / third-party imports ===
import unittest
from typing import Dict, Any

# === relative import for UUT ===
from _handle_literal_src import _handle_literal

# === Type aliases (matching UUT) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleLiteral(unittest.TestCase):
    """单元测试：_handle_literal 函数"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.empty_symbol_table: SymbolTable = {}

    def test_literal_int_type(self):
        """测试 literal_int 类型节点返回 'int'"""
        node: AST = {
            "type": "literal_int",
            "value": 42,
            "data_type": "int",
            "line": 1,
            "column": 5
        }
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "int")

    def test_int_literal_type(self):
        """测试 int_literal 类型节点返回 'int'"""
        node: AST = {
            "type": "int_literal",
            "value": 100,
            "data_type": "int",
            "line": 2,
            "column": 10
        }
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "int")

    def test_literal_char_type(self):
        """测试 literal_char 类型节点返回 'char'"""
        node: AST = {
            "type": "literal_char",
            "value": 'a',
            "data_type": "char",
            "line": 3,
            "column": 15
        }
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "char")

    def test_char_literal_type(self):
        """测试 char_literal 类型节点返回 'char'"""
        node: AST = {
            "type": "char_literal",
            "value": 'z',
            "data_type": "char",
            "line": 4,
            "column": 20
        }
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "char")

    def test_unknown_type_returns_void(self):
        """测试未知类型节点返回 'void'"""
        node: AST = {
            "type": "literal_float",
            "value": 3.14,
            "data_type": "float",
            "line": 5,
            "column": 25
        }
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "void")

    def test_missing_type_field_returns_void(self):
        """测试缺少 type 字段的节点返回 'void'"""
        node: AST = {
            "value": 42,
            "data_type": "int",
            "line": 6,
            "column": 30
        }
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "void")

    def test_empty_node_returns_void(self):
        """测试空节点返回 'void'"""
        node: AST = {}
        result = _handle_literal(node, self.empty_symbol_table)
        self.assertEqual(result, "void")

    def test_symbol_table_not_used(self):
        """测试 symbol_table 参数不影响结果（纯函数）"""
        node: AST = {
            "type": "literal_int",
            "value": 42
        }
        empty_table: SymbolTable = {}
        populated_table: SymbolTable = {
            "variables": {"x": {"type": "int"}},
            "functions": {"main": {}},
            "current_scope": 1
        }
        result_empty = _handle_literal(node, empty_table)
        result_populated = _handle_literal(node, populated_table)
        self.assertEqual(result_empty, result_populated)
        self.assertEqual(result_empty, "int")

    def test_various_int_values(self):
        """测试不同 int 字面量值都返回 'int'"""
        test_values = [0, -1, 2147483647, -2147483648]
        for value in test_values:
            node: AST = {
                "type": "literal_int",
                "value": value
            }
            result = _handle_literal(node, self.empty_symbol_table)
            self.assertEqual(result, "int", f"Failed for value: {value}")

    def test_various_char_values(self):
        """测试不同 char 字面量值都返回 'char'"""
        test_values = ['a', 'Z', '0', ' ', '\n', '\t']
        for value in test_values:
            node: AST = {
                "type": "literal_char",
                "value": value
            }
            result = _handle_literal(node, self.empty_symbol_table)
            self.assertEqual(result, "char", f"Failed for value: {repr(value)}")


if __name__ == "__main__":
    unittest.main()
