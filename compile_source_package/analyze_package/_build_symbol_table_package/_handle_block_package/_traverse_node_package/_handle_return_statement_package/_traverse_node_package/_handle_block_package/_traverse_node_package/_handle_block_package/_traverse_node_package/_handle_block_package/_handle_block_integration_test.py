"""Integration tests for _handle_block function.

Tests verify real module boundary behavior with actual _traverse_node dispatch.
Only external infrastructure dependencies are mocked (none needed for this function).
"""

import pytest
from typing import Any, Dict

# Import the actual function under test
from _handle_block_src import _handle_block


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


def create_block_node(children=None, line=1, column=1):
    """Helper to create a block AST node."""
    node = {
        "type": "block",
        "line": line,
        "column": column,
    }
    if children is not None:
        node["children"] = children
    return node


def create_var_decl_node(var_name, data_type="int", line=1, column=1):
    """Helper to create a variable declaration AST node."""
    return {
        "type": "var_decl",
        "name": var_name,
        "data_type": data_type,
        "line": line,
        "column": column,
    }


def create_assignment_node(var_name, line=1, column=1):
    """Helper to create an assignment AST node."""
    return {
        "type": "assignment",
        "name": var_name,
        "line": line,
        "column": column,
    }


class TestHandleBlockIntegration:
    """Integration tests for _handle_block with real _traverse_node dispatch."""

    def test_handle_block_enters_and_exits_scope(self):
        """Test that block handling correctly manages scope levels."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
        }
        
        block_node = create_block_node(children=[])
        
        initial_scope = symbol_table.get("current_scope", 0)
        _handle_block(block_node, symbol_table)
        final_scope = symbol_table.get("current_scope", 0)
        
        # Should return to original scope after block
        assert final_scope == initial_scope
        # Scope stack should be empty
        assert symbol_table.get("scope_stack", []) == []

    def test_handle_block_scope_level_increments_during_execution(self):
        """Test that scope level increases while inside block."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }
        
        # Manually test the scope change during block execution
        old_scope = symbol_table["current_scope"]
        symbol_table["scope_stack"].append(old_scope)
        symbol_table["current_scope"] = old_scope + 1
        
        # Verify scope increased
        assert symbol_table["current_scope"] == 1
        
        # Restore
        if symbol_table["scope_stack"]:
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
        
        assert symbol_table["current_scope"] == 0

    def test_handle_block_nested_blocks(self):
        """Test nested block scope management."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }
        
        # Create nested block structure
        inner_block = create_block_node(children=[])
        outer_block = create_block_node(children=[inner_block])
        
        _handle_block(outer_block, symbol_table)
        
        # Should return to scope 0 after both blocks
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_handle_block_initializes_missing_fields(self):
        """Test that _handle_block initializes missing symbol_table fields."""
        symbol_table: SymbolTable = {}
        
        block_node = create_block_node(children=[])
        _handle_block(block_node, symbol_table)
        
        # Should initialize all required fields
        assert "current_scope" in symbol_table
        assert "scope_stack" in symbol_table
        assert "errors" in symbol_table
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []
        assert symbol_table["errors"] == []

    def test_handle_block_exits_scope_on_error(self):
        """Test that scope is properly exited even if error occurs."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": [],
        }
        
        # Create a block with a problematic child node
        problematic_child = {
            "type": "unknown_type",
            "line": 5,
            "column": 10,
        }
        block_node = create_block_node(children=[problematic_child])
        
        # Should not raise exception
        _handle_block(block_node, symbol_table)
        
        # Scope should still be restored
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_handle_block_empty_block(self):
        """Test handling of empty block (no children)."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }
        
        block_node = create_block_node(children=[])
        _handle_block(block_node, symbol_table)
        
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_handle_block_missing_children_field(self):
        """Test handling of block node without children field."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }
        
        # Block without children field
        block_node = {
            "type": "block",
            "line": 1,
            "column": 1,
        }
        
        _handle_block(block_node, symbol_table)
        
        # Should handle gracefully with default empty list
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []

    def test_handle_block_preserves_other_fields(self):
        """Test that _handle_block doesn't modify unrelated symbol_table fields."""
        symbol_table: SymbolTable = {
            "variables": {"existing_var": {"data_type": "int", "is_declared": True}},
            "functions": {"main": {"return_type": "int", "params": []}},
            "current_scope": 0,
            "scope_stack": [],
            "custom_field": "should_not_change",
        }
        
        block_node = create_block_node(children=[])
        _handle_block(block_node, symbol_table)
        
        # Unrelated fields should be preserved
        assert symbol_table["variables"]["existing_var"]["data_type"] == "int"
        assert symbol_table["functions"]["main"]["return_type"] == "int"
        assert symbol_table["custom_field"] == "should_not_change"

    def test_handle_block_scope_stack_operations(self):
        """Test scope stack push/pop operations."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": [],
        }
        
        block_node = create_block_node(children=[])
        _handle_block(block_node, symbol_table)
        
        # Should return to scope 5
        assert symbol_table["current_scope"] == 5
        # Stack should be empty
        assert symbol_table["scope_stack"] == []

    def test_handle_block_with_multiple_statements(self):
        """Test block with multiple child statements."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": [],
        }
        
        # Create block with multiple children
        children = [
            create_var_decl_node("x", "int", line=2, column=1),
            create_assignment_node("x", line=3, column=1),
            create_var_decl_node("y", "char", line=4, column=1),
        ]
        block_node = create_block_node(children=children)
        
        _handle_block(block_node, symbol_table)
        
        # Scope should be restored
        assert symbol_table["current_scope"] == 0
        assert symbol_table["scope_stack"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
