import unittest
from unittest.mock import patch
import sys
import os

# Add parent directories to path for absolute imports
_base_dir = os.path.dirname(os.path.abspath(__file__))
for _ in range(10):
    sys.path.insert(0, _base_dir)
    _base_dir = os.path.dirname(_base_dir)

# Import from the same package
from _handle_assignment_package._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
                "y": {"data_type": "char", "is_declared": True, "line": 2, "column": 1, "scope_level": 0},
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "errors": []
        }
    
    def test_happy_path_matching_types(self):
        """Test assignment with declared variable and matching types."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
        mock_traverse.assert_called_once()
    
    def test_undeclared_variable(self):
        """Test assignment to undeclared variable."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable")
        self.assertIn("z", error["message"])
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
    
    def test_type_mismatch(self):
        """Test assignment with type mismatch."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": "a", "data_type": "char", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_mismatch")
        self.assertIn("char", error["message"])
        self.assertIn("int", error["message"])
        self.assertIn("x", error["message"])
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
    
    def test_missing_children(self):
        """Test assignment node with insufficient children."""
        node = {
            "type": "assignment",
            "children": [],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_non_identifier_target(self):
        """Test assignment with non-identifier target."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "literal", "value": 5, "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_missing_variable_name(self):
        """Test assignment with missing variable name in identifier."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": None, "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_empty_variable_name(self):
        """Test assignment with empty variable name."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_traverse_node_called_for_expression(self):
        """Test that _traverse_node is called for the expression node."""
        expression_node = {"type": "binary_op", "value": "+", "data_type": "int"}
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                expression_node
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)
        
        mock_traverse.assert_called_once_with(expression_node, self.symbol_table)
    
    def test_no_error_when_types_match_char(self):
        """Test assignment with char types matching."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "y", "line": 5, "column": 10},
                {"type": "literal", "value": "a", "data_type": "char", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_error_format_structure(self):
        """Test that error has correct structure."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, self.symbol_table)
        
        error = self.symbol_table["errors"][0]
        self.assertIn("message", error)
        self.assertIn("line", error)
        self.assertIn("column", error)
        self.assertIn("type", error)
        self.assertIsInstance(error["message"], str)
    
    def test_multiple_errors_accumulated(self):
        """Test that multiple errors are accumulated."""
        self.symbol_table["errors"] = [{"message": "existing error", "line": 1, "column": 1, "type": "other"}]
        
        node1 = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        node2 = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "w", "line": 6, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 6, "column": 15}
            ],
            "line": 6,
            "column": 10
        }
        
        _handle_assignment(node1, self.symbol_table)
        _handle_assignment(node2, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 3)
    
    def test_missing_line_column_info(self):
        """Test assignment node without line/column info."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z"},
                {"type": "literal", "value": 42, "data_type": "int"}
            ]
        }
        
        _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], "?")
        self.assertEqual(error["column"], "?")
    
    def test_variable_without_data_type(self):
        """Test assignment when variable has no data_type."""
        self.symbol_table["variables"]["no_type"] = {"is_declared": True, "line": 1, "column": 1, "scope_level": 0}
        
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "no_type", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_expression_without_data_type(self):
        """Test assignment when expression has no data_type."""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_symbol_table_without_errors_key(self):
        """Test that errors key is created if not present."""
        symbol_table_no_errors = {
            "variables": {
                "z": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
            },
            "functions": {},
        }
        
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 5, "column": 10},
                {"type": "literal", "value": "a", "data_type": "char", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table_no_errors)
        
        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)
    
    def test_symbol_table_without_variables_key(self):
        """Test that function handles missing variables key gracefully."""
        symbol_table_no_vars = {
            "functions": {},
            "current_scope": 0,
        }
        
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "data_type": "int", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        _handle_assignment(node, symbol_table_no_vars)
        
        self.assertEqual(len(symbol_table_no_vars.get("errors", [])), 1)


if __name__ == "__main__":
    unittest.main()
