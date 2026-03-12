import unittest
from unittest.mock import Mock, call
from typing import Dict, Any

# Import the function to test using relative import
from ._handle_block_src import _handle_block

# Type aliases
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """测试 _handle_block 函数的作用域管理和子节点遍历逻辑"""

    def test_handle_block_initializes_missing_scope_fields(self):
        """测试当 symbol_table 缺少作用域字段时会自动初始化"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {}  # 空符号表

        _handle_block(node, symbol_table)

        self.assertIn("scope_stack", symbol_table)
        self.assertIn("current_scope", symbol_table)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_block_enters_new_scope(self):
        """测试进入新作用域时 scope 递增"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}

        _handle_block(node, symbol_table)

        # 进入作用域后 scope 应该为 1
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [0])

    def test_handle_block_exits_scope_restores_previous(self):
        """测试退出作用域时恢复之前的 scope 值"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {"current_scope": 5, "scope_stack": []}

        _handle_block(node, symbol_table)

        # 退出后应该恢复为 5
        self.assertEqual(symbol_table["current_scope"], 5)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_with_children_calls_traverse_fn(self):
        """测试有子节点时调用 traverse_fn"""
        child1: AST = {"type": "var_decl", "value": "x"}
        child2: AST = {"type": "assignment", "value": "y"}
        node: AST = {"type": "block", "children": [child1, child2]}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}
        traverse_fn = Mock()

        _handle_block(node, symbol_table, traverse_fn)

        self.assertEqual(traverse_fn.call_count, 2)
        traverse_fn.assert_has_calls([
            call(child1, symbol_table),
            call(child2, symbol_table)
        ])

    def test_handle_block_no_children_no_traverse_fn(self):
        """测试没有子节点且无 traverse_fn 时不报错"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}

        # 应该不抛出异常
        _handle_block(node, symbol_table)

        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_traverse_fn_none(self):
        """测试 traverse_fn 为 None 时不处理子节点"""
        child1: AST = {"type": "var_decl", "value": "x"}
        node: AST = {"type": "block", "children": [child1]}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}

        _handle_block(node, symbol_table, traverse_fn=None)

        # scope 应该正常进出
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_nested_scopes(self):
        """测试嵌套作用域的正确性"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}

        # 第一次进入 block
        _handle_block(node, symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        # 第二次进入 block
        _handle_block(node, symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_preserves_other_symbol_table_fields(self):
        """测试不修改 symbol_table 的其他字段"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {
            "current_scope": 2,
            "scope_stack": [],
            "variables": {"x": {"type": "int"}},
            "functions": {"main": {"return_type": "int"}},
            "errors": []
        }

        _handle_block(node, symbol_table)

        self.assertEqual(symbol_table["variables"], {"x": {"type": "int"}})
        self.assertEqual(symbol_table["functions"], {"main": {"return_type": "int"}})
        self.assertEqual(symbol_table["errors"], [])

    def test_handle_block_scope_stack_operations(self):
        """测试作用域栈的 push/pop 操作"""
        node: AST = {"type": "block", "children": []}
        symbol_table: SymbolTable = {"current_scope": 3, "scope_stack": [1, 2]}

        _handle_block(node, symbol_table)

        # 退出后应该恢复到 2（栈顶）
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [1])

    def test_handle_block_children_missing_key(self):
        """测试节点没有 children 键时的处理"""
        node: AST = {"type": "block"}  # 没有 children 字段
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}
        traverse_fn = Mock()

        _handle_block(node, symbol_table, traverse_fn)

        # 不应该调用 traverse_fn
        traverse_fn.assert_not_called()
        # scope 应该正常进出
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_block_traverse_fn_receives_correct_symbol_table(self):
        """测试 traverse_fn 接收到的是同一个 symbol_table 引用"""
        child1: AST = {"type": "var_decl", "value": "x"}
        node: AST = {"type": "block", "children": [child1]}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}
        traverse_fn = Mock()

        _handle_block(node, symbol_table, traverse_fn)

        # 验证传入的是同一个 symbol_table 对象
        traverse_fn.assert_called_once()
        called_args = traverse_fn.call_args
        self.assertIs(called_args[0][1], symbol_table)

    def test_handle_block_scope_increment_during_children_processing(self):
        """测试在处理子节点期间 scope 保持递增状态"""
        child1: AST = {"type": "var_decl", "value": "x"}
        node: AST = {"type": "block", "children": [child1]}
        symbol_table: SymbolTable = {"current_scope": 0, "scope_stack": []}

        def check_scope_during_traversal(n: AST, st: SymbolTable):
            # 在遍历子节点时，scope 应该为 1（已进入新作用域）
            self.assertEqual(st["current_scope"], 1)

        _handle_block(node, symbol_table, check_scope_during_traversal)

        # 退出后恢复
        self.assertEqual(symbol_table["current_scope"], 0)


if __name__ == "__main__":
    unittest.main()
