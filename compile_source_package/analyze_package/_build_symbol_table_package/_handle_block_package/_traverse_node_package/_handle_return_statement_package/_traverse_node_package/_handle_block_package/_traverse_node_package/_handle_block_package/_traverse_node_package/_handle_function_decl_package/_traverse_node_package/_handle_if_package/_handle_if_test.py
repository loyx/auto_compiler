# -*- coding: utf-8 -*-
"""单元测试文件：_handle_if 函数测试"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测模块
from ._handle_if_src import _handle_if

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIf(unittest.TestCase):
    """_handle_if 函数测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.mock_traverse_node_patcher = patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_if_package._traverse_node_package._traverse_node_src._traverse_node"
        )
        self.mock_traverse_node = self.mock_traverse_node_patcher.start()

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        self.mock_traverse_node_patcher.stop()

    def test_handle_if_with_two_children(self) -> None:
        """测试 if 语句有两个子节点（条件表达式和 then 块）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "expression", "value": "x > 0"},
                {"type": "block", "children": []}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        _handle_if(node, symbol_table)

        # 验证 scope 管理：进入时 +1，退出时恢复
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 被调用了 2 次
        self.assertEqual(self.mock_traverse_node.call_count, 2)

        # 验证调用参数
        calls = self.mock_traverse_node.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "expression")
        self.assertEqual(calls[1][0][0]["type"], "block")

        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_if_with_three_children(self) -> None:
        """测试 if 语句有三个子节点（条件表达式、then 块和 else 块）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "expression", "value": "x > 0"},
                {"type": "block", "children": []},
                {"type": "block", "children": []}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [],
            "errors": []
        }

        _handle_if(node, symbol_table)

        # 验证 scope 管理
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 被调用了 3 次
        self.assertEqual(self.mock_traverse_node.call_count, 3)

        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_if_with_one_child(self) -> None:
        """测试 if 语句只有一个子节点（应记录错误）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "expression", "value": "x > 0"}
            ],
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        _handle_if(node, symbol_table)

        # 验证 scope 仍然正确恢复
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 被调用了 1 次（只处理存在的子节点）
        self.assertEqual(self.mock_traverse_node.call_count, 1)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "if 语句缺少子节点")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertEqual(error["node_type"], "if")

    def test_handle_if_with_no_children(self) -> None:
        """测试 if 语句没有子节点（应记录错误）"""
        node: AST = {
            "type": "if",
            "children": [],
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 3,
            "scope_stack": [],
            "errors": []
        }

        _handle_if(node, symbol_table)

        # 验证 scope 仍然正确恢复
        self.assertEqual(symbol_table["current_scope"], 3)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 没有被调用
        self.assertEqual(self.mock_traverse_node.call_count, 0)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "if 语句缺少子节点")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 3)

    def test_handle_if_with_missing_children_key(self) -> None:
        """测试 if 语句节点缺少 children 键（应记录错误）"""
        node: AST = {
            "type": "if",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        _handle_if(node, symbol_table)

        # 验证 scope 仍然正确恢复
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 验证 _traverse_node 没有被调用
        self.assertEqual(self.mock_traverse_node.call_count, 0)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "if 语句缺少子节点")
        self.assertEqual(error["line"], 25)
        self.assertEqual(error["column"], 10)

    def test_handle_if_scope_stack_management(self) -> None:
        """测试 if 语句的作用域栈管理（嵌套场景）"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "expression", "value": "x > 0"},
                {"type": "block", "children": []}
            ],
            "line": 30,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [1],  # 已有作用域栈
            "errors": []
        }

        _handle_if(node, symbol_table)

        # 验证 scope 恢复到进入前的值
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [1])

        # 验证 _traverse_node 被调用了 2 次
        self.assertEqual(self.mock_traverse_node.call_count, 2)

        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_if_initializes_scope_stack_if_missing(self) -> None:
        """测试 if 语句在 symbol_table 缺少 scope_stack 时自动初始化"""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "expression", "value": "x > 0"},
                {"type": "block", "children": []}
            ],
            "line": 35,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
            # 没有 scope_stack
        }

        _handle_if(node, symbol_table)

        # 验证 scope_stack 被创建并正确管理
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_if_initializes_errors_if_missing(self) -> None:
        """测试 if 语句在 symbol_table 缺少 errors 时自动初始化"""
        node: AST = {
            "type": "if",
            "children": [],
            "line": 40,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
            # 没有 errors
        }

        _handle_if(node, symbol_table)

        # 验证 errors 被创建并记录了错误
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "if 语句缺少子节点")

    def test_handle_if_preserves_existing_errors(self) -> None:
        """测试 if 语句保留已有的错误记录"""
        node: AST = {
            "type": "if",
            "children": [],
            "line": 45,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": [
                {"message": "之前的错误", "line": 1, "column": 1, "node_type": "test"}
            ]
        }

        _handle_if(node, symbol_table)

        # 验证保留了已有错误并添加了新错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "之前的错误")
        self.assertEqual(symbol_table["errors"][1]["message"], "if 语句缺少子节点")


if __name__ == "__main__":
    unittest.main()
