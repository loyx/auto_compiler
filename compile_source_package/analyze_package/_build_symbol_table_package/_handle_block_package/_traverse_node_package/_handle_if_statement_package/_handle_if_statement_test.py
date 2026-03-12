import unittest
from unittest.mock import patch, call

# Import the function under test using relative import
from ._handle_if_statement_src import _handle_if_statement

# Full module path for mocking _traverse_node (the actual definition location)
TRAVERSE_NODE_MODULE = 'compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src'


class TestHandleIfStatement(unittest.TestCase):
    """Test cases for _handle_if_statement function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_with_all_branches(self, mock_traverse):
        """Test if statement with condition, then_branch, and else_branch."""
        condition_node = {"type": "expression", "value": "x > 0"}
        then_branch_node = {"type": "block", "statements": []}
        else_branch_node = {"type": "block", "statements": []}
        
        node = {
            "type": "if_statement",
            "condition": condition_node,
            "then_branch": then_branch_node,
            "else_branch": else_branch_node
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called for each branch
        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_has_calls([
            call(condition_node, self.symbol_table),
            call(then_branch_node, self.symbol_table),
            call(else_branch_node, self.symbol_table)
        ])
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_without_else_branch(self, mock_traverse):
        """Test if statement without else_branch (optional branch)."""
        condition_node = {"type": "expression", "value": "x > 0"}
        then_branch_node = {"type": "block", "statements": []}
        
        node = {
            "type": "if_statement",
            "condition": condition_node,
            "then_branch": then_branch_node
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called only for condition and then_branch
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call(condition_node, self.symbol_table),
            call(then_branch_node, self.symbol_table)
        ])
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_with_explicit_none_else(self, mock_traverse):
        """Test if statement with explicit None else_branch."""
        condition_node = {"type": "expression", "value": "x > 0"}
        then_branch_node = {"type": "block", "statements": []}
        
        node = {
            "type": "if_statement",
            "condition": condition_node,
            "then_branch": then_branch_node,
            "else_branch": None
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called only for condition and then_branch
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call(condition_node, self.symbol_table),
            call(then_branch_node, self.symbol_table)
        ])
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_with_none_condition(self, mock_traverse):
        """Test if statement with None condition (edge case)."""
        then_branch_node = {"type": "block", "statements": []}
        
        node = {
            "type": "if_statement",
            "condition": None,
            "then_branch": then_branch_node,
            "else_branch": None
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called only for then_branch
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_once_with(then_branch_node, self.symbol_table)
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_with_all_none_branches(self, mock_traverse):
        """Test if statement with all branches as None."""
        node = {
            "type": "if_statement",
            "condition": None,
            "then_branch": None,
            "else_branch": None
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was not called
        self.assertEqual(mock_traverse.call_count, 0)
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_with_empty_node(self, mock_traverse):
        """Test if statement with empty node (missing all keys)."""
        node = {
            "type": "if_statement"
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was not called
        self.assertEqual(mock_traverse.call_count, 0)
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_with_complex_nested_structure(self, mock_traverse):
        """Test if statement with complex nested AST structure."""
        condition_node = {
            "type": "binary_expression",
            "left": {"type": "identifier", "value": "x"},
            "operator": ">",
            "right": {"type": "literal", "value": 0}
        }
        then_branch_node = {
            "type": "block",
            "statements": [
                {"type": "assignment", "target": "y", "value": {"type": "literal", "value": 1}}
            ]
        }
        else_branch_node = {
            "type": "block",
            "statements": [
                {"type": "assignment", "target": "y", "value": {"type": "literal", "value": 2}}
            ]
        }
        
        node = {
            "type": "if_statement",
            "condition": condition_node,
            "then_branch": then_branch_node,
            "else_branch": else_branch_node,
            "line": 10,
            "column": 5
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called for each branch with correct nodes
        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_has_calls([
            call(condition_node, self.symbol_table),
            call(then_branch_node, self.symbol_table),
            call(else_branch_node, self.symbol_table)
        ])
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_symbol_table_passed_by_reference(self, mock_traverse):
        """Test that symbol_table is passed by reference to _traverse_node."""
        condition_node = {"type": "expression", "value": "x > 0"}
        then_branch_node = {"type": "block", "statements": []}
        
        node = {
            "type": "if_statement",
            "condition": condition_node,
            "then_branch": then_branch_node
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify the same symbol_table object is passed (not a copy)
        calls = mock_traverse.call_args_list
        for call_args in calls:
            self.assertIs(call_args[0][1], self.symbol_table)
    
    @patch(TRAVERSE_NODE_MODULE + '._traverse_node')
    def test_if_statement_traverse_node_side_effects(self, mock_traverse):
        """Test that _traverse_node side effects are propagated."""
        condition_node = {"type": "expression", "value": "x > 0"}
        then_branch_node = {"type": "block", "statements": []}
        else_branch_node = {"type": "block", "statements": []}
        
        node = {
            "type": "if_statement",
            "condition": condition_node,
            "then_branch": then_branch_node,
            "else_branch": else_branch_node
        }
        
        # Simulate _traverse_node modifying the symbol_table
        def side_effect(node_arg, symbol_table_arg):
            symbol_table_arg["variables"]["modified"] = True
        
        mock_traverse.side_effect = side_effect
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify symbol_table was modified by _traverse_node calls
        self.assertEqual(mock_traverse.call_count, 3)
        self.assertIn("modified", self.symbol_table["variables"])
        self.assertTrue(self.symbol_table["variables"]["modified"])


if __name__ == '__main__':
    unittest.main()
