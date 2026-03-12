# -*- coding: utf-8 -*-
"""单元测试文件：_handle_program 函数测试"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._handle_program_src import _handle_program

# 类型别名
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleProgram(unittest.TestCase):
    """_handle_program 函数的单元测试类"""

    def test_handle_program_initializes_symbol_table(self):
        """测试：program 节点处理正确初始化符号表"""
        node: AST = {
            "type": "program",
            "children": []
        }
        symbol_table: SymbolTable = {}
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_program_preserves_existing_symbol_table_fields(self):
        """测试：保留符号表中已存在的字段"""
        node: AST = {
            "type": "program",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {"existing_var": {"data_type": "int"}},
            "functions": {"existing_func": {"return_type": "int"}}
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["variables"], {"existing_var": {"data_type": "int"}})
        self.assertEqual(symbol_table["functions"], {"existing_func": {"return_type": "int"}})
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_program_with_children_calls_traverse_node(self):
        """测试：有子节点时正确调用 _traverse_node"""
        node: AST = {
            "type": "program",
            "children": [
                {"type": "function_declaration", "value": "func1"},
                {"type": "function_declaration", "value": "func2"}
            ]
        }
        symbol_table: SymbolTable = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_program_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_program(node, symbol_table)
            
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call({"type": "function_declaration", "value": "func1"}, symbol_table)
            mock_traverse.assert_any_call({"type": "function_declaration", "value": "func2"}, symbol_table)

    def test_handle_program_without_children_does_not_call_traverse_node(self):
        """测试：无子节点时不调用 _traverse_node"""
        node: AST = {
            "type": "program",
            "children": []
        }
        symbol_table: SymbolTable = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_program_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_program(node, symbol_table)
            
            mock_traverse.assert_not_called()

    def test_handle_program_without_children_key_does_not_call_traverse_node(self):
        """测试：没有 children 键时不调用 _traverse_node"""
        node: AST = {
            "type": "program"
        }
        symbol_table: SymbolTable = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_program_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_program(node, symbol_table)
            
            mock_traverse.assert_not_called()

    def test_handle_program_with_none_children_does_not_call_traverse_node(self):
        """测试：children 为 None 时不调用 _traverse_node"""
        node: AST = {
            "type": "program",
            "children": None
        }
        symbol_table: SymbolTable = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_program_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_program(node, symbol_table)
            
            mock_traverse.assert_not_called()

    def test_handle_program_initializes_only_missing_fields(self):
        """测试：仅初始化符号表中缺失的字段"""
        node: AST = {
            "type": "program",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": ["pre-existing error"]
        }
        
        _handle_program(node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["variables"], {})
        self.assertIn("functions", symbol_table)
        self.assertEqual(symbol_table["errors"], ["pre-existing error"])


if __name__ == "__main__":
    unittest.main()
