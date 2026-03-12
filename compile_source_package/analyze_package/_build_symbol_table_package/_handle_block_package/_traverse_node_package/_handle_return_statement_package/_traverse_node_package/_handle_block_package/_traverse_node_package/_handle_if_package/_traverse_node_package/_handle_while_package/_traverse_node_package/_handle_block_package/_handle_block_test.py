# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_block 函数测试
测试 block 类型节点的处理逻辑，包括作用域管理和子节点遍历
"""

from typing import Any, Dict
from unittest.mock import patch

from ._handle_block_src import _handle_block


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock:
    """_handle_block 函数测试类"""

    def test_handle_block_normal_with_children(self):
        """测试正常情况：block 包含多个子节点"""
        node: AST = {
            "type": "block",
            "children": [
                {"type": "var_decl", "value": "x"},
                {"type": "assignment", "value": "y"},
                {"type": "function_call", "value": "print"}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域变化：进入时 +1，退出时恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

        # 验证 _traverse_node 被调用 3 次（每个子节点一次）
        assert mock_traverse.call_count == 3

        # 验证调用参数
        calls = mock_traverse.call_args_list
        assert calls[0][0][0]["type"] == "var_decl"
        assert calls[1][0][0]["type"] == "assignment"
        assert calls[2][0][0]["type"] == "function_call"

    def test_handle_block_empty_children(self):
        """测试边界情况：block 没有子节点"""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 5,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

        # 验证作用域变化：进入时 +1（从 1 到 2），退出时恢复为 1
        assert symbol_table["current_scope"] == 1
        assert symbol_table["scope_stack"] == []

        # 验证 _traverse_node 没有被调用
        assert mock_traverse.call_count == 0

    def test_handle_block_initializes_missing_fields(self):
        """测试初始化：symbol_table 缺少必要字段时自动初始化"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {}

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证字段被初始化
        assert "current_scope" in symbol_table
        assert symbol_table["current_scope"] == 0
        assert "scope_stack" in symbol_table
        assert symbol_table["scope_stack"] == []
        assert "errors" in symbol_table
        assert symbol_table["errors"] == []

    def test_handle_block_nested_scope_simulation(self):
        """测试作用域嵌套：模拟多层 block 嵌套"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [0, 1]
        }

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证作用域变化：从 2 提升到 3，然后恢复为 2
        assert symbol_table["current_scope"] == 2
        assert symbol_table["scope_stack"] == [0, 1]

    def test_handle_block_empty_stack_on_exit(self):
        """测试边界情况：退出 block 时 scope_stack 为空"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证作用域恢复为 0（即使栈为空）
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_handle_block_preserves_other_fields(self):
        """测试副作用：不修改 symbol_table 的其他字段"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 1,
            "scope_stack": [0],
            "current_function": "main",
            "custom_field": "custom_value"
        }

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证其他字段保持不变
        assert symbol_table["variables"]["x"]["data_type"] == "int"
        assert symbol_table["functions"]["main"]["return_type"] == "int"
        assert symbol_table["current_function"] == "main"
        assert symbol_table["custom_field"] == "custom_value"

    def test_handle_block_scope_intermediate_state(self):
        """测试中间状态：在遍历子节点时作用域处于提升状态"""
        node: AST = {
            "type": "block",
            "children": [{"type": "var_decl"}]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # 自定义 mock，在调用时检查中间状态
        def check_scope_during_call(child, st):
            # 在 _traverse_node 被调用时，scope 应该是提升后的值
            assert st["current_scope"] == 1
            assert st["scope_stack"] == [0]

        with patch("._handle_block_src._traverse_node", side_effect=check_scope_during_call):
            _handle_block(node, symbol_table)

        # 验证最终状态
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_handle_block_no_line_column(self):
        """测试边界情况：node 没有 line/column 字段"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node"):
            # 不应该抛出异常
            _handle_block(node, symbol_table)

        assert symbol_table["current_scope"] == 0

    def test_handle_block_multiple_sequential_calls(self):
        """测试多次调用：连续处理多个 block"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node"):
            # 第一次调用
            _handle_block(node, symbol_table)
            assert symbol_table["current_scope"] == 0
            assert symbol_table["scope_stack"] == []

            # 第二次调用
            _handle_block(node, symbol_table)
            assert symbol_table["current_scope"] == 0
            assert symbol_table["scope_stack"] == []

            # 第三次调用
            _handle_block(node, symbol_table)
            assert symbol_table["current_scope"] == 0
            assert symbol_table["scope_stack"] == []

    def test_handle_block_with_errors_field(self):
        """测试 errors 字段：验证 errors 字段被正确初始化"""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node"):
            _handle_block(node, symbol_table)

        # 验证 errors 字段被初始化且为空列表
        assert "errors" in symbol_table
        assert isinstance(symbol_table["errors"], list)
        assert len(symbol_table["errors"]) == 0
