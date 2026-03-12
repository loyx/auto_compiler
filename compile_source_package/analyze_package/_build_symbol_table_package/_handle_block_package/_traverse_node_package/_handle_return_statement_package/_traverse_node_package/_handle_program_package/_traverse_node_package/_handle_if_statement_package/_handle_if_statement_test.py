import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._handle_if_statement_src import _handle_if_statement


class TestHandleIfStatement(unittest.TestCase):
    """Test cases for _handle_if_statement function"""
    
    def _create_valid_if_statement(self, has_else: bool = True) -> Dict[str, Any]:
        """Helper to create a valid if_statement node"""
        node = {
            "type": "if_statement",
            "condition": {"type": "expression", "value": "x > 0"},
            "then_branch": {"type": "block", "children": []},
            "line": 10,
            "column": 5
        }
        if has_else:
            node["else_branch"] = {"type": "block", "children": []}
        return node
    
    def _create_symbol_table(self) -> Dict[str, Any]:
        """Helper to create a symbol table with errors list"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    def test_handle_if_statement_with_all_branches(self):
        """Test if_statement with condition, then_branch, and else_branch"""
        node = self._create_valid_if_statement(has_else=True)
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify _traverse_node was called 3 times (condition, then_branch, else_branch)
            self.assertEqual(mock_traverse.call_count, 3)
            
            # Verify calls were made with correct arguments
            calls = mock_traverse.call_args_list
            self.assertEqual(calls[0][0][0], node["condition"])  # condition
            self.assertEqual(calls[1][0][0], node["then_branch"])  # then_branch
            self.assertEqual(calls[2][0][0], node["else_branch"])  # else_branch
            
            # Verify symbol_table was passed to all calls
            for call in calls:
                self.assertEqual(call[0][1], symbol_table)
            
            # Verify no errors were added
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_handle_if_statement_without_else_branch(self):
        """Test if_statement without else_branch"""
        node = self._create_valid_if_statement(has_else=False)
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify _traverse_node was called 2 times (condition, then_branch only)
            self.assertEqual(mock_traverse.call_count, 2)
            
            # Verify no errors were added
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_handle_if_statement_else_branch_none(self):
        """Test if_statement with else_branch explicitly set to None"""
        node = {
            "type": "if_statement",
            "condition": {"type": "expression", "value": "x > 0"},
            "then_branch": {"type": "block", "children": []},
            "else_branch": None,
            "line": 20,
            "column": 10
        }
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify _traverse_node was called 2 times (condition, then_branch only, not else_branch)
            self.assertEqual(mock_traverse.call_count, 2)
            
            # Verify no errors were added
            self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_handle_if_statement_missing_condition(self):
        """Test if_statement missing 'condition' field"""
        node = {
            "type": "if_statement",
            "then_branch": {"type": "block", "children": []},
            "line": 10,
            "column": 5
        }
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify _traverse_node was NOT called
            mock_traverse.assert_not_called()
            
            # Verify error was added
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["message"], "if_statement missing 'condition' field")
            self.assertEqual(error["line"], 10)
            self.assertEqual(error["column"], 5)
            self.assertEqual(error["type"], "missing_field")
    
    def test_handle_if_statement_missing_then_branch(self):
        """Test if_statement missing 'then_branch' field"""
        node = {
            "type": "if_statement",
            "condition": {"type": "expression", "value": "x > 0"},
            "line": 15,
            "column": 8
        }
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify _traverse_node was NOT called
            mock_traverse.assert_not_called()
            
            # Verify error was added
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["message"], "if_statement missing 'then_branch' field")
            self.assertEqual(error["line"], 15)
            self.assertEqual(error["column"], 8)
            self.assertEqual(error["type"], "missing_field")
    
    def test_handle_if_statement_missing_line_column(self):
        """Test if_statement with missing line and column information"""
        node = {
            "type": "if_statement",
            # Missing condition
            "then_branch": {"type": "block", "children": []}
        }
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify error was added with "unknown" for line/column
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["message"], "if_statement missing 'condition' field")
            self.assertEqual(error["line"], "unknown")
            self.assertEqual(error["column"], "unknown")
            self.assertEqual(error["type"], "missing_field")
            
            # Verify _traverse_node was NOT called
            mock_traverse.assert_not_called()
    
    def test_handle_if_statement_with_complex_branches(self):
        """Test if_statement with complex nested branches"""
        node = {
            "type": "if_statement",
            "condition": {
                "type": "binary_operation",
                "left": {"type": "variable", "name": "x"},
                "right": {"type": "literal", "value": 0},
                "operator": ">"
            },
            "then_branch": {
                "type": "block",
                "children": [
                    {"type": "assignment", "variable": "y", "value": {"type": "literal", "value": 1}}
                ]
            },
            "else_branch": {
                "type": "block",
                "children": [
                    {"type": "assignment", "variable": "y", "value": {"type": "literal", "value": 0}}
                ]
            },
            "line": 25,
            "column": 12
        }
        symbol_table = self._create_symbol_table()
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_if_statement(node, symbol_table)
            
            # Verify _traverse_node was called 3 times
            self.assertEqual(mock_traverse.call_count, 3)
            
            # Verify correct nodes were passed
            calls = mock_traverse.call_args_list
            self.assertEqual(calls[0][0][0], node["condition"])
            self.assertEqual(calls[1][0][0], node["then_branch"])
            self.assertEqual(calls[2][0][0], node["else_branch"])
            
            # Verify no errors were added
            self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == '__main__':
    unittest.main()
