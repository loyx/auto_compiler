import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._handle_assignment_src import _handle_assignment, _get_expression_type


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function"""
    
    def test_valid_assignment_same_type_int(self):
        """Test valid assignment where both variable and expression are int type"""
        node = {
            "type": "assignment",
            "target": "x",
            "expression": {"type": "literal", "value": 5, "data_type": "int", "line": 1, "column": 1},
            "line": 1,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_assignment_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_assignment(node, symbol_table)
            
            mock_traverse.assert_called_once()
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_valid_assignment_same_type_char(self):
        """Test valid assignment where both variable and expression are char type"""
        node = {
            "type": "assignment",
            "target": "y",
            "expression": {"type": "literal", "value": "a", "data_type": "char", "line": 2, "column": 3},
            "line": 2,
            "column": 3
        }
        
        symbol_table = {
            "variables": {
                "y": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_assignment_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_assignment(node, symbol_table)
            
            mock_traverse.assert_called_once()
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_undefined_variable(self):
        """Test assignment to undeclared variable"""
        node = {
            "type": "assignment",
            "target": "z",
            "expression": {"type": "literal", "value": 10, "data_type": "int", "line": 5, "column": 10},
            "line": 5,
            "column": 10
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Assignment to undeclared variable 'z'")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
        self.assertEqual(error["type"], "undefined_variable")
    
    def test_type_mismatch_int_to_char(self):
        """Test type mismatch: assigning int to char variable"""
        node = {
            "type": "assignment",
            "target": "x",
            "expression": {"type": "literal", "value": 42, "data_type": "int", "line": 3, "column": 5},
            "line": 3,
            "column": 5
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_assignment_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_assignment(node, symbol_table)
            
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["message"], "Type mismatch: expected 'char' but got 'int'")
            self.assertEqual(error["line"], 3)
            self.assertEqual(error["column"], 5)
            self.assertEqual(error["type"], "type_mismatch")
    
    def test_type_mismatch_char_to_int(self):
        """Test type mismatch: assigning char to int variable"""
        node = {
            "type": "assignment",
            "target": "count",
            "expression": {"type": "literal", "value": "c", "data_type": "char", "line": 7, "column": 2},
            "line": 7,
            "column": 2
        }
        
        symbol_table = {
            "variables": {
                "count": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_assignment_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_assignment(node, symbol_table)
            
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["message"], "Type mismatch: expected 'int' but got 'char'")
            self.assertEqual(error["line"], 7)
            self.assertEqual(error["column"], 2)
            self.assertEqual(error["type"], "type_mismatch")
    
    def test_initializes_errors_list_if_missing(self):
        """Test that errors list is initialized if not present in symbol_table"""
        node = {
            "type": "assignment",
            "target": "missing_var",
            "expression": {"type": "literal", "value": 1, "data_type": "int", "line": 1, "column": 1},
            "line": 1,
            "column": 1
        }
        
        symbol_table = {
            "variables": {}
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "undefined_variable")
    
    def test_expression_is_none(self):
        """Test handling when expression is None"""
        node = {
            "type": "assignment",
            "target": "x",
            "expression": None,
            "line": 4,
            "column": 6
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_expression_without_data_type_uses_type_field_int(self):
        """Test expression type inference from type field containing 'int'"""
        node = {
            "type": "assignment",
            "target": "x",
            "expression": {"type": "int_literal", "value": 100, "line": 1, "column": 1},
            "line": 1,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_assignment_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_assignment(node, symbol_table)
            
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_expression_without_data_type_uses_type_field_char(self):
        """Test expression type inference from type field containing 'char'"""
        node = {
            "type": "assignment",
            "target": "c",
            "expression": {"type": "char_literal", "value": "x", "line": 2, "column": 2},
            "line": 2,
            "column": 2
        }
        
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_assignment_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_assignment(node, symbol_table)
            
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_default_line_column_values(self):
        """Test that default line and column values are used when not provided"""
        node = {
            "type": "assignment",
            "target": "undefined",
            "expression": {"type": "literal", "value": 5, "data_type": "int"}
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)


class TestGetExpressionType(unittest.TestCase):
    """Test cases for _get_expression_type helper function"""
    
    def test_returns_data_type_when_present(self):
        """Test that data_type field is returned when present"""
        expression = {"type": "literal", "data_type": "int", "value": 42}
        self.assertEqual(_get_expression_type(expression), "int")
        
        expression = {"type": "literal", "data_type": "char", "value": "a"}
        self.assertEqual(_get_expression_type(expression), "char")
    
    def test_infers_int_from_type_field(self):
        """Test type inference from type field containing 'int'"""
        expression = {"type": "int_literal", "value": 10}
        self.assertEqual(_get_expression_type(expression), "int")
        
        expression = {"type": "int_expression", "value": 20}
        self.assertEqual(_get_expression_type(expression), "int")
    
    def test_infers_char_from_type_field(self):
        """Test type inference from type field containing 'char'"""
        expression = {"type": "char_literal", "value": "x"}
        self.assertEqual(_get_expression_type(expression), "char")
        
        expression = {"type": "char_expression", "value": "y"}
        self.assertEqual(_get_expression_type(expression), "char")
    
    def test_returns_none_when_no_type_info(self):
        """Test that None is returned when no type information is available"""
        expression = {"type": "unknown", "value": "something"}
        self.assertIsNone(_get_expression_type(expression))
        
        expression = {"value": 123}
        self.assertIsNone(_get_expression_type(expression))
    
    def test_returns_none_for_none_input(self):
        """Test that None is returned when expression is None"""
        self.assertIsNone(_get_expression_type(None))


if __name__ == '__main__':
    unittest.main()
