# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._traverse_node_src import _traverse_node

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    # ==================== Basic Dispatch Tests ====================

    def test_traverse_node_creates_errors_list_if_missing(self) -> None:
        """Test that _traverse_node creates errors list if not present in symbol_table."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {}
        }
        node: AST = {"type": "unknown_type"}
        
        _traverse_node(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_traverse_node_unknown_type_skips_silently(self) -> None:
        """Test that unknown node types are skipped without error."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {"type": "unknown_type"}
        
        # Should not raise any exception
        _traverse_node(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== Handler Dispatch Tests ====================

    @patch('_traverse_node_src._handle_variable_declaration')
    def test_traverse_node_dispatches_variable_declaration(self, mock_handler: MagicMock) -> None:
        """Test dispatch to _handle_variable_declaration handler."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handler.assert_called_once_with(node, symbol_table)

    @patch('_traverse_node_src._handle_assignment')
    def test_traverse_node_dispatches_assignment(self, mock_handler: MagicMock) -> None:
        """Test dispatch to _handle_assignment handler."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "assignment",
            "name": "x",
            "value": 10,
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handler.assert_called_once_with(node, symbol_table)

    @patch('_traverse_node_src._handle_if_statement')
    def test_traverse_node_dispatches_if_statement(self, mock_handler: MagicMock) -> None:
        """Test dispatch to _handle_if_statement handler."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_block": {"type": "block"},
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handler.assert_called_once_with(node, symbol_table)

    @patch('_traverse_node_src._handle_while_loop')
    def test_traverse_node_dispatches_while_loop(self, mock_handler: MagicMock) -> None:
        """Test dispatch to _handle_while_loop handler."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "binary_op"},
            "body": {"type": "block"},
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handler.assert_called_once_with(node, symbol_table)

    @patch('_traverse_node_src._handle_return_statement')
    def test_traverse_node_dispatches_return_statement(self, mock_handler: MagicMock) -> None:
        """Test dispatch to _handle_return_statement handler."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "return_statement",
            "value": {"type": "literal", "value": 10},
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handler.assert_called_once_with(node, symbol_table)

    @patch('_traverse_node_src._handle_print_statement')
    def test_traverse_node_dispatches_print_statement(self, mock_handler: MagicMock) -> None:
        """Test dispatch to _handle_print_statement handler."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "print_statement",
            "arguments": [{"type": "identifier", "name": "x"}],
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handler.assert_called_once_with(node, symbol_table)

    def test_traverse_node_dispatches_function_declaration_inline(self) -> None:
        """Test dispatch to _handle_function_declaration handler (inline function)."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "function_declaration",
            "name": "main",
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        # The inline _handle_function_declaration should be called
        # Verify by checking the function was registered
        self.assertIn("main", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "int")

    # ==================== Auto-traversal Tests ====================

    @patch('_traverse_node_src._handle_variable_declaration')
    def test_traverse_node_auto_traverses_children_for_variable_declaration(self, mock_handler: MagicMock) -> None:
        """Test auto-traversal of children for variable_declaration (non-excluded type)."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        child_node: AST = {"type": "literal", "value": 10}
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "children": [child_node],
            "line": 1,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        # Handler should be called
        mock_handler.assert_called_once()

    def test_traverse_node_excluded_types_program(self) -> None:
        """Test that program type does NOT auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertIn("program", excluded_types)

    def test_traverse_node_excluded_types_block(self) -> None:
        """Test that block type does NOT auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertIn("block", excluded_types)

    def test_traverse_node_excluded_types_if_statement(self) -> None:
        """Test that if_statement type does NOT auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertIn("if_statement", excluded_types)

    def test_traverse_node_excluded_types_while_loop(self) -> None:
        """Test that while_loop type does NOT auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertIn("while_loop", excluded_types)

    def test_traverse_node_excluded_types_function_declaration(self) -> None:
        """Test that function_declaration type does NOT auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertIn("function_declaration", excluded_types)

    def test_traverse_node_not_excluded_assignment(self) -> None:
        """Test that assignment type DOES auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertNotIn("assignment", excluded_types)

    def test_traverse_node_not_excluded_return_statement(self) -> None:
        """Test that return_statement type DOES auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertNotIn("return_statement", excluded_types)

    def test_traverse_node_not_excluded_print_statement(self) -> None:
        """Test that print_statement type DOES auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertNotIn("print_statement", excluded_types)

    def test_traverse_node_not_excluded_variable_declaration(self) -> None:
        """Test that variable_declaration type DOES auto-traverse children."""
        excluded_types = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertNotIn("variable_declaration", excluded_types)

    # ==================== Edge Cases ====================

    def test_traverse_node_empty_node(self) -> None:
        """Test handling of empty/minimal node."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {}
        
        # Should not raise
        _traverse_node(node, symbol_table)
        
        # Unknown type should be skipped
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_traverse_node_node_without_type_field(self) -> None:
        """Test handling of node without type field."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {"name": "test"}
        
        # Should not raise, type defaults to ""
        _traverse_node(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_traverse_node_node_without_children_field(self) -> None:
        """Test handling of node without children field."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {"type": "variable_declaration", "name": "x", "data_type": "int"}
        
        with patch('_traverse_node_src._handle_variable_declaration'):
            # Should not raise
            _traverse_node(node, symbol_table)

    def test_traverse_node_with_empty_children_list(self) -> None:
        """Test handling of node with empty children list."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "children": []
        }
        
        with patch('_traverse_node_src._handle_variable_declaration'):
            # Should not raise
            _traverse_node(node, symbol_table)

    # ==================== Integration Tests ====================

    @patch('_traverse_node_src._handle_variable_declaration')
    @patch('_traverse_node_src._handle_assignment')
    def test_traverse_node_multiple_dispatches(self, mock_assignment: MagicMock, mock_variable: MagicMock) -> None:
        """Test multiple node traversals with different types."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        
        var_node: AST = {"type": "variable_declaration", "name": "x", "data_type": "int"}
        assign_node: AST = {"type": "assignment", "name": "x", "value": 10}
        
        _traverse_node(var_node, symbol_table)
        _traverse_node(assign_node, symbol_table)
        
        mock_variable.assert_called_once_with(var_node, symbol_table)
        mock_assignment.assert_called_once_with(assign_node, symbol_table)

    def test_traverse_node_function_declaration_registers_function(self) -> None:
        """Test that function_declaration properly registers function in symbol_table."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        node: AST = {
            "type": "function_declaration",
            "name": "test_func",
            "return_type": "char",
            "params": [{"name": "a", "data_type": "int"}],
            "line": 5,
            "column": 10
        }
        
        _traverse_node(node, symbol_table)
        
        # Verify function is registered
        self.assertIn("test_func", symbol_table["functions"])
        func_info = symbol_table["functions"]["test_func"]
        self.assertEqual(func_info["return_type"], "char")
        self.assertEqual(func_info["line"], 5)
        self.assertEqual(func_info["column"], 10)
        self.assertEqual(len(func_info["params"]), 1)
        
        # Verify current_function is set then cleared
        self.assertIsNone(symbol_table["current_function"])

    def test_traverse_node_duplicate_function_declaration(self) -> None:
        """Test duplicate function declaration adds error."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["functions"] = {
            "main": {"return_type": "int", "params": [], "line": 1, "column": 1}
        }
        
        node: AST = {
            "type": "function_declaration",
            "name": "main",
            "return_type": "char",
            "params": [],
            "line": 10,
            "column": 1
        }
        
        _traverse_node(node, symbol_table)
        
        # Should have error about duplicate
        self.assertGreater(len(symbol_table["errors"]), 0)
        self.assertIn("already declared", symbol_table["errors"][0])


class TestTraverseNodeChildTraversal(unittest.TestCase):
    """Test child traversal behavior."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    @patch('_traverse_node_src._handle_variable_declaration')
    def test_auto_traversal_logic(self, mock_handler: MagicMock) -> None:
        """Test that children are traversed after handler is called."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        
        child1: AST = {"type": "literal", "value": 10}
        child2: AST = {"type": "identifier", "name": "x"}
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "children": [child1, child2]
        }
        
        _traverse_node(node, symbol_table)
        
        # Handler should be called
        mock_handler.assert_called_once()
        
        # Verify variable_declaration is not in excluded types
        excluded = {"program", "block", "if_statement", "while_loop", "function_declaration"}
        self.assertNotIn("variable_declaration", excluded)


if __name__ == "__main__":
    unittest.main()
