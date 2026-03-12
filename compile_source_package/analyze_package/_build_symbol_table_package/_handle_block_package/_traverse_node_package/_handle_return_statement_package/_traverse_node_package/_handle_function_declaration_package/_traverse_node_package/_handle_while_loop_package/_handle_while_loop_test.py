"""Unit tests for _handle_while_loop function."""

import unittest
from unittest.mock import Mock
from typing import Dict, Any

from ._handle_while_loop_src import _handle_while_loop


class TestHandleWhileLoop(unittest.TestCase):
    """Test cases for _handle_while_loop function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.traverse_fn = Mock()
    
    def _create_symbol_table(self) -> Dict[str, Any]:
        """Create a fresh symbol table for testing."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": "",
            "errors": []
        }
    
    def _create_while_loop_node(
        self,
        condition_node: Dict[str, Any],
        body_node: Dict[str, Any],
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Create a while_loop AST node."""
        return {
            "type": "while_loop",
            "children": [condition_node, body_node],
            "line": line,
            "column": column
        }
    
    def test_valid_while_loop_with_block_body(self):
        """Test while_loop with block body - scope should be managed."""
        symbol_table = self._create_symbol_table()
        
        condition_node = {"type": "binary_op", "value": "==", "children": []}
        body_node = {
            "type": "block",
            "children": [
                {"type": "assignment", "value": "x = 1"},
                {"type": "assignment", "value": "y = 2"}
            ]
        }
        while_node = self._create_while_loop_node(condition_node, body_node)
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify traverse_fn called on condition
        self.traverse_fn.assert_any_call(condition_node, symbol_table)
        
        # Verify traverse_fn called on body children
        self.traverse_fn.assert_any_call(body_node["children"][0], symbol_table)
        self.traverse_fn.assert_any_call(body_node["children"][1], symbol_table)
        
        # Verify scope management
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_valid_while_loop_with_non_block_body(self):
        """Test while_loop with non-block body - no scope management."""
        symbol_table = self._create_symbol_table()
        
        condition_node = {"type": "identifier", "value": "x"}
        body_node = {"type": "assignment", "value": "x = 1"}
        while_node = self._create_while_loop_node(condition_node, body_node)
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify traverse_fn called on condition
        self.traverse_fn.assert_any_call(condition_node, symbol_table)
        
        # Verify traverse_fn called on body directly
        self.traverse_fn.assert_any_call(body_node, symbol_table)
        
        # Verify no scope management
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_invalid_node_less_than_2_children(self):
        """Test while_loop with less than 2 children - should append error."""
        symbol_table = self._create_symbol_table()
        
        condition_node = {"type": "binary_op", "value": "==", "children": []}
        while_node = {
            "type": "while_loop",
            "children": [condition_node],  # Only 1 child
            "line": 5,
            "column": 10
        }
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify error was appended
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "AST_ERROR")
        self.assertIn("at least 2 children", error["message"])
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
        
        # Verify traverse_fn not called
        self.traverse_fn.assert_not_called()
        
        # Verify no scope changes
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_invalid_node_no_children(self):
        """Test while_loop with no children - should append error."""
        symbol_table = self._create_symbol_table()
        
        while_node = {
            "type": "while_loop",
            "children": [],
            "line": 3,
            "column": 5
        }
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify error was appended
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "AST_ERROR")
        self.assertIn("at least 2 children", error["message"])
        self.assertEqual(error["line"], 3)
        self.assertEqual(error["column"], 5)
        
        # Verify traverse_fn not called
        self.traverse_fn.assert_not_called()
    
    def test_scope_management_with_block_body(self):
        """Test that scope is properly incremented and decremented for block body."""
        symbol_table = self._create_symbol_table()
        symbol_table["current_scope"] = 2
        symbol_table["scope_stack"] = [1, 2]
        
        condition_node = {"type": "identifier", "value": "x"}
        body_node = {
            "type": "block",
            "children": [{"type": "assignment", "value": "x = 1"}]
        }
        while_node = self._create_while_loop_node(condition_node, body_node)
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify scope returns to original value
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [1, 2])
    
    def test_traverse_fn_not_provided(self):
        """Test that function handles missing traverse_fn gracefully."""
        symbol_table = self._create_symbol_table()
        
        condition_node = {"type": "identifier", "value": "x"}
        body_node = {"type": "assignment", "value": "x = 1"}
        while_node = self._create_while_loop_node(condition_node, body_node)
        
        # Should not raise exception
        _handle_while_loop(while_node, symbol_table, None)
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_empty_block_body(self):
        """Test while_loop with empty block body."""
        symbol_table = self._create_symbol_table()
        
        condition_node = {"type": "identifier", "value": "x"}
        body_node = {
            "type": "block",
            "children": []
        }
        while_node = self._create_while_loop_node(condition_node, body_node)
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify traverse_fn called on condition
        self.traverse_fn.assert_called_with(condition_node, symbol_table)
        
        # Verify scope management still happens
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_error_preserves_existing_errors(self):
        """Test that new errors are appended without removing existing ones."""
        symbol_table = self._create_symbol_table()
        symbol_table["errors"].append({"type": "EXISTING_ERROR", "message": "pre-existing"})
        
        while_node = {
            "type": "while_loop",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        _handle_while_loop(while_node, symbol_table, self.traverse_fn)
        
        # Verify both errors exist
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["type"], "EXISTING_ERROR")
        self.assertEqual(symbol_table["errors"][1]["type"], "AST_ERROR")


if __name__ == "__main__":
    unittest.main()
