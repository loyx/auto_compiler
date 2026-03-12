# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_program 函数测试
测试目标：验证 program 根节点处理时符号表初始化的正确性
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_program_src import _handle_program

# 类型别名（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleProgram(unittest.TestCase):
    """_handle_program 函数测试用例"""

    def test_handle_program_initializes_empty_symbol_table(self):
        """测试：空符号表初始化所有字段"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["errors"], [])
        self.assertEqual(symbol_table["current_function"], "")

    def test_handle_program_preserves_existing_variables(self):
        """测试：保留已存在的 variables 字段"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int", "scope": 0}}
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["variables"], {"x": {"type": "int", "scope": 0}})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["errors"], [])
        self.assertEqual(symbol_table["current_function"], "")

    def test_handle_program_preserves_existing_functions(self):
        """测试：保留已存在的 functions 字段"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "functions": {"main": {"params": [], "return_type": "int"}}
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {"main": {"params": [], "return_type": "int"}})
        self.assertEqual(symbol_table["errors"], [])
        self.assertEqual(symbol_table["current_function"], "")

    def test_handle_program_preserves_existing_errors(self):
        """测试：保留已存在的 errors 字段"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "errors": [{"message": "Previous error", "line": 10}]
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["errors"], [{"message": "Previous error", "line": 10}])
        self.assertEqual(symbol_table["current_function"], "")

    def test_handle_program_preserves_existing_current_function(self):
        """测试：保留已存在的 current_function 字段"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "current_function": "main"
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["errors"], [])
        self.assertEqual(symbol_table["current_function"], "main")

    def test_handle_program_overwrites_scope_stack_and_current_scope(self):
        """测试：即使已存在 scope_stack 和 current_scope 也会被覆盖"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "scope_stack": [1, 2, 3],
            "current_scope": 5
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_program_with_all_fields_present(self):
        """测试：所有字段已存在时的行为"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int"}},
            "functions": {"main": {"params": []}},
            "current_scope": 10,
            "scope_stack": [1, 2],
            "current_function": "helper",
            "errors": [{"msg": "error"}]
        }
        
        _handle_program(node, symbol_table)
        
        # scope_stack 和 current_scope 应被重置
        self.assertEqual(symbol_table["scope_stack"], [0])
        self.assertEqual(symbol_table["current_scope"], 0)
        # 其他字段应保持不变
        self.assertEqual(symbol_table["variables"], {"x": {"type": "int"}})
        self.assertEqual(symbol_table["functions"], {"main": {"params": []}})
        self.assertEqual(symbol_table["current_function"], "helper")
        self.assertEqual(symbol_table["errors"], [{"msg": "error"}])

    def test_handle_program_node_ignored(self):
        """测试：node 参数不影响符号表初始化（仅用于接口一致性）"""
        node1: AST = {"type": "program", "children": []}
        node2: AST = {"type": "program", "children": [{"type": "statement"}]}
        node3: AST = {"type": "program", "value": "test"}
        
        symbol_table1: SymbolTable = {}
        symbol_table2: SymbolTable = {}
        symbol_table3: SymbolTable = {}
        
        _handle_program(node1, symbol_table1)
        _handle_program(node2, symbol_table2)
        _handle_program(node3, symbol_table3)
        
        # 所有符号表应相同
        self.assertEqual(symbol_table1, symbol_table2)
        self.assertEqual(symbol_table2, symbol_table3)

    def test_handle_program_returns_none(self):
        """测试：函数返回 None（原地修改）"""
        node: AST = {"type": "program", "children": []}
        symbol_table: SymbolTable = {}
        
        result = _handle_program(node, symbol_table)
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
