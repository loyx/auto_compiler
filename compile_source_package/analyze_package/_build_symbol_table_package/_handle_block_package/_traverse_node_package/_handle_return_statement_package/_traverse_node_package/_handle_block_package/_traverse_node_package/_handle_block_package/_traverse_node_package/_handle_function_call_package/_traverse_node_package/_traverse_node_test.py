import unittest
from unittest.mock import patch
from typing import Dict, Any

# Import the function under test using relative import
from ._traverse_node_src import _traverse_node


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    def test_block_node_dispatches_to_handle_block(self):
        """Test that block nodes are dispatched to _handle_block."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block:
            node = {"type": "block", "children": []}
            _traverse_node(node, self.symbol_table)
            mock_handle_block.assert_called_once_with(node, self.symbol_table)
    
    def test_function_decl_node_dispatches_to_handle_function_decl(self):
        """Test that function_decl nodes are dispatched to _handle_function_decl."""
        with patch('._handle_function_decl_package._handle_function_decl_src._handle_function_decl') as mock_handle_function_decl:
            node = {
                "type": "function_decl",
                "name": "test_func",
                "return_type": "int",
                "params": []
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_function_decl.assert_called_once_with(node, self.symbol_table)
    
    def test_var_decl_node_dispatches_to_handle_var_decl(self):
        """Test that var_decl nodes are dispatched to _handle_var_decl."""
        with patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl') as mock_handle_var_decl:
            node = {
                "type": "var_decl",
                "name": "x",
                "data_type": "int"
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_var_decl.assert_called_once_with(node, self.symbol_table)
    
    def test_assignment_node_dispatches_to_handle_assignment(self):
        """Test that assignment nodes are dispatched to _handle_assignment."""
        with patch('._handle_assignment_package._handle_assignment_src._handle_assignment') as mock_handle_assignment:
            node = {
                "type": "assignment",
                "target": {"type": "identifier", "value": "x"},
                "value": {"type": "literal", "value": 5}
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_assignment.assert_called_once_with(node, self.symbol_table)
    
    def test_if_node_dispatches_to_handle_if(self):
        """Test that if nodes are dispatched to _handle_if."""
        with patch('._handle_if_package._handle_if_src._handle_if') as mock_handle_if:
            node = {
                "type": "if",
                "children": [
                    {"type": "binary_op"},  # condition
                    {"type": "block"}       # then branch
                ]
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_if.assert_called_once_with(node, self.symbol_table)
    
    def test_while_node_dispatches_to_handle_while(self):
        """Test that while nodes are dispatched to _handle_while."""
        with patch('._handle_while_package._handle_while_src._handle_while') as mock_handle_while:
            node = {
                "type": "while",
                "children": [
                    {"type": "binary_op"},  # condition
                    {"type": "block"}       # body
                ]
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_while.assert_called_once_with(node, self.symbol_table)
    
    def test_function_call_node_dispatches_to_handle_function_call(self):
        """Test that function_call nodes are dispatched to _handle_function_call."""
        with patch('._handle_function_call_package._handle_function_call_src._handle_function_call') as mock_handle_function_call:
            node = {
                "type": "function_call",
                "name": "print",
                "arguments": []
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_function_call.assert_called_once_with(node, self.symbol_table)
    
    def test_return_node_dispatches_to_handle_return(self):
        """Test that return nodes are dispatched to _handle_return."""
        with patch('._handle_return_package._handle_return_src._handle_return') as mock_handle_return:
            node = {
                "type": "return",
                "value": {"type": "literal", "value": 42}
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_return.assert_called_once_with(node, self.symbol_table)
    
    def test_expression_node_dispatches_to_handle_expression(self):
        """Test that expression nodes are dispatched to _handle_expression."""
        with patch('._handle_expression_package._handle_expression_src._handle_expression') as mock_handle_expression:
            node = {
                "type": "expression",
                "operator": "+",
                "left": {"type": "literal", "value": 1},
                "right": {"type": "literal", "value": 2}
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_expression.assert_called_once_with(node, self.symbol_table)
    
    def test_binary_op_node_dispatches_to_handle_expression(self):
        """Test that binary_op nodes are dispatched to _handle_expression."""
        with patch('._handle_expression_package._handle_expression_src._handle_expression') as mock_handle_expression:
            node = {
                "type": "binary_op",
                "operator": "*",
                "left": {"type": "identifier", "value": "x"},
                "right": {"type": "literal", "value": 10}
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_expression.assert_called_once_with(node, self.symbol_table)
    
    def test_unknown_node_type_no_handler_called(self):
        """Test that unknown node types don't call any handler."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block, \
             patch('._handle_function_decl_package._handle_function_decl_src._handle_function_decl') as mock_handle_function_decl:
            node = {"type": "unknown_type"}
            _traverse_node(node, self.symbol_table)
            mock_handle_block.assert_not_called()
            mock_handle_function_decl.assert_not_called()
    
    def test_missing_type_field_no_exception(self):
        """Test that nodes without type field don't cause exceptions."""
        node = {"children": [], "value": None}
        # Should not raise any exception
        _traverse_node(node, self.symbol_table)
    
    def test_empty_node_no_exception(self):
        """Test that empty node dict doesn't cause exceptions."""
        node = {}
        # Should not raise any exception
        _traverse_node(node, self.symbol_table)
    
    def test_identifier_node_no_handler_called(self):
        """Test that identifier nodes (leaf nodes) don't call any handler."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block:
            node = {"type": "identifier", "value": "x"}
            _traverse_node(node, self.symbol_table)
            mock_handle_block.assert_not_called()
    
    def test_literal_node_no_handler_called(self):
        """Test that literal nodes (leaf nodes) don't call any handler."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block:
            node = {"type": "literal", "value": 42}
            _traverse_node(node, self.symbol_table)
            mock_handle_block.assert_not_called()
    
    def test_node_with_all_fields_block(self):
        """Test block node with all possible AST fields."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block:
            node = {
                "type": "block",
                "children": [],
                "value": None,
                "data_type": "int",
                "line": 10,
                "column": 5
            }
            _traverse_node(node, self.symbol_table)
            mock_handle_block.assert_called_once_with(node, self.symbol_table)
    
    def test_multiple_sequential_calls(self):
        """Test multiple sequential calls with different node types."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block, \
             patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl') as mock_handle_var_decl:
            node1 = {"type": "block"}
            node2 = {"type": "var_decl"}
            
            _traverse_node(node1, self.symbol_table)
            _traverse_node(node2, self.symbol_table)
            
            mock_handle_block.assert_called_once_with(node1, self.symbol_table)
            mock_handle_var_decl.assert_called_once_with(node2, self.symbol_table)
    
    def test_symbol_table_passed_unchanged_reference(self):
        """Test that symbol_table is passed as the same reference to handlers."""
        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handle_block:
            node = {"type": "block"}
            _traverse_node(node, self.symbol_table)
            # Verify the exact same object reference is passed
            args, kwargs = mock_handle_block.call_args
            self.assertIs(args[1], self.symbol_table)
    
    def test_none_node_raises_attribute_error(self):
        """Test that None node raises AttributeError (expected behavior)."""
        with self.assertRaises(AttributeError):
            _traverse_node(None, self.symbol_table)  # type: ignore


if __name__ == "__main__":
    unittest.main()
