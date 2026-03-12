# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._handle_assignment_src import _handle_assignment

# === type aliases for test clarity ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """测试 _handle_assignment 函数的各种场景"""

    def test_happy_path_variable_declared_type_matches(self):
        """Happy Path: 变量已声明且类型匹配，不应产生错误"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_not_declared(self):
        """边界值：变量未声明，应记录错误"""
        node: AST = {
            "type": "assignment",
            "value": "y",
            "data_type": "int",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Variable 'y' not declared", symbol_table["errors"][0])
        self.assertIn("line 15", symbol_table["errors"][0])
        self.assertIn("column 8", symbol_table["errors"][0])

    def test_type_mismatch(self):
        """边界值：类型不匹配，应记录错误"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch for 'x'", symbol_table["errors"][0])
        self.assertIn("line 20", symbol_table["errors"][0])
        self.assertIn("column 3", symbol_table["errors"][0])

    def test_empty_symbol_table_variables(self):
        """边界值：符号表 variables 为空，应记录未声明错误"""
        node: AST = {
            "type": "assignment",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Variable 'z' not declared", symbol_table["errors"][0])

    def test_symbol_table_without_errors_key(self):
        """边界值：符号表没有 errors 键，函数应自动创建"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_node_missing_line_column_defaults_to_zero(self):
        """边界值：节点缺少 line/column，应默认使用 0"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "int"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 0", symbol_table["errors"][0])
        self.assertIn("column 0", symbol_table["errors"][0])

    def test_multiple_errors_accumulated(self):
        """状态变化：多次调用应累积错误"""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        node1: AST = {
            "type": "assignment",
            "value": "y",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "char",
            "line": 11,
            "column": 6
        }
        
        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertIn("Variable 'y' not declared", symbol_table["errors"][0])
        self.assertIn("Type mismatch for 'x'", symbol_table["errors"][1])

    def test_declared_type_none_no_type_check(self):
        """边界值：声明的类型为 None，不应触发类型不匹配错误"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": None, "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_assigned_type_none_no_type_check(self):
        """边界值：赋值的类型为 None，不应触发类型不匹配错误"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": None,
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_char_type_matching(self):
        """Happy Path: char 类型匹配"""
        node: AST = {
            "type": "assignment",
            "value": "c",
            "data_type": "char",
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_returns_none(self):
        """验证函数返回 None"""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
