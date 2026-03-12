# === imports ===
from typing import Any, Dict
from unittest.mock import patch, call

# === relative imports for UUT ===
from ._handle_block_src import _handle_block

# === type aliases (matching UUT) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# === test cases ===
def test_handle_block_with_children_scope_management():
    """测试 block 有子节点时的作用域管理。"""
    node: AST = {
        "type": "block",
        "children": [
            {"type": "var_decl", "value": "x"},
            {"type": "assignment", "value": "y"},
        ],
        "line": 1,
        "column": 0,
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": [],
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        _handle_block(node, symbol_table)
    
    # 验证作用域进入时递增
    assert symbol_table["current_scope"] == 0  # 退出后应恢复为 0
    assert symbol_table["scope_stack"] == []  # 栈应清空
    
    # 验证 _traverse_node 被调用两次（每个子节点一次）
    assert mock_traverse.call_count == 2
    mock_traverse.assert_has_calls([
        call({"type": "var_decl", "value": "x"}, symbol_table),
        call({"type": "assignment", "value": "y"}, symbol_table),
    ])


def test_handle_block_empty_children():
    """测试空 block（无子节点）的处理。"""
    node: AST = {
        "type": "block",
        "children": [],
        "line": 1,
        "column": 0,
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 5,
        "scope_stack": [],
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        _handle_block(node, symbol_table)
    
    # 验证作用域恢复
    assert symbol_table["current_scope"] == 5
    assert symbol_table["scope_stack"] == []
    # 验证 _traverse_node 未被调用
    mock_traverse.assert_not_called()


def test_handle_block_missing_errors_key():
    """测试 symbol_table 缺少 errors 键时的处理。"""
    node: AST = {
        "type": "block",
        "children": [],
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 0,
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node"):
        _handle_block(node, symbol_table)
    
    # 验证 errors 被创建
    assert "errors" in symbol_table
    assert symbol_table["errors"] == []


def test_handle_block_missing_scope_stack_key():
    """测试 symbol_table 缺少 scope_stack 键时的处理。"""
    node: AST = {
        "type": "block",
        "children": [],
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 0,
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node"):
        _handle_block(node, symbol_table)
    
    # 验证 scope_stack 被创建
    assert "scope_stack" in symbol_table
    assert symbol_table["scope_stack"] == []


def test_handle_block_missing_current_scope_key():
    """测试 symbol_table 缺少 current_scope 键时的处理（应默认为 0）。"""
    node: AST = {
        "type": "block",
        "children": [],
    }
    symbol_table: SymbolTable = {
        "variables": {},
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node"):
        _handle_block(node, symbol_table)
    
    # 验证 current_scope 恢复为默认值 0
    assert symbol_table["current_scope"] == 0


def test_handle_block_nested_scope_restoration():
    """测试嵌套作用域的正确恢复。"""
    node: AST = {
        "type": "block",
        "children": [],
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 3,
        "scope_stack": [0, 1, 2],
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node"):
        _handle_block(node, symbol_table)
    
    # 验证作用域恢复为进入前的值
    assert symbol_table["current_scope"] == 3
    assert symbol_table["scope_stack"] == [0, 1, 2]


def test_handle_block_scope_increment_during_execution():
    """测试作用域在处理过程中的递增行为。"""
    node: AST = {
        "type": "block",
        "children": [{"type": "var_decl"}],
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 0,
        "scope_stack": [],
    }
    
    # 捕获 _traverse_node 调用时的作用域状态
    captured_scopes = []
    
    def capture_scope(node, st):
        captured_scopes.append(st["current_scope"])
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node", side_effect=capture_scope):
        _handle_block(node, symbol_table)
    
    # 验证在子节点处理时作用域为 1（进入 block 后递增）
    assert captured_scopes == [1]
    # 验证最终恢复为 0
    assert symbol_table["current_scope"] == 0


def test_handle_block_multiple_children_order():
    """测试多个子节点的处理顺序。"""
    node: AST = {
        "type": "block",
        "children": [
            {"type": "stmt1", "value": "first"},
            {"type": "stmt2", "value": "second"},
            {"type": "stmt3", "value": "third"},
        ],
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 0,
        "scope_stack": [],
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        _handle_block(node, symbol_table)
    
    # 验证调用顺序与子节点顺序一致
    assert mock_traverse.call_count == 3
    calls = mock_traverse.call_args_list
    assert calls[0][0][0]["value"] == "first"
    assert calls[1][0][0]["value"] == "second"
    assert calls[2][0][0]["value"] == "third"


def test_handle_block_children_key_missing():
    """测试 node 缺少 children 键时的处理。"""
    node: AST = {
        "type": "block",
        "line": 1,
    }
    symbol_table: SymbolTable = {
        "variables": {},
        "current_scope": 0,
        "scope_stack": [],
    }
    
    with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
        _handle_block(node, symbol_table)
    
    # 验证 _traverse_node 未被调用（children 默认为空列表）
    mock_traverse.assert_not_called()
    # 验证作用域正确恢复
    assert symbol_table["current_scope"] == 0
