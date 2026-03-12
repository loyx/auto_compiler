# -*- coding: utf-8 -*-
"""Unit tests for _handle_block function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative imports from the same package
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        pass

    def tearDown(self) -> None:
        """Tear down test fixtures."""
        pass

    def test_handle_block_empty_block(self) -> None:
        """Test handling an empty block with no children."""
        node: Dict[str, Any] = {
            "type": "block",
            "children": []
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        _handle_block(node, symbol_table)

        # Scope should be restored to original value
        self.assertEqual(symbol_table["current_scope"], 0)
        # Scope stack should be empty after pop
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_with_children(self) -> None:
        """Test handling a block with child nodes."""
        child_node1: Dict[str, Any] = {"type": "declaration", "value": "x"}
        child_node2: Dict[str, Any] = {"type": "statement", "value": "y"}
        node: Dict[str, Any] = {
            "type": "block",
            "children": [child_node1, child_node2]
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)

            # _traverse_node should be called for each child
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(child_node1, symbol_table)
            mock_traverse.assert_any_call(child_node2, symbol_table)

        # Scope should be restored
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_scope_increment_and_restore(self) -> None:
        """Test that scope is properly incremented and restored."""
        node: Dict[str, Any] = {
            "type": "block",
            "children": []
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": [0, 1, 2]
        }

        _handle_block(node, symbol_table)

        # current_scope should be restored to 5
        self.assertEqual(symbol_table["current_scope"], 5)
        # scope_stack should be restored to original state
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2])

    def test_handle_block_nested_blocks(self) -> None:
        """Test handling nested blocks (multiple scope levels)."""
        inner_child: Dict[str, Any] = {"type": "declaration", "value": "inner"}
        inner_block: Dict[str, Any] = {
            "type": "block",
            "children": [inner_child]
        }
        outer_child: Dict[str, Any] = {"type": "declaration", "value": "outer"}
        outer_block: Dict[str, Any] = {
            "type": "block",
            "children": [outer_child, inner_block]
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_block_src._traverse_node") as mock_traverse:
            # Make _traverse_node call _handle_block for inner block
            def traverse_side_effect(node: Dict[str, Any], st: Dict[str, Any]) -> None:
                if node.get("type") == "block":
                    _handle_block(node, st)

            mock_traverse.side_effect = traverse_side_effect
            _handle_block(outer_block, symbol_table)

        # After processing both blocks, scope should be back to 0
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_block_missing_children_key(self) -> None:
        """Test handling a block node without 'children' key."""
        node: Dict[str, Any] = {
            "type": "block"
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 3,
            "scope_stack": [0, 1, 2]
        }

        _handle_block(node, symbol_table)

        # Should handle gracefully with empty children
        self.assertEqual(symbol_table["current_scope"], 3)
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2])

    def test_handle_block_scope_stack_operations(self) -> None:
        """Test that scope_stack operations are correct (append before, pop after)."""
        node: Dict[str, Any] = {
            "type": "block",
            "children": []
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 10,
            "scope_stack": [5]
        }

        # During execution, scope_stack should have [5, 10] and current_scope should be 11
        # After execution, both should be restored
        _handle_block(node, symbol_table)

        # Verify restoration
        self.assertEqual(symbol_table["current_scope"], 10)
        self.assertEqual(symbol_table["scope_stack"], [5])


if __name__ == "__main__":
    unittest.main()
