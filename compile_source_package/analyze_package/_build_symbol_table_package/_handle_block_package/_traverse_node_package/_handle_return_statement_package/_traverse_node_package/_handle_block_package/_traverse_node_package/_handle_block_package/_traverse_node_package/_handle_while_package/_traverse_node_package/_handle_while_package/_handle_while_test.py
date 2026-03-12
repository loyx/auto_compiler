# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._handle_while_src import _handle_while

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_handle_while_normal_case(self):
        """Test normal while node with condition and body."""
        condition_node = {"type": "identifier", "value": "x", "line": 5, "column": 10}
        body_node = {"type": "block", "children": [], "line": 5, "column": 15}
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(condition_node, self.symbol_table)
            mock_traverse.assert_any_call(body_node, self.symbol_table)

    def test_handle_while_none_node(self):
        """Test that None node is handled gracefully."""
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(None, self.symbol_table)

            mock_traverse.assert_not_called()
            self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_while_no_children(self):
        """Test while node with no children."""
        node = {
            "type": "while",
            "children": [],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            mock_traverse.assert_not_called()
            self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_while_one_child(self):
        """Test while node with only one child (less than 2)."""
        condition_node = {"type": "identifier", "value": "x", "line": 5, "column": 10}
        node = {
            "type": "while",
            "children": [condition_node],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            mock_traverse.assert_not_called()
            self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_while_missing_children_key(self):
        """Test while node without children key."""
        node = {
            "type": "while",
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            mock_traverse.assert_not_called()
            self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_handle_while_three_children(self):
        """Test while node with more than 2 children (only first 2 used)."""
        condition_node = {"type": "identifier", "value": "x", "line": 5, "column": 10}
        body_node = {"type": "block", "children": [], "line": 5, "column": 15}
        extra_node = {"type": "comment", "value": "extra", "line": 5, "column": 20}
        node = {
            "type": "while",
            "children": [condition_node, body_node, extra_node],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(condition_node, self.symbol_table)
            mock_traverse.assert_any_call(body_node, self.symbol_table)

    def test_handle_while_preserves_symbol_table_errors(self):
        """Test that existing errors in symbol_table are preserved."""
        condition_node = {"type": "identifier", "value": "x", "line": 5, "column": 10}
        body_node = {"type": "block", "children": [], "line": 5, "column": 15}
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 0
        }
        self.symbol_table["errors"] = ["Existing error"]

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            self.assertIn("Existing error", self.symbol_table["errors"])
            self.assertEqual(len(self.symbol_table["errors"]), 1)

    def test_handle_while_with_complex_condition(self):
        """Test while node with complex condition expression."""
        condition_node = {
            "type": "binary_op",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": 10, "line": 5, "column": 12}
            ],
            "line": 5,
            "column": 8
        }
        body_node = {
            "type": "block",
            "children": [
                {"type": "assignment", "line": 6, "column": 4}
            ],
            "line": 5,
            "column": 15
        }
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(condition_node, self.symbol_table)
            mock_traverse.assert_any_call(body_node, self.symbol_table)

    def test_handle_while_empty_body(self):
        """Test while node with empty body."""
        condition_node = {"type": "identifier", "value": "x", "line": 5, "column": 10}
        body_node = {"type": "block", "children": [], "line": 5, "column": 15}
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)

    def test_handle_while_nested_while(self):
        """Test while node with nested while in body."""
        inner_while = {
            "type": "while",
            "children": [
                {"type": "identifier", "value": "y", "line": 6, "column": 10},
                {"type": "block", "children": [], "line": 6, "column": 15}
            ],
            "line": 6,
            "column": 4
        }
        condition_node = {"type": "identifier", "value": "x", "line": 5, "column": 10}
        body_node = {
            "type": "block",
            "children": [inner_while],
            "line": 5,
            "column": 15
        }
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 0
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, self.symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(condition_node, self.symbol_table)
            mock_traverse.assert_any_call(body_node, self.symbol_table)


if __name__ == "__main__":
    unittest.main()
