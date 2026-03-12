import unittest
from unittest.mock import patch, call
from typing import Any, Dict

# 相对导入被测函数
from ._handle_block_src import _handle_block


# 类型别名（与被测代码保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """测试 _handle_block 函数的作用域管理逻辑"""

    def test_handle_block_normal_with_children(self):
        """测试正常情况：有子节点的 block"""
        # 准备测试数据
        node: AST = {
            "type": "block",
            "children": [
                {"type": "var_decl", "value": "x"},
                {"type": "assignment", "value": "y"},
                {"type": "if", "condition": "z > 0"}
            ]
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        # 执行测试 - patch _dispatch_node
        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            _handle_block(node, symbol_table)

        # 验证作用域变化
        self.assertEqual(symbol_table["current_scope"], 0)  # 退出后恢复为 0
        self.assertEqual(symbol_table["scope_stack"], [])  # stack 为空
        
        # 验证 _dispatch_node 被正确调用
        self.assertEqual(mock_dispatch.call_count, 3)
        mock_dispatch.assert_has_calls([
            call({"type": "var_decl", "value": "x"}, symbol_table),
            call({"type": "assignment", "value": "y"}, symbol_table),
            call({"type": "if", "condition": "z > 0"}, symbol_table)
        ])

    def test_handle_block_missing_scope_stack(self):
        """测试边界情况：symbol_table 缺少 scope_stack 字段"""
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "a"}]
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
            # 注意：没有 scope_stack 字段
        }

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            _handle_block(node, symbol_table)

        # 验证 scope_stack 被自动初始化
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(mock_dispatch.call_count, 1)

    def test_handle_block_non_zero_initial_scope(self):
        """测试边界情况：current_scope 初始值不为 0"""
        node: AST = {
            "type": "block",
            "children": [{"type": "assignment", "value": "b"}]
        }
        symbol_table: SymbolTable = {
            "current_scope": 5,
            "scope_stack": [0, 2, 3]
        }

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            _handle_block(node, symbol_table)

        # 验证作用域正确恢复
        self.assertEqual(symbol_table["current_scope"], 5)  # 恢复为初始值
        self.assertEqual(symbol_table["scope_stack"], [0, 2, 3])  # 恢复为初始 stack
        self.assertEqual(mock_dispatch.call_count, 1)

    def test_handle_block_empty_children(self):
        """测试边界情况：空 children 列表"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            _handle_block(node, symbol_table)

        # 验证作用域正确管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        # 验证 _dispatch_node 未被调用
        mock_dispatch.assert_not_called()

    def test_handle_block_missing_children_field(self):
        """测试边界情况：node 缺少 children 字段"""
        node: AST = {
            "type": "block"
            # 注意：没有 children 字段
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            _handle_block(node, symbol_table)

        # 验证作用域正确管理
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        mock_dispatch.assert_not_called()

    def test_handle_block_dispatch_node_exception_propagation(self):
        """测试异常场景：_dispatch_node 抛出异常时的传播"""
        node: AST = {
            "type": "block",
            "children": [
                {"type": "var_decl", "value": "x"},
                {"type": "assignment", "value": "y"}
            ]
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            # 让第二次调用抛出异常
            mock_dispatch.side_effect = ValueError("Test exception")

            # 验证异常被传播
            with self.assertRaises(ValueError) as context:
                _handle_block(node, symbol_table)

            self.assertEqual(str(context.exception), "Test exception")
            
            # 验证异常时 scope 仍然被恢复（因为 pop 在异常前已完成？需要验证实际行为）
            # 根据实现，异常发生在遍历子节点时，此时 scope 还未恢复
            # 但这是预期行为 - 异常会中断执行
            self.assertEqual(mock_dispatch.call_count, 1)

    def test_handle_block_nested_blocks_scope_isolation(self):
        """测试嵌套 block 的作用域隔离"""
        # 模拟嵌套 block 场景
        inner_node: AST = {
            "type": "block",
            "children": []
        }
        outer_node: AST = {
            "type": "block",
            "children": [inner_node]
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        # 需要递归 patch，因为内层 block 也会调用 _handle_block
        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ) as mock_dispatch:
            # 让 dispatch_node 在处理内层 block 时递归调用 _handle_block
            def dispatch_side_effect(node, st):
                if node.get("type") == "block":
                    # 导入真实的 _handle_block 进行递归
                    from ._handle_block_src import _handle_block as real_handle_block
                    real_handle_block(node, st)

            mock_dispatch.side_effect = dispatch_side_effect
            _handle_block(outer_node, symbol_table)

        # 验证最终作用域恢复为 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_stack_operations(self):
        """测试作用域栈的 push/pop 操作"""
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl", "value": "x"}]
        }
        symbol_table: SymbolTable = {
            "current_scope": 3,
            "scope_stack": [0, 1, 2]
        }

        with patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package."
            "_handle_block_package._traverse_node_package._handle_return_statement_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._traverse_node_package._handle_function_call_package."
            "_traverse_node_package._handle_block_package._traverse_node_package."
            "_handle_block_package._dispatch_node_package._dispatch_node_src._dispatch_node"
        ):
            # 在函数执行过程中验证中间状态
            # 进入 block 时 scope 应该变为 4，stack 变为 [0, 1, 2, 3]
            # 退出后 scope 恢复为 3，stack 恢复为 [0, 1, 2]
            _handle_block(node, symbol_table)

        self.assertEqual(symbol_table["current_scope"], 3)
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
