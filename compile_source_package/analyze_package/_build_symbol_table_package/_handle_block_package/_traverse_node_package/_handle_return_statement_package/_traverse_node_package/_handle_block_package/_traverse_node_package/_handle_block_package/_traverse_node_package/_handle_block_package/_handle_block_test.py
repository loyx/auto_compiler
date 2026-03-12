# -*- coding: utf-8 -*-
"""单元测试文件：_handle_block 函数测试"""

import unittest
from unittest.mock import patch, call
from typing import Any, Dict

# 相对导入被测函数
from ._handle_block_src import _handle_block

# 类型别名（与被测代码保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """_handle_block 函数测试用例"""

    def setUp(self) -> None:
        """测试前准备"""
        pass

    def tearDown(self) -> None:
        """测试后清理"""
        pass

    def test_handle_block_empty_children(self) -> None:
        """测试空块（无子节点）的情况"""
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

        # 验证作用域正确进入和退出
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_with_children(self) -> None:
        """测试包含子节点的块"""
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

        with patch("._traverse_node._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # 验证 _traverse_node 被调用两次
            self.assertEqual(mock_traverse.call_count, 2)
            # 验证调用参数
            mock_traverse.assert_any_call(child1, symbol_table)
            mock_traverse.assert_any_call(child2, symbol_table)

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_enter_exit(self) -> None:
        """测试作用域进入和退出的正确性"""
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "x", "line": 2, "column": 5}],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [0, 1]
        }

        with patch("._traverse_node._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证作用域正确恢复为进入前的值
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [0, 1])

    def test_handle_block_initializes_missing_fields(self) -> None:
        """测试当 symbol_table 缺少必要字段时的初始化"""
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

        with patch("._traverse_node._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证字段被正确初始化
        self.assertIn("current_scope", symbol_table)
        self.assertIn("scope_stack", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_block_scope_increment(self) -> None:
        """测试作用域层级正确递增"""
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

        # 在 _traverse_node 调用期间验证作用域已递增
        def check_scope_during_traverse(node_arg: AST, sym_table: SymbolTable) -> None:
            self.assertEqual(sym_table["current_scope"], 1)
            self.assertEqual(sym_table["scope_stack"], [0])

        with patch("._traverse_node._traverse_node", side_effect=check_scope_during_traverse):
            _handle_block(node, symbol_table)

        # 验证最终作用域已恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_nested_blocks(self) -> None:
        """测试嵌套块的作用域管理"""
        inner_child: AST = {"type": "var_decl", "value": "y", "line": 3, "column": 9}
        inner_block: AST = {
            "type": "block",
            "children": [inner_child],
            "line": 2,
            "column": 5
        }
        
        node: AST = {
            "type": "block",
            "children": [inner_block],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node._traverse_node") as mock_traverse:
            # 模拟 _traverse_node 遇到 block 类型时递归调用 _handle_block
            def traverse_side_effect(node_arg: AST, sym_table: SymbolTable) -> None:
                if node_arg.get("type") == "block":
                    _handle_block(node_arg, sym_table)

            mock_traverse.side_effect = traverse_side_effect
            _handle_block(node, symbol_table)

        # 验证最终作用域恢复到初始状态
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_error_handling(self) -> None:
        """测试错误处理：即使子节点处理出错也要恢复作用域"""
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "x", "line": 2, "column": 5}],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node._traverse_node", side_effect=Exception("Test error")):
            try:
                _handle_block(node, symbol_table)
            except Exception:
                pass  # 预期会抛出异常

        # 验证即使有异常，作用域也应该恢复（finally 块执行）
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_missing_children_field(self) -> None:
        """测试节点缺少 children 字段的情况"""
        node: AST = {
            "type": "block",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # 验证 _traverse_node 未被调用（因为没有 children）
            mock_traverse.assert_not_called()

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_multiple_statements(self) -> None:
        """测试块内多个语句的处理顺序"""
        children = [
            {"type": "var_decl", "value": "x", "line": 2, "column": 5},
            {"type": "assignment", "value": "x", "line": 3, "column": 5},
            {"type": "if", "line": 4, "column": 5},
        ]
        
        node: AST = {
            "type": "block",
            "children": children,
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._traverse_node._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # 验证调用顺序
            calls = [call(child, symbol_table) for child in children]
            mock_traverse.assert_has_calls(calls, any_order=False)

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_preserves_other_fields(self) -> None:
        """测试处理块时不修改 symbol_table 的其他字段"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": "main",
            "custom_field": "custom_value"
        }

        with patch("._traverse_node._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证其他字段未被修改
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "int")
        self.assertEqual(symbol_table["current_function"], "main")
        self.assertEqual(symbol_table["custom_field"], "custom_value")


if __name__ == "__main__":
    unittest.main()
