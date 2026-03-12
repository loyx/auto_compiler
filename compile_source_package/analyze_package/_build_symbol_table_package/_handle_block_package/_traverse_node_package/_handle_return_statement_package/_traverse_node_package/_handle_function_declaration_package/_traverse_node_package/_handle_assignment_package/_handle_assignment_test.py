"""
Unit tests for _handle_assignment function.
Tests variable declaration validation in assignment nodes.
"""

import unittest
from typing import Any, Dict

# Import the function under test using relative import
from ._handle_assignment_src import _handle_assignment


# Type aliases for clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_variable_declared_no_error(self):
        """Happy path: variable is declared, no error should be added."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_not_declared_adds_error(self):
        """Error case: variable not declared, error should be added."""
        node: AST = {
            "type": "assignment",
            "value": "y",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Error: Variable 'y' used without declaration at line 15, column 8", 
                      symbol_table["errors"])

    def test_empty_symbol_table_initializes_fields(self):
        """Edge case: empty symbol_table should have fields initialized."""
        node: AST = {
            "type": "assignment",
            "value": "z",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {}
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_variable_name_from_name_field(self):
        """Edge case: variable name extracted from 'name' field when 'value' is absent."""
        node: AST = {
            "type": "assignment",
            "name": "counter",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Error: Variable 'counter' used without declaration at line 25, column 10", 
                      symbol_table["errors"])

    def test_variable_name_value_takes_precedence_over_name(self):
        """Edge case: 'value' field takes precedence over 'name' field."""
        node: AST = {
            "type": "assignment",
            "value": "priority_var",
            "name": "ignored_var",
            "line": 30,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Error: Variable 'priority_var' used without declaration at line 30, column 12", 
                      symbol_table["errors"])

    def test_missing_line_column_defaults_to_zero(self):
        """Edge case: missing line/column should default to 0 in error message."""
        node: AST = {
            "type": "assignment",
            "value": "missing_loc"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Error: Variable 'missing_loc' used without declaration at line 0, column 0", 
                      symbol_table["errors"])

    def test_existing_errors_preserved(self):
        """Edge case: existing errors in symbol_table should be preserved."""
        node: AST = {
            "type": "assignment",
            "value": "new_error",
            "line": 35,
            "column": 7
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": ["Existing error message"]
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0], "Existing error message")
        self.assertIn("Error: Variable 'new_error' used without declaration at line 35, column 7", 
                      symbol_table["errors"])

    def test_multiple_assignments_same_undeclared_variable(self):
        """Edge case: multiple assignments to same undeclared variable add multiple errors."""
        node1: AST = {
            "type": "assignment",
            "value": "dup_var",
            "line": 40,
            "column": 1
        }
        node2: AST = {
            "type": "assignment",
            "value": "dup_var",
            "line": 41,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_declared_variable_with_other_variables_present(self):
        """Happy path: declared variable among other variables, no error."""
        node: AST = {
            "type": "assignment",
            "value": "target",
            "line": 50,
            "column": 15
        }
        symbol_table: SymbolTable = {
            "variables": {
                "other1": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
                "target": {"data_type": "char", "is_declared": True, "line": 2, "column": 2, "scope_level": 0},
                "other2": {"data_type": "int", "is_declared": True, "line": 3, "column": 3, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
