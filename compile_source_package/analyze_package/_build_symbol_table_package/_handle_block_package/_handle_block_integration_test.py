# === Integration Test for _handle_block ===
"""
集成测试：验证_handle_block 在真实模块边界中的行为。
只 mock 外部基础设施依赖，通过真实调用链验证作用域管理和子节点遍历。
"""

import pytest
from typing import Dict, Any
from unittest.mock import patch

# Import the function under test
from projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src import (
    _handle_block,
    _init_traverse_node,
)

# ADT type aliases
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


def create_symbol_table() -> SymbolTable:
    """创建初始符号表"""
    return {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": [],
    }


def create_block_node(children: list = None) -> AST:
    """创建 block 类型的 AST 节点"""
    return {
        "type": "block",
        "children": children if children is not None else [],
        "line": 1,
        "column": 1,
    }


def create_var_decl_node(var_name: str, data_type: str = "int") -> AST:
    """创建变量声明节点"""
    return {
        "type": "var_decl",
        "value": var_name,
        "data_type": data_type,
        "line": 2,
        "column": 5,
    }


class TestHandleBlockIntegration:
    """_handle_block 集成测试"""

    def test_scope_enter_exit_with_real_traverse(self):
        """测试作用域进入/退出，使用真实的_traverse_node"""
        symbol_table = create_symbol_table()
        block_node = create_block_node([])
        
        # 初始化 traverse_fn（真实函数）
        _init_traverse_node()
        
        _handle_block(block_node, symbol_table)
        
        # 验证作用域正确恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_scope_level_increment_decrement(self):
        """测试作用域层级正确增减"""
        symbol_table = create_symbol_table()
        block_node = create_block_node([])
        
        _init_traverse_node()
        _handle_block(block_node, symbol_table)
        
        # 验证作用域层级变化
        assert symbol_table["current_scope"] == 0  # 应该恢复到 0

    def test_scope_stack_push_pop(self):
        """测试作用域栈正确 push/pop"""
        symbol_table = create_symbol_table()
        block_node = create_block_node([])
        
        _init_traverse_node()
        _handle_block(block_node, symbol_table)
        
        # 验证作用域栈正确恢复
        assert symbol_table["scope_stack"] == []

    def test_child_traversal_with_mocked_traverse_node(self):
        """测试子节点遍历，mock _traverse_node 以验证调用"""
        symbol_table = create_symbol_table()
        child1 = create_var_decl_node("x")
        child2 = create_var_decl_node("y")
        block_node = create_block_node([child1, child2])
        
        # Mock _traverse_node 来验证调用
        with patch(
            'projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._traverse_node'
        ) as mock_traverse:
            _handle_block(block_node, symbol_table)
            
            # 验证_traverse_node 被调用了 2 次（每个子节点一次）
            assert mock_traverse.call_count == 2
            # 验证调用参数
            mock_traverse.assert_any_call(child1, symbol_table)
            mock_traverse.assert_any_call(child2, symbol_table)

    def test_empty_children_handling(self):
        """测试空子节点列表的处理"""
        symbol_table = create_symbol_table()
        block_node = create_block_node([])
        
        _init_traverse_node()
        _handle_block(block_node, symbol_table)
        
        # 验证作用域正确恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_missing_children_key(self):
        """测试缺少 children 键的处理"""
        symbol_table = create_symbol_table()
        # 创建没有 children 键的节点
        block_node = {
            "type": "block",
            "line": 1,
            "column": 1,
        }
        
        _init_traverse_node()
        _handle_block(block_node, symbol_table)
        
        # 验证作用域正确恢复（不应该抛异常）
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_nested_blocks_scope_management(self):
        """测试嵌套块的作用域管理"""
        symbol_table = create_symbol_table()
        inner_block = create_block_node([])
        outer_block = create_block_node([inner_block])
        
        _init_traverse_node()
        
        # 处理外层块
        _handle_block(outer_block, symbol_table)
        
        # 验证最终作用域恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_exception_in_child_traversal_guarantees_exit(self):
        """测试子节点遍历异常时，finally 保证退出作用域"""
        symbol_table = create_symbol_table()
        child_node = create_var_decl_node("x")
        block_node = create_block_node([child_node])
        
        # Mock _traverse_node 抛异常
        with patch(
            'projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._traverse_node',
            side_effect=RuntimeError("Test exception")
        ):
            with pytest.raises(RuntimeError, match="Test exception"):
                _handle_block(block_node, symbol_table)
        
        # 验证即使抛异常，作用域也正确恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_multiple_sequential_blocks(self):
        """测试多个顺序块的作用域管理"""
        symbol_table = create_symbol_table()
        block1 = create_block_node([])
        block2 = create_block_node([])
        
        _init_traverse_node()
        
        # 处理两个块
        _handle_block(block1, symbol_table)
        _handle_block(block2, symbol_table)
        
        # 验证作用域正确恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_scope_stack_content_verification(self):
        """验证作用域栈内容在块处理期间正确"""
        symbol_table = create_symbol_table()
        block_node = create_block_node([])
        
        # 我们需要在块处理期间检查栈内容
        # 通过 mock traverse_fn 来在遍历期间检查
        original_traverse = _init_traverse_node()
        
        def check_scope_during_traverse(node, st):
            # 在遍历期间，作用域应该是 1，栈应该有"block"
            assert st["current_scope"] == 1
            assert "block" in st["scope_stack"]
        
        with patch(
            'projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._traverse_node',
            side_effect=check_scope_during_traverse
        ):
            _handle_block(block_node, symbol_table)
        
        # 验证最终恢复
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
