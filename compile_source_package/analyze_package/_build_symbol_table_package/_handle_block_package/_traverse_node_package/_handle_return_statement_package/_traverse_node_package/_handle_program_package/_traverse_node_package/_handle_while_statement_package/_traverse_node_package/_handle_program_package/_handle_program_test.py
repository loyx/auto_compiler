# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._handle_program_src import _handle_program


# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# === Test Class ===
class TestHandleProgram(unittest.TestCase):
    """测试_handle_program函数"""

    def test_handle_program_initializes_scope(self):
        """测试初始化作用域字段"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])

    def test_handle_program_initializes_variables_dict(self):
        """测试初始化 variables 字典"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertEqual(symbol_table["variables"], {})

    def test_handle_program_initializes_functions_dict(self):
        """测试初始化 functions 字典"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertIn("functions", symbol_table)
        self.assertEqual(symbol_table["functions"], {})

    def test_handle_program_initializes_errors_list(self):
        """测试初始化 errors 列表"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_program_preserves_existing_variables(self):
        """测试保留已存在的 variables 字典"""
        node: AST = {"type": "program", "children": []}
        existing_vars = {"x": {"data_type": "int", "is_declared": True}}
        symbol_table: SymbolTable = {"variables": existing_vars}
        
        _handle_program(node, symbol_table)
        
        self.assertIs(symbol_table["variables"], existing_vars)
        self.assertEqual(symbol_table["variables"], {"x": {"data_type": "int", "is_declared": True}})

    def test_handle_program_preserves_existing_functions(self):
        """测试保留已存在的 functions 字典"""
        node: AST = {"type": "program", "children": []}
        existing_funcs = {"main": {"return_type": "int", "params": []}}
        symbol_table: SymbolTable = {"functions": existing_funcs}
        
        _handle_program(node, symbol_table)
        
        self.assertIs(symbol_table["functions"], existing_funcs)
        self.assertEqual(symbol_table["functions"], {"main": {"return_type": "int", "params": []}})

    def test_handle_program_preserves_existing_errors(self):
        """测试保留已存在的 errors 列表"""
        node: AST = {"type": "program", "children": []}
        existing_errors = ["Error 1", "Error 2"]
        symbol_table: SymbolTable = {"errors": existing_errors}
        
        _handle_program(node, symbol_table)
        
        self.assertIs(symbol_table["errors"], existing_errors)
        self.assertEqual(symbol_table["errors"], ["Error 1", "Error 2"])

    def test_handle_program_with_partial_symbol_table(self):
        """测试部分初始化的符号表"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {"variables": {"x": {}}}
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertIn("functions", symbol_table)
        self.assertEqual(symbol_table["functions"], {})
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_program_with_complete_symbol_table(self):
        """测试完全初始化的符号表（应只更新 scope 相关字段）"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "variables": {"x": {}},
            "functions": {"main": {}},
            "errors": [],
            "current_scope": 5,
            "scope_stack": [1, 2, 3]
        }
        
        _handle_program(node, symbol_table)
        
        # scope 字段应被重置
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])
        # 其他字段应保持不变
        self.assertEqual(symbol_table["variables"], {"x": {}})
        self.assertEqual(symbol_table["functions"], {"main": {}})
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_program_with_node_children(self):
        """测试带子节点的 program 节点（不遍历子节点）"""
        node: AST = {
            "type": "program",
            "children": [
                {"type": "function_declaration", "value": "main"},
                {"type": "block", "children": []}
            ]
        }
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        # 只初始化符号表，不处理子节点
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_program_with_node_metadata(self):
        """测试带元数据的 program 节点"""
        node: AST = {
            "type": "program",
            "children": [],
            "line": 1,
            "column": 0
        }
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])

    def test_handle_program_multiple_calls_resets_scope(self):
        """测试多次调用会重置作用域"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        # 模拟作用域变化
        symbol_table["current_scope"] = 5
        symbol_table["scope_stack"] = [0, 1, 2]
        
        _handle_program(node, symbol_table)
        
        # 再次调用应重置
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])

    def test_handle_program_returns_none(self):
        """测试函数返回 None"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        result = _handle_program(node, symbol_table)
        
        self.assertIsNone(result)


# === Main ===
if __name__ == "__main__":
    unittest.main()
