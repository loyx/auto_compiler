# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# === relative imports ===
from ._handle_return_statement_src import _handle_return_statement, AST, SymbolTable


class TestHandleReturnStatement(unittest.TestCase):
    """Test cases for _handle_return_statement function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": None,
            "errors": []
        }

    def test_return_outside_function(self) -> None:
        """Test return statement when not inside a function."""
        node: AST = {
            "type": "return_statement",
            "line": 10,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("return statement outside function at line 10", self.symbol_table["errors"])

    def test_function_not_in_symbol_table(self) -> None:
        """Test return statement when current function is not in symbol table."""
        self.symbol_table["current_function"] = "nonexistent_func"
        
        node: AST = {
            "type": "return_statement",
            "line": 15,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("function 'nonexistent_func' not found in symbol table at line 15", 
                     self.symbol_table["errors"])

    def test_return_type_mismatch(self) -> None:
        """Test return statement with type mismatch."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 20,
            "column": 5,
            "children": [],
            "value": None,
            "data_type": "char"
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Return type mismatch: expected int but got char at line 20", 
                     self.symbol_table["errors"])

    def test_void_return_for_non_void_function(self) -> None:
        """Test void return when function expects non-void return type."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 25,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Function 'my_func' expects return type int but got void at line 25", 
                     self.symbol_table["errors"])

    def test_valid_return_with_matching_type(self) -> None:
        """Test valid return statement with matching type."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 30,
            "column": 5,
            "children": [],
            "value": None,
            "data_type": "int"
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_valid_void_return_for_void_function(self) -> None:
        """Test valid void return for void function."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "void",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 35,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_return_type_from_child_node(self) -> None:
        """Test return type detection from child node's data_type."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "char",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 40,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "char",
                    "value": "'a'"
                }
            ],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_return_type_mismatch_from_child_node(self) -> None:
        """Test return type mismatch detection from child node's data_type."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 45,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "char",
                    "value": "'a'"
                }
            ],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("Return type mismatch: expected int but got char at line 45", 
                     self.symbol_table["errors"])

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_return_statement_package._handle_return_statement_src._traverse_node')
    def test_children_traversal(self, mock_traverse: MagicMock) -> None:
        """Test that children nodes are traversed recursively."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        child_node: Dict[str, Any] = {
            "type": "expression",
            "data_type": "int",
            "value": 42
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 50,
            "column": 5,
            "children": [child_node],
            "value": None,
            "data_type": "int"
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called for each child
        mock_traverse.assert_called_once_with(child_node, self.symbol_table)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_return_statement_package._handle_return_statement_src._traverse_node')
    def test_multiple_children_traversal(self, mock_traverse: MagicMock) -> None:
        """Test that multiple children nodes are traversed."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        child_node1: Dict[str, Any] = {
            "type": "expression",
            "data_type": "int",
            "value": 42
        }
        
        child_node2: Dict[str, Any] = {
            "type": "binary_op",
            "data_type": "int",
            "value": "+"
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 55,
            "column": 5,
            "children": [child_node1, child_node2],
            "value": None,
            "data_type": "int"
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called for each child
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call(child_node1, self.symbol_table)
        mock_traverse.assert_any_call(child_node2, self.symbol_table)

    def test_no_errors_list_initialized(self) -> None:
        """Test when errors list is not pre-initialized in symbol table."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        # Remove errors key
        if "errors" in self.symbol_table:
            del self.symbol_table["errors"]
        
        node: AST = {
            "type": "return_statement",
            "line": 60,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        # Should still work and create errors list
        self.assertIn("errors", self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    def test_node_without_line_number(self) -> None:
        """Test return statement without line number (defaults to 0)."""
        node: AST = {
            "type": "return_statement",
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("return statement outside function at line 0", self.symbol_table["errors"])

    def test_function_with_none_return_type(self) -> None:
        """Test void return when function has None as return type."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": None,
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 70,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        # None return type should be treated as void
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_function_with_empty_return_type(self) -> None:
        """Test void return when function has empty string as return type."""
        self.symbol_table["current_function"] = "my_func"
        self.symbol_table["functions"] = {
            "my_func": {
                "return_type": "",
                "params": [],
                "line": 1,
                "column": 1
            }
        }
        
        node: AST = {
            "type": "return_statement",
            "line": 75,
            "column": 5,
            "children": [],
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        # Empty return type should be treated as void
        self.assertEqual(len(self.symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
