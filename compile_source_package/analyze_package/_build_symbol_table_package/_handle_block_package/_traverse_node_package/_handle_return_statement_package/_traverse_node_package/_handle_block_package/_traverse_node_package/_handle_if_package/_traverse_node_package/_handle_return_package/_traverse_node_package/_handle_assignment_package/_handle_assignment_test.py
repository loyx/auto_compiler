# -*- coding: utf-8 -*-
"""
Unit tests for _handle_assignment function.
"""
import unittest
from typing import Any, Dict

# Import the function under test using relative import
from ._handle_assignment_src import _handle_assignment

# Type aliases for test clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_value_with_data_type_field(self):
        """Test when value node already has data_type field."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "data_type": "int", "literal_type": "int"}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "int")

    def test_literal_value_with_literal_type(self):
        """Test literal value node with literal_type field."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "literal_type": "str"}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "str")

    def test_literal_value_without_literal_type(self):
        """Test literal value node without literal_type field (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal"}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_identifier_found_in_symbol_table(self):
        """Test identifier value found in symbol table."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "identifier", "name": "y"}
        }
        symbol_table: SymbolTable = {
            "variables": {
                "y": {"type": "float", "scope": 1}
            },
            "functions": {}
        }
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "float")

    def test_identifier_not_found_in_symbol_table(self):
        """Test identifier value not found in symbol table (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "identifier", "name": "undefined_var"}
        }
        symbol_table: SymbolTable = {
            "variables": {
                "y": {"type": "float"}
            },
            "functions": {}
        }
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_identifier_with_empty_symbol_table(self):
        """Test identifier value with empty symbol table (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "identifier", "name": "y"}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_binary_op_value(self):
        """Test binary_op value node (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {
                "type": "binary_op",
                "operator": "+",
                "left": {"type": "literal", "literal_type": "int"},
                "right": {"type": "literal", "literal_type": "int"}
            }
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_function_call_value(self):
        """Test function_call value node (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {
                "type": "function_call",
                "name": "print",
                "args": []
            }
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_value_is_none(self):
        """Test when value is None (returns 'void')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": None
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "void")

    def test_value_key_missing(self):
        """Test when value key is missing from node (returns 'void')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "void")

    def test_unknown_value_type(self):
        """Test unknown value type (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "unknown_type"}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_empty_value_type_string(self):
        """Test empty value type string (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": ""}
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_symbol_table_missing_variables_key(self):
        """Test when symbol_table is missing 'variables' key."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "identifier", "name": "y"}
        }
        symbol_table: SymbolTable = {"functions": {}}
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_identifier_without_name_field(self):
        """Test identifier value without name field (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "identifier"}
        }
        symbol_table: SymbolTable = {
            "variables": {
                "y": {"type": "int"}
            },
            "functions": {}
        }
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")

    def test_variable_without_type_field(self):
        """Test variable in symbol table without type field (returns 'any')."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "identifier", "name": "y"}
        }
        symbol_table: SymbolTable = {
            "variables": {
                "y": {"scope": 1, "line": 10}
            },
            "functions": {}
        }
        
        result = _handle_assignment(node, symbol_table)
        
        self.assertEqual(result, "any")


if __name__ == "__main__":
    unittest.main()
