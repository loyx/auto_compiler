# === std / third-party imports ===
from typing import Any, Dict
from unittest.mock import patch

# === relative imports ===
from ._handle_block_src import _handle_block

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


def test_handle_block_empty_block():
    """测试空块：没有子节点"""
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
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


def test_handle_block_with_children():
    """测试有子节点的块"""
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
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        _handle_block(node, symbol_table)
    
    # 验证 _traverse_node 被调用两次
    assert mock_traverse.call_count == 2
    mock_traverse.assert_any_call(child1, symbol_table)
    mock_traverse.assert_any_call(child2, symbol_table)
    
    # 验证作用域正确恢复
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


def test_handle_block_scope_management():
    """测试作用域管理：进入和退出作用域"""
    node: AST = {
        "type": "block",
        "children": [],
        "line": 1,
        "column": 1
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "functions": {},
        "current_scope": 2,
        "scope_stack": [0, 1]
    }
    
    _handle_block(node, symbol_table)
    
    # 验证作用域栈和 current_scope 的变化
    assert symbol_table["current_scope"] == 2
    assert symbol_table["scope_stack"] == [0, 1]


def test_handle_block_nested_scope():
    """测试嵌套作用域"""
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
    
    # 第一次进入块
    _handle_block(node, symbol_table)
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []
    
    # 再次进入块（模拟嵌套）
    _handle_block(node, symbol_table)
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


def test_handle_block_scope_stack_initialization():
    """测试 symbol_table 没有 scope_stack 时的初始化"""
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
    
    # 验证 scope_stack 被创建并正确恢复
    assert "scope_stack" in symbol_table
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


def test_handle_block_with_traverse_node_side_effects():
    """测试 _traverse_node 的副作用（如修改变量表）"""
    child: AST = {"type": "var_decl", "value": "x", "data_type": "int", "line": 2, "column": 5}
    
    node: AST = {
        "type": "block",
        "children": [child],
        "line": 1,
        "column": 1
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": []
    }
    
    def mock_traverse_side_effect(node_arg, st):
        if node_arg.get("type") == "var_decl":
            var_name = node_arg.get("value")
            st["variables"][var_name] = {
                "data_type": node_arg.get("data_type"),
                "is_declared": True,
                "line": node_arg.get("line"),
                "column": node_arg.get("column"),
                "scope_level": st["current_scope"]
            }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        mock_traverse.side_effect = mock_traverse_side_effect
        _handle_block(node, symbol_table)
    
    # 验证变量被添加到符号表
    assert "x" in symbol_table["variables"]
    assert symbol_table["variables"]["x"]["scope_level"] == 1  # 在块内 scope 为 1
    assert symbol_table["variables"]["x"]["data_type"] == "int"
    
    # 验证作用域正确恢复
    assert symbol_table["current_scope"] == 0


def test_handle_block_multiple_children_order():
    """测试多个子节点的处理顺序"""
    child1: AST = {"type": "var_decl", "value": "a", "line": 2, "column": 5}
    child2: AST = {"type": "var_decl", "value": "b", "line": 3, "column": 5}
    child3: AST = {"type": "assignment", "value": "c", "line": 4, "column": 5}
    
    node: AST = {
        "type": "block",
        "children": [child1, child2, child3],
        "line": 1,
        "column": 1
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": []
    }
    
    call_order = []
    
    def mock_traverse_track(node_arg, st):
        call_order.append(node_arg.get("value"))
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        mock_traverse.side_effect = mock_traverse_track
        _handle_block(node, symbol_table)
    
    # 验证调用顺序与 children 顺序一致
    assert call_order == ["a", "b", "c"]
    assert mock_traverse.call_count == 3


def test_handle_block_no_current_scope():
    """测试 symbol_table 没有 current_scope 键的情况"""
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
    
    # 验证 current_scope 被正确设置和恢复
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []
