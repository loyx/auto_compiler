# -*- coding: utf-8 -*-
"""
单元测试文件：_traverse_node 函数测试
测试 AST 节点遍历器的分发逻辑
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any


# === 类型定义（与源文件一致）===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# 模块基础路径
MODULE_BASE = 'main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package'


# === 测试类 ===
class TestTraverseNode(unittest.TestCase):
    """测试 _traverse_node 函数的分发逻辑"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def _create_all_mocks(self, target_mock=None):
        """创建所有 handler 的 mock，返回 mock 字典和目标 mock"""
        mocks = {}
        handlers = [
            '_handle_program',
            '_handle_function_declaration',
            '_handle_function_call',
            '_handle_return_statement',
            '_handle_assignment',
            '_handle_expression',
            '_handle_identifier',
            '_handle_literal',
            '_handle_block',
            '_handle_if_statement',
            '_handle_while_loop',
            '_handle_variable_declaration',
        ]
        for handler in handlers:
            if handler == target_mock:
                mocks[handler] = MagicMock()
            else:
                mocks[handler] = MagicMock()
        return mocks

    # ========== 测试各节点类型的分发 ==========

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_program_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 program 类型节点正确分发到 _handle_program"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "program",
            "children": [
                {"type": "function_declaration", "value": "main"}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_program.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_function_declaration_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 function_declaration 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "function_declaration",
            "value": "main",
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_func_decl.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_function_call_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 function_call 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "function_call",
            "value": "printf",
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_func_call.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_return_statement_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 return_statement 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "return_statement",
            "children": [
                {"type": "literal", "value": 0, "data_type": "int"}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_return.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_assignment_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 assignment 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x"},
                {"type": "literal", "value": 5, "data_type": "int"}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_assign.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_expression_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 expression 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "identifier", "value": "a"},
                {"type": "identifier", "value": "b"}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_expr.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_identifier_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 identifier 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "identifier",
            "value": "x",
            "line": 5,
            "column": 10
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_ident.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_literal_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 literal 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_literal.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_block_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 block 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "block",
            "children": [
                {"type": "assignment", "children": []}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_block.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_if_statement_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 if_statement 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "value": ">", "children": []},
                {"type": "block", "children": []}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_if.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_while_loop_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 while_loop 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "while_loop",
            "children": [
                {"type": "expression", "value": "<", "children": []},
                {"type": "block", "children": []}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_while.assert_called_once_with(node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_dispatch_variable_declaration_node(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 variable_declaration 类型节点正确分发"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 3,
            "column": 5
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_var_decl.assert_called_once_with(node, self.symbol_table)

    # ========== 测试未知节点类型 ==========

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_unknown_node_type_records_warning(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试未知节点类型会记录警告"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "unknown_type",
            "line": 10,
            "column": 20
        }
        
        _traverse_node(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Warning: Unknown node type 'unknown_type'", self.symbol_table["errors"][0])
        self.assertIn("line 10", self.symbol_table["errors"][0])
        self.assertIn("column 20", self.symbol_table["errors"][0])

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_unknown_node_type_with_missing_location(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试未知节点类型缺少位置信息时使用默认值"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "another_unknown"
        }
        
        _traverse_node(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("line ?", self.symbol_table["errors"][0])
        self.assertIn("column ?", self.symbol_table["errors"][0])

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_unknown_node_type_without_errors_list(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试符号表没有 errors 字段时的处理"""
        from ._traverse_node_src import _traverse_node
        
        symbol_table_no_errors: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        
        node: AST = {
            "type": "unknown_type"
        }
        
        # 不应该抛出异常
        _traverse_node(node, symbol_table_no_errors)
        
        # errors 列表应该被创建
        self.assertIn("errors", symbol_table_no_errors)

    # ========== 测试子节点递归遍历 ==========

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_recursion_for_assignment_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 assignment 类型会递归遍历子节点"""
        from ._traverse_node_src import _traverse_node
        
        child_node: AST = {"type": "identifier", "value": "x"}
        parent_node: AST = {
            "type": "assignment",
            "children": [child_node]
        }
        
        _traverse_node(parent_node, self.symbol_table)
        
        # handler 被调用一次（处理父节点）
        mock_assign.assert_called_once()

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_no_recursion_for_program_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 program 类型不会在 handler 后递归遍历子节点"""
        from ._traverse_node_src import _traverse_node
        
        child_node: AST = {"type": "function_declaration", "value": "main"}
        parent_node: AST = {
            "type": "program",
            "children": [child_node]
        }
        
        _traverse_node(parent_node, self.symbol_table)
        
        mock_program.assert_called_once_with(parent_node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_no_recursion_for_block_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 block 类型不会在 handler 后递归遍历子节点"""
        from ._traverse_node_src import _traverse_node
        
        parent_node: AST = {
            "type": "block",
            "children": [{"type": "assignment", "children": []}]
        }
        
        _traverse_node(parent_node, self.symbol_table)
        
        mock_block.assert_called_once_with(parent_node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_no_recursion_for_if_statement_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 if_statement 类型不会在 handler 后递归遍历子节点"""
        from ._traverse_node_src import _traverse_node
        
        parent_node: AST = {
            "type": "if_statement",
            "children": []
        }
        
        _traverse_node(parent_node, self.symbol_table)
        
        mock_if.assert_called_once_with(parent_node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_no_recursion_for_while_loop_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 while_loop 类型不会在 handler 后递归遍历子节点"""
        from ._traverse_node_src import _traverse_node
        
        parent_node: AST = {
            "type": "while_loop",
            "children": []
        }
        
        _traverse_node(parent_node, self.symbol_table)
        
        mock_while.assert_called_once_with(parent_node, self.symbol_table)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_no_recursion_for_function_declaration_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试 function_declaration 类型不会在 handler 后递归遍历子节点"""
        from ._traverse_node_src import _traverse_node
        
        parent_node: AST = {
            "type": "function_declaration",
            "value": "main",
            "children": []
        }
        
        _traverse_node(parent_node, self.symbol_table)
        
        mock_func_decl.assert_called_once_with(parent_node, self.symbol_table)

    # ========== 边界情况测试 ==========

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_node_without_type_field(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试节点没有 type 字段时的处理"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "value": "test"
        }
        
        _traverse_node(node, self.symbol_table)
        
        # 空字符串 type 不会匹配任何 handler
        mock_literal.assert_not_called()
        # 应该记录未知类型警告
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_node_with_empty_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试节点有空的 children 列表"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "literal",
            "value": 42,
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_literal.assert_called_once()

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_node_without_children_field(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试节点没有 children 字段"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "literal",
            "value": 42
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_literal.assert_called_once()

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_node_with_none_children(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试节点 children 为 None"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "assignment",
            "children": None
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_assign.assert_called_once()

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_multiple_children_recursion(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试有多个子节点时的递归"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "identifier", "value": "a"},
                {"type": "identifier", "value": "b"},
                {"type": "identifier", "value": "c"}
            ]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_expr.assert_called_once()

    # ========== 符号表状态测试 ==========

    @patch(f"{MODULE_BASE}._handle_program_package._handle_program_src._handle_program")
    @patch(f"{MODULE_BASE}._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration")
    @patch(f"{MODULE_BASE}._handle_function_call_package._handle_function_call_src._handle_function_call")
    @patch(f"{MODULE_BASE}._handle_return_statement_package._handle_return_statement_src._handle_return_statement")
    @patch(f"{MODULE_BASE}._handle_assignment_package._handle_assignment_src._handle_assignment")
    @patch(f"{MODULE_BASE}._handle_expression_package._handle_expression_src._handle_expression")
    @patch(f"{MODULE_BASE}._handle_identifier_package._handle_identifier_src._handle_identifier")
    @patch(f"{MODULE_BASE}._handle_literal_package._handle_literal_src._handle_literal")
    @patch(f"{MODULE_BASE}._handle_block_package._handle_block_src._handle_block")
    @patch(f"{MODULE_BASE}._handle_if_statement_package._handle_if_statement_src._handle_if_statement")
    @patch(f"{MODULE_BASE}._handle_while_loop_package._handle_while_loop_src._handle_while_loop")
    @patch(f"{MODULE_BASE}._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration")
    def test_symbol_table_passed_to_handler(self, mock_var_decl, mock_while, mock_if, mock_block, mock_literal, mock_ident, mock_expr, mock_assign, mock_return, mock_func_call, mock_func_decl, mock_program):
        """测试符号表正确传递给 handler"""
        from ._traverse_node_src import _traverse_node
        
        node: AST = {
            "type": "identifier",
            "value": "test"
        }
        
        custom_symbol_table: SymbolTable = {
            "variables": {"test": {"data_type": "int"}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0],
            "errors": []
        }
        
        _traverse_node(node, custom_symbol_table)
        
        # 验证 handler 收到的是同一个符号表对象
        _, passed_symbol_table = mock_ident.call_args
        self.assertIs(passed_symbol_table, custom_symbol_table)


# ========== 运行测试 ==========
if __name__ == "__main__":
    unittest.main()