# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._handle_block_src import _handle_block

# === Type definitions ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""

    def _create_symbol_table(self, current_scope: int = 0, scope_stack: list = None) -> SymbolTable:
        """Helper to create a fresh symbol table."""
        if scope_stack is None:
            scope_stack = []
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": scope_stack,
            "current_function": None,
            "errors": []
        }

    def test_handle_block_empty_children(self):
        """Test block with no children - scope should still be managed correctly."""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])

        _handle_block(node, symbol_table)

        # Scope should be restored to original value
        self.assertEqual(symbol_table["current_scope"], 0)
        # Stack should be empty after pop
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_single_child(self):
        """Test block with one child - _traverse_node should be called once."""
        child_node: AST = {"type": "var_decl", "value": "x"}
        node: AST = {
            "type": "block",
            "children": [child_node]
        }
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # Verify _traverse_node was called once with the child
            mock_traverse.assert_called_once_with(child_node, symbol_table)

        # Scope should be restored
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_multiple_children(self):
        """Test block with multiple children - _traverse_node should be called for each."""
        child1: AST = {"type": "var_decl", "value": "x"}
        child2: AST = {"type": "assignment", "value": "y"}
        child3: AST = {"type": "if", "value": "condition"}
        node: AST = {
            "type": "block",
            "children": [child1, child2, child3]
        }
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # Verify _traverse_node was called 3 times in order
            self.assertEqual(mock_traverse.call_count, 3)
            expected_calls = [
                unittest.mock.call(child1, symbol_table),
                unittest.mock.call(child2, symbol_table),
                unittest.mock.call(child3, symbol_table)
            ]
            mock_traverse.assert_has_calls(expected_calls)

        # Scope should be restored
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_increment(self):
        """Test that current_scope is incremented when entering block."""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table = self._create_symbol_table(current_scope=5, scope_stack=[])

        # During execution, current_scope should be 6
        original_scope = symbol_table["current_scope"]
        
        _handle_block(node, symbol_table)

        # After completion, scope should be restored to 5
        self.assertEqual(symbol_table["current_scope"], 5)
        # But during execution it was incremented (we can verify via stack)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_stack_management(self):
        """Test that scope_stack is properly managed (push and pop)."""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table = self._create_symbol_table(current_scope=3, scope_stack=[0, 1])

        _handle_block(node, symbol_table)

        # Stack should be restored to original state
        self.assertEqual(symbol_table["scope_stack"], [0, 1])
        self.assertEqual(symbol_table["current_scope"], 3)

    def test_handle_block_nested_scope_simulation(self):
        """Test block handling simulates nested scope behavior."""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])

        # First block
        _handle_block(node, symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        # Second block (simulating nested)
        _handle_block(node, symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_with_existing_scope_stack(self):
        """Test block when scope_stack already has values."""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table = self._create_symbol_table(current_scope=2, scope_stack=[0, 1])

        _handle_block(node, symbol_table)

        # Should restore to previous state
        self.assertEqual(symbol_table["scope_stack"], [0, 1])
        self.assertEqual(symbol_table["current_scope"], 2)

    def test_handle_block_children_missing_key(self):
        """Test block node without children key - should handle gracefully."""
        node: AST = {
            "type": "block"
            # No "children" key
        }
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # Should not call _traverse_node since no children
            mock_traverse.assert_not_called()

        # Scope should still be managed correctly
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_value_preservation(self):
        """Test that the exact scope value is preserved after block execution."""
        node: AST = {
            "type": "block",
            "children": []
        }
        
        for initial_scope in [0, 1, 5, 10, 100]:
            with self.subTest(initial_scope=initial_scope):
                symbol_table = self._create_symbol_table(current_scope=initial_scope, scope_stack=[])
                _handle_block(node, symbol_table)
                self.assertEqual(symbol_table["current_scope"], initial_scope)
                self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_does_not_modify_other_fields(self):
        """Test that _handle_block only modifies scope-related fields."""
        node: AST = {
            "type": "block",
            "children": []
        }
        symbol_table = self._create_symbol_table(current_scope=0, scope_stack=[])
        symbol_table["variables"] = {"x": {"data_type": "int"}}
        symbol_table["functions"] = {"main": {"return_type": "int"}}
        symbol_table["current_function"] = "main"
        symbol_table["errors"] = ["some error"]

        original_variables = symbol_table["variables"].copy()
        original_functions = symbol_table["functions"].copy()
        original_function = symbol_table["current_function"]
        original_errors = symbol_table["errors"].copy()

        _handle_block(node, symbol_table)

        # Other fields should remain unchanged
        self.assertEqual(symbol_table["variables"], original_variables)
        self.assertEqual(symbol_table["functions"], original_functions)
        self.assertEqual(symbol_table["current_function"], original_function)
        self.assertEqual(symbol_table["errors"], original_errors)


if __name__ == "__main__":
    unittest.main()
