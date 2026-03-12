# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._handle_return_src import _handle_return

# === Type definitions ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturn(unittest.TestCase):
    """Test cases for _handle_return function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_handle_return_with_single_child(self):
        """Test return statement with a single return expression."""
        node: AST = {
            "type": "return",
            "children": [{"type": "expression", "value": 42, "line": 1, "column": 5}],
            "line": 1,
            "column": 1
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, self.symbol_table)
            
            mock_traverse.assert_called_once()
            mock_traverse.assert_called_once_with(node["children"][0], self.symbol_table)

    def test_handle_return_with_multiple_children(self):
        """Test return statement with multiple return expressions."""
        child1: AST = {"type": "expression", "value": 1, "line": 1, "column": 10}
        child2: AST = {"type": "expression", "value": 2, "line": 1, "column": 15}
        child3: AST = {"type": "expression", "value": 3, "line": 1, "column": 20}
        
        node: AST = {
            "type": "return",
            "children": [child1, child2, child3],
            "line": 1,
            "column": 1
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, self.symbol_table)
            
            self.assertEqual(mock_traverse.call_count, 3)
            mock_traverse.assert_any_call(child1, self.symbol_table)
            mock_traverse.assert_any_call(child2, self.symbol_table)
            mock_traverse.assert_any_call(child3, self.symbol_table)

    def test_handle_return_without_children(self):
        """Test return statement without children (empty return)."""
        node: AST = {
            "type": "return",
            "line": 1,
            "column": 1
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, self.symbol_table)
            
            mock_traverse.assert_not_called()

    def test_handle_return_with_empty_children_list(self):
        """Test return statement with empty children list."""
        node: AST = {
            "type": "return",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, self.symbol_table)
            
            mock_traverse.assert_not_called()

    def test_handle_return_with_complex_expression(self):
        """Test return statement with complex nested expression."""
        nested_child: AST = {
            "type": "binary_op",
            "children": [
                {"type": "variable", "value": "x", "line": 2, "column": 10},
                {"type": "literal", "value": 5, "line": 2, "column": 12}
            ],
            "value": "+",
            "line": 2,
            "column": 11
        }
        
        node: AST = {
            "type": "return",
            "children": [nested_child],
            "line": 1,
            "column": 1
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, self.symbol_table)
            
            mock_traverse.assert_called_once_with(nested_child, self.symbol_table)

    def test_handle_return_preserves_symbol_table(self):
        """Test that symbol_table is passed correctly to _traverse_node."""
        node: AST = {
            "type": "return",
            "children": [{"type": "expression", "value": "test", "line": 1, "column": 5}],
            "line": 1,
            "column": 1
        }

        custom_symbol_table: SymbolTable = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 1,
            "scope_stack": [0],
            "current_function": "main",
            "errors": []
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, custom_symbol_table)
            
            mock_traverse.assert_called_once()
            # Verify the exact same symbol_table object is passed
            self.assertIs(mock_traverse.call_args[0][1], custom_symbol_table)

    def test_handle_return_with_none_children(self):
        """Test return statement where children is explicitly None."""
        node: AST = {
            "type": "return",
            "children": None,
            "line": 1,
            "column": 1
        }

        with patch("._handle_return_src._traverse_node") as mock_traverse:
            _handle_return(node, self.symbol_table)
            
            mock_traverse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
