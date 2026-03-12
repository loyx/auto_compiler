import unittest
from unittest.mock import patch

# Relative import from the same package
from ._handle_while_src import _handle_while


class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function."""
    
    def test_happy_path_valid_while(self):
        """Test valid while node with int condition."""
        node = {
            "type": "while",
            "line": 10,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 10,
                    "column": 10
                },
                {
                    "type": "block",
                    "line": 11,
                    "column": 5,
                    "children": []
                }
            ]
        }
        
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)
            
            mock_traverse.assert_called_once()
            called_node = mock_traverse.call_args[0][0]
            self.assertEqual(called_node["type"], "block")
            
            self.assertEqual(len(symbol_table["errors"]), 0)
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["scope_stack"]), 0)
    
    def test_missing_children(self):
        """Test while node with insufficient children."""
        node = {
            "type": "while",
            "line": 10,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 10,
                    "column": 10
                }
            ]
        }
        
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)
            
            mock_traverse.assert_not_called()
            
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["line"], 10)
            self.assertEqual(error["column"], 5)
            self.assertEqual(error["message"], "while node must have condition and body children")
            
            self.assertEqual(symbol_table["current_scope"], 0)
    
    def test_wrong_condition_type(self):
        """Test while node with non-int condition type."""
        node = {
            "type": "while",
            "line": 10,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "char",
                    "line": 10,
                    "column": 10
                },
                {
                    "type": "block",
                    "line": 11,
                    "column": 5,
                    "children": []
                }
            ]
        }
        
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)
            
            mock_traverse.assert_not_called()
            
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["line"], 10)
            self.assertEqual(error["column"], 10)
            self.assertEqual(error["message"], "while condition must be int type, got char")
            
            self.assertEqual(symbol_table["current_scope"], 0)
    
    def test_scope_management(self):
        """Test scope entering and exiting."""
        node = {
            "type": "while",
            "line": 10,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 10,
                    "column": 10
                },
                {
                    "type": "block",
                    "line": 11,
                    "column": 5,
                    "children": []
                }
            ]
        }
        
        symbol_table = {
            "variables": {},
            "current_scope": 2,
            "scope_stack": [0, 1],
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)
            
            mock_traverse.assert_called_once()
            
            self.assertEqual(len(symbol_table["errors"]), 0)
            self.assertEqual(symbol_table["current_scope"], 2)
            self.assertEqual(symbol_table["scope_stack"], [0, 1])
    
    def test_error_list_creation(self):
        """Test that errors list is created if not present."""
        node = {
            "type": "while",
            "line": 10,
            "column": 5,
            "children": []
        }
        
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)
            
            self.assertIn("errors", symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_scope_fields_initialization(self):
        """Test that scope fields are initialized if not present."""
        node = {
            "type": "while",
            "line": 10,
            "column": 5,
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 10,
                    "column": 10
                },
                {
                    "type": "block",
                    "line": 11,
                    "column": 5,
                    "children": []
                }
            ]
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)
            
            self.assertIn("scope_stack", symbol_table)
            self.assertIn("current_scope", symbol_table)
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["scope_stack"]), 0)
    
    def test_error_message_includes_actual_type(self):
        """Test error message includes the actual data type."""
        for wrong_type in ["char", "float", "void", None]:
            node = {
                "type": "while",
                "line": 10,
                "column": 5,
                "children": [
                    {
                        "type": "expression",
                        "data_type": wrong_type,
                        "line": 10,
                        "column": 10
                    },
                    {
                        "type": "block",
                        "line": 11,
                        "column": 5,
                        "children": []
                    }
                ]
            }
            
            symbol_table = {
                "variables": {},
                "current_scope": 0,
                "scope_stack": [],
                "errors": []
            }
            
            with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
                _handle_while(node, symbol_table)
                
                self.assertEqual(len(symbol_table["errors"]), 1)
                error = symbol_table["errors"][0]
                self.assertIn(f"got {wrong_type}", error["message"])


if __name__ == "__main__":
    unittest.main()
