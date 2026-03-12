import unittest
from unittest.mock import patch, call, MagicMock
from typing import Dict, Any

# Import the function under test using relative import
from ._handle_block_src import _handle_block

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    def test_handle_block_enters_and_exits_scope(self):
        """Test that block handling properly enters and exits scope."""
        node = {
            "type": "block",
            "children": [],
            "value": None,
            "data_type": None,
            "line": 1,
            "column": 1
        }
        
        mock_traverse = MagicMock()
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._init_traverse_node", return_value=mock_traverse):
            _handle_block(node, self.symbol_table)
        
        # Scope should return to original value after entering and exiting
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])
    
    def test_handle_block_with_children_calls_traverse(self):
        """Test that _traverse_node is called for each child."""
        child1 = {"type": "statement", "children": []}
        child2 = {"type": "statement", "children": []}
        node = {
            "type": "block",
            "children": [child1, child2],
            "value": None,
            "data_type": None,
            "line": 1,
            "column": 1
        }
        
        mock_traverse = MagicMock()
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._init_traverse_node", return_value=mock_traverse):
            _handle_block(node, self.symbol_table)
            
            # _traverse_node should be called twice (once for each child)
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(child1, self.symbol_table)
            mock_traverse.assert_any_call(child2, self.symbol_table)
    
    def test_handle_block_exits_scope_on_exception(self):
        """Test that scope is exited even if traversal raises an exception."""
        child = {"type": "statement", "children": []}
        node = {
            "type": "block",
            "children": [child],
            "value": None,
            "data_type": None,
            "line": 1,
            "column": 1
        }
        
        mock_traverse = MagicMock()
        mock_traverse.side_effect = RuntimeError("Test exception")
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._init_traverse_node", return_value=mock_traverse):
            with self.assertRaises(RuntimeError):
                _handle_block(node, self.symbol_table)
            
            # Scope should still be exited despite exception
            self.assertEqual(self.symbol_table["current_scope"], 0)
            self.assertEqual(self.symbol_table["scope_stack"], [])
    
    def test_handle_block_empty_children(self):
        """Test handling of block with no children."""
        node = {
            "type": "block",
            "children": [],
            "value": None,
            "data_type": None,
            "line": 1,
            "column": 1
        }
        
        mock_traverse = MagicMock()
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._init_traverse_node", return_value=mock_traverse):
            _handle_block(node, self.symbol_table)
        
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])
    
    def test_handle_block_missing_children_key(self):
        """Test handling of node without children key."""
        node = {
            "type": "block",
            "value": None,
            "data_type": None,
            "line": 1,
            "column": 1
        }
        
        mock_traverse = MagicMock()
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._init_traverse_node", return_value=mock_traverse):
            _handle_block(node, self.symbol_table)
        
        self.assertEqual(self.symbol_table["current_scope"], 0)
        self.assertEqual(self.symbol_table["scope_stack"], [])
    
    def test_handle_block_nested_scope_levels(self):
        """Test handling when starting from non-zero scope level."""
        self.symbol_table["current_scope"] = 2
        self.symbol_table["scope_stack"] = ["global", "function"]
        
        node = {
            "type": "block",
            "children": [],
            "value": None,
            "data_type": None,
            "line": 1,
            "column": 1
        }
        
        mock_traverse = MagicMock()
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._handle_block_src._init_traverse_node", return_value=mock_traverse):
            _handle_block(node, self.symbol_table)
        
        # Should return to original scope level
        self.assertEqual(self.symbol_table["current_scope"], 2)
        self.assertEqual(self.symbol_table["scope_stack"], ["global", "function"])


if __name__ == "__main__":
    unittest.main()