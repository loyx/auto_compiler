# -*- coding: utf-8 -*-
"""
单元测试：_handle_block 函数
测试 block 类型节点的作用域管理逻辑
"""

import unittest
from unittest.mock import patch, call
from typing import Any, Dict

# 相对导入被测模块
from ._handle_block_src import _handle_block

# ADT 类型定义（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """_handle_block 函数测试类"""

    def setUp(self):
        """测试前准备"""
        pass

    def tearDown(self):
        """测试后清理"""
        pass

    def test_handle_block_empty_block(self):
        """测试空 block 节点（无子节点）"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        _handle_block(node, symbol_table)

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_with_children(self):
        """测试带子节点的 block"""
        child1: AST = {"type": "var_decl", "value": "x", "line": 2, "column": 5}
        child2: AST = {"type": "assignment", "value": "y", "line": 3, "column": 5}
        node: AST = {
            "type": "block",
            "children": [child1, child2],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_while_package._traverse_node_package._handle_block_package._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # 验证 _traverse_node 被调用 2 次
            self.assertEqual(mock_traverse.call_count, 2)
            # 验证调用参数
            mock_traverse.assert_has_calls([
                call(child1, symbol_table),
                call(child2, symbol_table)
            ])

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_increment(self):
        """测试作用域层级递增"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": []
        }

        # 在 block 处理过程中，current_scope 应该先增加到 6
        # 我们需要 mock _traverse_node 来捕获中间状态
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_while_package._traverse_node_package._handle_block_package._handle_block_src._traverse_node") as mock_traverse:
            def capture_scope(child_node, sym_table):
                # 在遍历过程中捕获作用域状态
                self.assertEqual(sym_table["current_scope"], 6)

            mock_traverse.side_effect = capture_scope
            _handle_block(node, symbol_table)

        # 验证作用域最终恢复
        self.assertEqual(symbol_table["current_scope"], 5)

    def test_handle_block_scope_stack_operation(self):
        """测试作用域栈操作"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 3,
            "scope_stack": [0, 1, 2]
        }

        _handle_block(node, symbol_table)

        # 验证 scope_stack 先 push 再 pop，最终恢复原状
        self.assertEqual(symbol_table["current_scope"], 3)
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2])

    def test_handle_block_no_initial_scope_stack(self):
        """测试符号表没有初始 scope_stack 的情况"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }

        _handle_block(node, symbol_table)

        # 验证自动创建了 scope_stack
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_no_initial_current_scope(self):
        """测试符号表没有初始 current_scope 的情况"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {}
        }

        _handle_block(node, symbol_table)

        # 验证默认 current_scope 为 0，处理后恢复为 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_nested_blocks(self):
        """测试嵌套 block 的作用域管理"""
        inner_child: AST = {"type": "var_decl", "value": "x", "line": 2, "column": 5}
        inner_node: AST = {
            "type": "block",
            "children": [inner_child],
            "line": 1,
            "column": 1
        }
        outer_node: AST = {
            "type": "block",
            "children": [inner_node],
            "line": 0,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_while_package._traverse_node_package._handle_block_package._handle_block_src._traverse_node") as mock_traverse:
            # 当遍历到 inner_node 时，递归调用 _handle_block
            def traverse_side_effect(child_node, sym_table):
                if child_node["type"] == "block":
                    # 递归处理嵌套 block
                    from ._handle_block_src import _handle_block
                    _handle_block(child_node, sym_table)

            mock_traverse.side_effect = traverse_side_effect
            _handle_block(outer_node, symbol_table)

        # 验证嵌套 block 处理后作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_preserves_other_symbol_table_fields(self):
        """测试不修改符号表的其他字段"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        original_variables = {"x": {"data_type": "int", "is_declared": True}}
        original_functions = {"main": {"return_type": "int"}}
        original_current_function = "main"
        original_errors = []

        symbol_table: SymbolTable = {
            "variables": original_variables,
            "functions": original_functions,
            "current_scope": 0,
            "scope_stack": [],
            "current_function": original_current_function,
            "errors": original_errors
        }

        _handle_block(node, symbol_table)

        # 验证其他字段未被修改
        self.assertEqual(symbol_table["variables"], original_variables)
        self.assertEqual(symbol_table["functions"], original_functions)
        self.assertEqual(symbol_table["current_function"], original_current_function)
        self.assertEqual(symbol_table["errors"], original_errors)

    def test_handle_block_multiple_children_order(self):
        """测试多个子节点按顺序遍历"""
        children = [
            {"type": "var_decl", "value": "a", "line": 1, "column": 1},
            {"type": "var_decl", "value": "b", "line": 2, "column": 1},
            {"type": "var_decl", "value": "c", "line": 3, "column": 1},
        ]
        node: AST = {
            "type": "block",
            "children": children,
            "line": 0,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_while_package._traverse_node_package._handle_block_package._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # 验证调用顺序与 children 顺序一致
            expected_calls = [call(child, symbol_table) for child in children]
            mock_traverse.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
