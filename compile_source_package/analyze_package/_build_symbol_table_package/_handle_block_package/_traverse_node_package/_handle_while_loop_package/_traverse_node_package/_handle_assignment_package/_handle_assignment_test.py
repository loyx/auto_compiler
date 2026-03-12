import unittest
from unittest.mock import patch, call

from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_both_target_and_value_present(self, mock_traverse):
        """Test assignment with both target and value present."""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "value": 5}
        }

        _handle_assignment(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call({"type": "identifier", "name": "x"}, self.symbol_table),
            call({"type": "literal", "value": 5}, self.symbol_table)
        ])

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_target_is_none(self, mock_traverse):
        """Test assignment with target being None."""
        node = {
            "type": "assignment",
            "target": None,
            "value": {"type": "literal", "value": 10}
        }

        _handle_assignment(node, self.symbol_table)

        mock_traverse.assert_called_once_with(
            {"type": "literal", "value": 10},
            self.symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_value_is_none(self, mock_traverse):
        """Test assignment with value being None."""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "y"},
            "value": None
        }

        _handle_assignment(node, self.symbol_table)

        mock_traverse.assert_called_once_with(
            {"type": "identifier", "name": "y"},
            self.symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_both_target_and_value_none(self, mock_traverse):
        """Test assignment with both target and value being None."""
        node = {
            "type": "assignment",
            "target": None,
            "value": None
        }

        _handle_assignment(node, self.symbol_table)

        mock_traverse.assert_not_called()

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_target_missing_from_node(self, mock_traverse):
        """Test assignment node without target key."""
        node = {
            "type": "assignment",
            "value": {"type": "literal", "value": 42}
        }

        _handle_assignment(node, self.symbol_table)

        mock_traverse.assert_called_once_with(
            {"type": "literal", "value": 42},
            self.symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_value_missing_from_node(self, mock_traverse):
        """Test assignment node without value key."""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "z"}
        }

        _handle_assignment(node, self.symbol_table)

        mock_traverse.assert_called_once_with(
            {"type": "identifier", "name": "z"},
            self.symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_complex_nested_expression(self, mock_traverse):
        """Test assignment with complex nested expressions."""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "result"},
            "value": {
                "type": "binary_op",
                "left": {"type": "identifier", "name": "a"},
                "right": {"type": "literal", "value": 1}
            }
        }

        _handle_assignment(node, self.symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_traverse_propagates_exceptions(self, mock_traverse):
        """Test that exceptions from _traverse_node are propagated."""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "value": 5}
        }
        mock_traverse.side_effect = ValueError("Traversal error")

        with self.assertRaises(ValueError) as context:
            _handle_assignment(node, self.symbol_table)

        self.assertEqual(str(context.exception), "Traversal error")
        mock_traverse.assert_called_once_with(
            {"type": "identifier", "name": "x"},
            self.symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_symbol_table_not_modified_directly(self, mock_traverse):
        """Test that symbol_table is passed but not directly modified by _handle_assignment."""
        original_symbol_table = self.symbol_table.copy()
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "name": "x"},
            "value": {"type": "literal", "value": 5}
        }

        _handle_assignment(node, self.symbol_table)

        # _handle_assignment itself doesn't modify symbol_table directly
        # (modifications happen via _traverse_node)
        self.assertEqual(self.symbol_table, original_symbol_table)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_empty_node_dict(self, mock_traverse):
        """Test with empty node dictionary."""
        node = {}

        _handle_assignment(node, self.symbol_table)

        mock_traverse.assert_not_called()


if __name__ == '__main__':
    unittest.main()
