"""Unit tests for _verify_assignment function."""
import unittest
from unittest.mock import patch

from . import _verify_assignment_src


class TestVerifyAssignment(unittest.TestCase):
    """Test cases for _verify_assignment function."""

    def setUp(self):
        """Set up test fixtures."""
        self.filename = "test_file.py"
        self.context_stack = []
        
    def test_happy_path_valid_assignment(self):
        """Test valid assignment with matching types."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 10, "column": 5},
            "value": {"data_type": "int", "line": 10, "column": 9},
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node') as mock_verify_node:
            _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
        mock_verify_node.assert_called_once_with(
            node["value"], symbol_table, self.context_stack, self.filename
        )
    
    def test_value_without_data_type_raises_error(self):
        """Test assignment where value has no data_type raises ValueError."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 15, "column": 3},
            "value": {"line": 15, "column": 7},
            "line": 15,
            "column": 3
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            self.assertEqual(str(context.exception), f"{self.filename}:15:3: error: unable to determine type of assignment value")
    
    def test_undefined_variable_raises_error(self):
        """Test assignment to undefined variable raises ValueError."""
        node = {
            "type": "assignment",
            "target": {"name": "y", "line": 20, "column": 1},
            "value": {"data_type": "str", "line": 20, "column": 5},
            "line": 20,
            "column": 1
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            self.assertEqual(str(context.exception), f"{self.filename}:20:1: error: undefined variable 'y'")
    
    def test_type_mismatch_raises_error(self):
        """Test assignment with type mismatch raises ValueError."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 25, "column": 2},
            "value": {"data_type": "str", "line": 25, "column": 6},
            "line": 25,
            "column": 2
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            self.assertEqual(str(context.exception), f"{self.filename}:25:2: error: type mismatch in assignment, expected int but got str")
    
    def test_uses_target_line_column_when_available(self):
        """Test that target line/column takes precedence over node line/column."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 30, "column": 4},
            "value": {"data_type": "int", "line": 100, "column": 100},
            "line": 99,
            "column": 99
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                # Make value_type None to trigger error with target's line/column
                node["value"] = {"line": 100, "column": 100}
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            self.assertEqual(str(context.exception), f"{self.filename}:30:4: error: unable to determine type of assignment value")
    
    def test_falls_back_to_node_line_column(self):
        """Test that node line/column is used when target doesn't have them."""
        node = {
            "type": "assignment",
            "target": {"name": "x"},
            "value": {"data_type": "int"},
            "line": 35,
            "column": 6
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "str", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            self.assertEqual(str(context.exception), f"{self.filename}:35:6: error: type mismatch in assignment, expected str but got int")
    
    def test_verify_node_called_with_correct_arguments(self):
        """Test that _verify_node is called with the value node and correct context."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 40, "column": 1},
            "value": {"data_type": "int", "line": 40, "column": 5},
            "line": 40,
            "column": 1
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        context_stack = [{"type": "function", "name": "main", "return_type": "int"}]
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node') as mock_verify_node:
            _verify_assignment_src._verify_assignment(node, symbol_table, context_stack, self.filename)
            
        mock_verify_node.assert_called_once_with(
            node["value"], symbol_table, context_stack, self.filename
        )
    
    def test_exact_string_type_matching(self):
        """Test that type matching uses exact string equality."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 45, "column": 1},
            "value": {"data_type": "Integer", "line": 45, "column": 5},
            "line": 45,
            "column": 1
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "scope": 0}
            },
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            # "Integer" != "int" should fail
            self.assertEqual(str(context.exception), f"{self.filename}:45:1: error: type mismatch in assignment, expected int but got Integer")
    
    def test_empty_symbol_table_raises_undefined_variable(self):
        """Test assignment with empty variables dict raises undefined variable error."""
        node = {
            "type": "assignment",
            "target": {"name": "x", "line": 50, "column": 1},
            "value": {"data_type": "int", "line": 50, "column": 5},
            "line": 50,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        with patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_node_src._verify_node'):
            with self.assertRaises(ValueError) as context:
                _verify_assignment_src._verify_assignment(node, symbol_table, self.context_stack, self.filename)
            
            self.assertEqual(str(context.exception), f"{self.filename}:50:1: error: undefined variable 'x'")


if __name__ == "__main__":
    unittest.main()
