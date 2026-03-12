import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Relative import from the same package
from ._handle_block_src import _handle_block

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""
    
    def test_handle_block_scope_management_empty_children(self):
        """Test that scope is properly entered and exited with empty block."""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        node: AST = {
            "type": "block",
            "line": 1,
            "column": 1
        }
        
        _handle_block(node, symbol_table)
        
        # Scope should be restored to original value
        self.assertEqual(symbol_table["current_scope"], 0)
        # Stack should be empty after pop
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_missing_children_key(self):
        """Test block with no children key (uses default empty list)."""
        symbol_table: SymbolTable = {
            "current_scope": 5,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        node: AST = {
            "type": "block",
            "line": 1,
            "column": 1
            # No children key
        }
        
        _handle_block(node, symbol_table)
        
        # Scope should be restored
        self.assertEqual(symbol_table["current_scope"], 5)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    @patch('projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._handle_block_src._traverse_node')
    def test_handle_block_with_children(self, mock_traverse: MagicMock):
        """Test that all children are processed via _traverse_node."""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        child1: AST = {"type": "var_decl", "line": 2, "column": 1}
        child2: AST = {"type": "assignment", "line": 3, "column": 1}
        child3: AST = {"type": "if", "line": 4, "column": 1}
        
        node: AST = {
            "type": "block",
            "children": [child1, child2, child3],
            "line": 1,
            "column": 1
        }
        
        _handle_block(node, symbol_table)
        
        # _traverse_node should be called 3 times, once for each child
        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_any_call(child1, symbol_table)
        mock_traverse.assert_any_call(child2, symbol_table)
        mock_traverse.assert_any_call(child3, symbol_table)
    
    @patch('._handle_block_src._traverse_node')
    def test_handle_block_scope_increment_during_processing(self, mock_traverse: MagicMock):
        """Test that scope is incremented during child processing."""
        symbol_table: SymbolTable = {
            "current_scope": 5,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        node: AST = {
            "type": "block",
            "children": [{"type": "stmt", "line": 2, "column": 1}],
            "line": 1,
            "column": 1
        }
        
        # Track scope value during child processing
        scope_during_call = None
        
        def capture_scope(child: AST, st: SymbolTable) -> None:
            nonlocal scope_during_call
            scope_during_call = st["current_scope"]
        
        mock_traverse.side_effect = capture_scope
        
        _handle_block(node, symbol_table)
        
        # Verify scope was incremented to 6 during child processing
        self.assertEqual(scope_during_call, 6)
        # Verify scope restored to 5 after block exits
        self.assertEqual(symbol_table["current_scope"], 5)
    
    @patch('._handle_block_src._traverse_node')
    def test_handle_block_nested_scopes(self, mock_traverse: MagicMock):
        """Test nested block scope management."""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        # Simulate nested block by having _traverse_node call _handle_block again
        def nested_block_handler(child: AST, st: SymbolTable) -> None:
            if child.get("type") == "block":
                _handle_block(child, st)
        
        mock_traverse.side_effect = nested_block_handler
        
        inner_block: AST = {
            "type": "block",
            "children": [],
            "line": 2,
            "column": 1
        }
        
        outer_block: AST = {
            "type": "block",
            "children": [inner_block],
            "line": 1,
            "column": 1
        }
        
        _handle_block(outer_block, symbol_table)
        
        # Both scopes should be properly managed and restored
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    @patch('._handle_block_src._traverse_node')
    def test_handle_block_preserves_existing_stack(self, mock_traverse: MagicMock):
        """Test that existing scope stack is preserved and restored."""
        symbol_table: SymbolTable = {
            "current_scope": 2,
            "scope_stack": [0, 1],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        _handle_block(node, symbol_table)
        
        # Should restore to previous scope level (2)
        self.assertEqual(symbol_table["current_scope"], 2)
        # Original stack should be restored
        self.assertEqual(symbol_table["scope_stack"], [0, 1])
    
    @patch('._handle_block_src._traverse_node')
    def test_handle_block_multiple_nested_levels(self, mock_traverse: MagicMock):
        """Test multiple levels of nested blocks."""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": []
        }
        
        def nested_handler(child: AST, st: SymbolTable) -> None:
            if child.get("type") == "block":
                _handle_block(child, st)
        
        mock_traverse.side_effect = nested_handler
        
        # Create 3 levels of nested blocks
        level3: AST = {"type": "block", "children": [], "line": 3, "column": 1}
        level2: AST = {"type": "block", "children": [level3], "line": 2, "column": 1}
        level1: AST = {"type": "block", "children": [level2], "line": 1, "column": 1}
        
        _handle_block(level1, symbol_table)
        
        # All scopes should be properly restored
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    @patch('._handle_block_src._traverse_node')
    def test_handle_block_with_existing_data(self, mock_traverse: MagicMock):
        """Test that block processing doesn't affect other symbol_table fields."""
        symbol_table: SymbolTable = {
            "current_scope": 1,
            "scope_stack": [0],
            "variables": {"x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}},
            "functions": {"main": {"return_type": "int", "params": [], "line": 1, "column": 1}},
            "errors": [{"type": "warning", "line": 1, "column": 1, "message": "test"}]
        }
        
        # Store copies for comparison
        original_vars = dict(symbol_table["variables"])
        original_funcs = dict(symbol_table["functions"])
        original_errors = list(symbol_table["errors"])
        
        node: AST = {
            "type": "block",
            "children": [],
            "line": 2,
            "column": 1
        }
        
        _handle_block(node, symbol_table)
        
        # Other fields should remain unchanged
        self.assertEqual(symbol_table["variables"], original_vars)
        self.assertEqual(symbol_table["functions"], original_funcs)
        self.assertEqual(symbol_table["errors"], original_errors)
        # Scope should be restored
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [0])


if __name__ == '__main__':
    unittest.main()
