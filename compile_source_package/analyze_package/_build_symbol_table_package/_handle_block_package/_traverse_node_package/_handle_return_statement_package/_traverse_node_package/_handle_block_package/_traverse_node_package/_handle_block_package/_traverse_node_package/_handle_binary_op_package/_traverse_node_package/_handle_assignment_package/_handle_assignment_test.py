import unittest
from typing import Any, Dict

from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: Dict[str, Any] = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
                "y": {"data_type": "char", "is_declared": True, "line": 2, "column": 1, "scope_level": 0},
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    def test_valid_assignment_same_type(self):
        """Test valid assignment with matching types."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_valid_assignment_char_type(self):
        """Test valid assignment for char type variable."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "y",
            "data_type": "char",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_missing_value_field(self):
        """Test assignment node without value field."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["message"], 
                         "Missing value field in assignment node")
        self.assertEqual(self.symbol_table["errors"][0]["line"], 5)
        self.assertEqual(self.symbol_table["errors"][0]["column"], 10)
    
    def test_missing_value_field_default_location(self):
        """Test assignment node without value field and no line/column."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "data_type": "int",
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["line"], -1)
        self.assertEqual(self.symbol_table["errors"][0]["column"], -1)
    
    def test_undeclared_variable(self):
        """Test assignment to variable not in symbol table."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["message"], 
                         "Assignment to undeclared variable: z")
        self.assertEqual(self.symbol_table["errors"][0]["line"], 5)
        self.assertEqual(self.symbol_table["errors"][0]["column"], 10)
    
    def test_type_mismatch_int_to_char(self):
        """Test assignment with type mismatch: int variable assigned char."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "char",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["message"], 
                         "Type mismatch in assignment: expected int, got char")
    
    def test_type_mismatch_char_to_int(self):
        """Test assignment with type mismatch: char variable assigned int."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "y",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["message"], 
                         "Type mismatch in assignment: expected char, got int")
    
    def test_no_data_type_no_error(self):
        """Test assignment without data_type field does not cause type error."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_variable_without_data_type(self):
        """Test assignment to variable without data_type in symbol table."""
        symbol_table: Dict[str, Any] = {
            "variables": {
                "z": {"is_declared": True, "line": 1, "column": 1, "scope_level": 0},
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_empty_children(self):
        """Test assignment with empty children list."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_literal_children_ignored(self):
        """Test that literal nodes in children are ignored."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [
                {
                    "type": "literal",
                    "value": 42,
                    "line": 5,
                    "column": 15
                }
            ]
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_identifier_child_undeclared(self):
        """Test processing children containing undeclared variable reference."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [
                {
                    "type": "identifier",
                    "value": "z",
                    "line": 5,
                    "column": 15
                }
            ]
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["message"], 
                         "Use of undeclared variable: z")
    
    def test_identifier_child_declared(self):
        """Test processing children containing declared variable reference."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [
                {
                    "type": "identifier",
                    "value": "y",
                    "line": 5,
                    "column": 15
                }
            ]
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_nested_children_with_undeclared(self):
        """Test processing nested children with undeclared variable."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [
                {
                    "type": "binary_op",
                    "value": "+",
                    "children": [
                        {
                            "type": "identifier",
                            "value": "z",
                            "line": 5,
                            "column": 15
                        },
                        {
                            "type": "literal",
                            "value": 1,
                            "line": 5,
                            "column": 17
                        }
                    ]
                }
            ]
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(self.symbol_table["errors"][0]["message"], 
                         "Use of undeclared variable: z")
    
    def test_multiple_errors_accumulated(self):
        """Test that multiple errors are accumulated in symbol table."""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": [{"type": "error", "message": "Previous error", "line": 1, "column": 1}]
        }
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
    
    def test_empty_symbol_table_variables(self):
        """Test assignment when symbol_table has no variables key."""
        symbol_table: Dict[str, Any] = {
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], 
                         "Assignment to undeclared variable: x")
    
    def test_no_errors_key_created(self):
        """Test that errors key is created when not present."""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_non_dict_child_ignored(self):
        """Test that non-dict children are ignored."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [None, "string", 123]
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
