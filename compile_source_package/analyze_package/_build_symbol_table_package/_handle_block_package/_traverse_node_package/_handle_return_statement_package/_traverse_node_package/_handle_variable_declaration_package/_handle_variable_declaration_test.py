# Test file for _handle_variable_declaration
import unittest
from unittest.mock import patch

# Relative import from the same package
from ._handle_variable_declaration_src import _handle_variable_declaration


class TestHandleVariableDeclaration(unittest.TestCase):
    """Test cases for _handle_variable_declaration function."""
    
    def test_valid_int_declaration(self):
        """Test valid int variable declaration."""
        node = {
            "type": "variable_declaration",
            "name": "var1",
            "variable_type": "int",
            "line": 1,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify variable was registered
        self.assertIn("var1", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["var1"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["var1"]["scope_level"], 0)
        self.assertEqual(symbol_table["variables"]["var1"]["line"], 1)
        self.assertEqual(symbol_table["variables"]["var1"]["column"], 5)
        self.assertTrue(symbol_table["variables"]["var1"]["is_declared"])
    
    def test_valid_char_declaration(self):
        """Test valid char variable declaration."""
        node = {
            "type": "variable_declaration",
            "name": "charVar",
            "variable_type": "char",
            "line": 5,
            "column": 10
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify variable was registered
        self.assertIn("charVar", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["charVar"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["charVar"]["scope_level"], 0)
    
    def test_invalid_type_records_error(self):
        """Test that invalid variable type records an error."""
        node = {
            "type": "variable_declaration",
            "name": "badVar",
            "variable_type": "float",
            "line": 3,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify error was recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Invalid variable type", symbol_table["errors"][0])
        self.assertIn("float", symbol_table["errors"][0])
        # Variable should NOT be registered
        self.assertNotIn("badVar", symbol_table["variables"])
    
    def test_duplicate_declaration_same_scope_records_error(self):
        """Test that duplicate declaration in same scope records an error."""
        node = {
            "type": "variable_declaration",
            "name": "dupVar",
            "variable_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {
                "dupVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify error was recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("already declared", symbol_table["errors"][0])
        # Original variable info should remain unchanged
        self.assertEqual(symbol_table["variables"]["dupVar"]["line"], 5)
    
    def test_variable_shadowing_different_scope_allowed(self):
        """Test that variable shadowing in different scope is allowed."""
        node = {
            "type": "variable_declaration",
            "name": "shadowVar",
            "variable_type": "int",
            "line": 15,
            "column": 5
        }
        symbol_table = {
            "variables": {
                "shadowVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "current_scope": 1  # Different scope level
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Should NOT record error (shadowing is allowed)
        self.assertNotIn("errors", symbol_table)
        # Variable should be updated to new scope
        self.assertEqual(symbol_table["variables"]["shadowVar"]["line"], 15)
        self.assertEqual(symbol_table["variables"]["shadowVar"]["scope_level"], 1)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._traverse_node')
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._infer_expression_type')
    def test_initial_value_traversed(self, mock_infer_type, mock_traverse):
        """Test that initial value expression is traversed."""
        initial_value = {"type": "literal", "value": 42}
        node = {
            "type": "variable_declaration",
            "name": "varWithInit",
            "variable_type": "int",
            "initial_value": initial_value,
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        mock_traverse.return_value = None
        mock_infer_type.return_value = "int"
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify traverse_node was called with initial_value
        mock_traverse.assert_called_once_with(initial_value, symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._traverse_node')
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._infer_expression_type')
    def test_type_mismatch_records_error(self, mock_infer_type, mock_traverse):
        """Test that type mismatch in initial value records an error."""
        initial_value = {"type": "literal", "value": "hello"}
        node = {
            "type": "variable_declaration",
            "name": "typeMismatchVar",
            "variable_type": "int",
            "initial_value": initial_value,
            "line": 7,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        mock_traverse.return_value = None
        mock_infer_type.return_value = "char"  # Inferred type doesn't match declared type
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify error was recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch", symbol_table["errors"][0])
        self.assertIn("expected int but got char", symbol_table["errors"][0])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._traverse_node')
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._infer_expression_type')
    def test_type_match_no_error(self, mock_infer_type, mock_traverse):
        """Test that matching types don't record an error."""
        initial_value = {"type": "literal", "value": 42}
        node = {
            "type": "variable_declaration",
            "name": "typeMatchVar",
            "variable_type": "int",
            "initial_value": initial_value,
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        mock_traverse.return_value = None
        mock_infer_type.return_value = "int"  # Matches declared type
        
        _handle_variable_declaration(node, symbol_table)
        
        # Should NOT record error
        self.assertNotIn("errors", symbol_table)
        # Variable should be registered
        self.assertIn("typeMatchVar", symbol_table["variables"])
    
    def test_missing_variable_type_field(self):
        """Test handling when variable_type field is missing."""
        node = {
            "type": "variable_declaration",
            "name": "noTypeVar",
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Should record error for invalid/missing type
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Invalid variable type", symbol_table["errors"][0])
    
    def test_data_type_fallback(self):
        """Test that data_type is used as fallback when variable_type is missing."""
        node = {
            "type": "variable_declaration",
            "name": "fallbackVar",
            "data_type": "int",  # Using data_type instead of variable_type
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Variable should be registered with data_type
        self.assertIn("fallbackVar", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["fallbackVar"]["data_type"], "int")
    
    def test_missing_line_column_defaults(self):
        """Test that missing line/column default to 0."""
        node = {
            "type": "variable_declaration",
            "name": "noLineColVar",
            "variable_type": "int"
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Variable should be registered with default line/column
        self.assertIn("noLineColVar", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["noLineColVar"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["noLineColVar"]["column"], 0)
    
    def test_empty_symbol_table_initialized(self):
        """Test that function initializes missing symbol_table fields."""
        node = {
            "type": "variable_declaration",
            "name": "initVar",
            "variable_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table = {}  # Empty symbol table
        
        _handle_variable_declaration(node, symbol_table)
        
        # Symbol table should be initialized
        self.assertIn("variables", symbol_table)
        self.assertIn("initVar", symbol_table["variables"])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._infer_expression_type')
    def test_unknown_inferred_type_no_error(self, mock_infer_type):
        """Test that 'unknown' inferred type doesn't trigger type mismatch error."""
        initial_value = {"type": "complex_expression"}
        node = {
            "type": "variable_declaration",
            "name": "unknownTypeVar",
            "variable_type": "int",
            "initial_value": initial_value,
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        mock_infer_type.return_value = "unknown"
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_variable_declaration_package._handle_variable_declaration_src._traverse_node'):
            _handle_variable_declaration(node, symbol_table)
        
        # Should NOT record error for unknown type
        self.assertNotIn("errors", symbol_table)


if __name__ == "__main__":
    unittest.main()
