import unittest
from unittest.mock import patch
import sys

# Register module alias BEFORE importing _traverse_node_src
# This allows child modules that import from .._traverse_node to work correctly
# The alias maps _traverse_node to _traverse_node_src
_package_name = __package__ + "._traverse_node"

# Pre-register the alias as None first, then we'll update it after import
# This prevents the ModuleNotFoundError when _handle_block_src tries to import
sys.modules[_package_name] = None  # Placeholder

# Now import _traverse_node_src - this will trigger imports of child modules
# which will use our placeholder
from ._traverse_node_src import _traverse_node

# Update the placeholder with the actual module
sys.modules[_package_name] = sys.modules[__package__ + "._traverse_node_src"]


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""

    def test_none_node_silent_ignore(self):
        """Test that None node is silently ignored."""
        symbol_table = {"errors": []}
        _traverse_node(None, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_type_field_records_error(self):
        """Test that missing 'type' field records an error."""
        node = {"line": 10, "column": 5}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Node missing 'type' field")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

    def test_missing_type_field_defaults_line_column(self):
        """Test that missing type field uses defaults for line/column."""
        node = {}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], -1)
        self.assertEqual(error["column"], -1)

    @patch('._handle_block_package._handle_block_src._handle_block')
    def test_block_dispatch(self, mock_handler):
        """Test dispatch to _handle_block for block type."""
        node = {"type": "block", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    def test_var_decl_dispatch(self, mock_handler):
        """Test dispatch to _handle_var_decl for var_decl type."""
        node = {"type": "var_decl", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_assignment_package._handle_assignment_src._handle_assignment')
    def test_assignment_dispatch(self, mock_handler):
        """Test dispatch to _handle_assignment for assignment type."""
        node = {"type": "assignment", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_if_package._handle_if_src._handle_if')
    def test_if_dispatch(self, mock_handler):
        """Test dispatch to _handle_if for if type."""
        node = {"type": "if", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_while_package._handle_while_src._handle_while')
    def test_while_dispatch(self, mock_handler):
        """Test dispatch to _handle_while for while type."""
        node = {"type": "while", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_function_call_package._handle_function_call_src._handle_function_call')
    def test_function_call_dispatch(self, mock_handler):
        """Test dispatch to _handle_function_call for function_call type."""
        node = {"type": "function_call", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_function_decl_package._handle_function_decl_src._handle_function_decl')
    def test_function_decl_dispatch(self, mock_handler):
        """Test dispatch to _handle_function_decl for function_decl type."""
        node = {"type": "function_decl", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_return_package._handle_return_src._handle_return')
    def test_return_dispatch(self, mock_handler):
        """Test dispatch to _handle_return for return type."""
        node = {"type": "return", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_literal_package._handle_literal_src._handle_literal')
    def test_literal_dispatch(self, mock_handler):
        """Test dispatch to _handle_literal for literal type."""
        node = {"type": "literal", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_binary_op_package._handle_binary_op_src._handle_binary_op')
    def test_binary_op_dispatch(self, mock_handler):
        """Test dispatch to _handle_binary_op for binary_op type."""
        node = {"type": "binary_op", "line": 5, "column": 10}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        mock_handler.assert_called_once_with(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_unknown_type_records_error(self):
        """Test that unknown node type records an error."""
        node = {"type": "unknown_type", "line": 15, "column": 20}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Unknown node type: unknown_type")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 20)

    def test_unknown_type_error_format(self):
        """Test error format for unknown type has all required fields."""
        node = {"type": "invalid", "line": 1, "column": 1}
        symbol_table = {"errors": []}
        _traverse_node(node, symbol_table)

        error = symbol_table["errors"][0]
        self.assertIn("type", error)
        self.assertIn("message", error)
        self.assertIn("line", error)
        self.assertIn("column", error)
        self.assertEqual(error["type"], "error")

    def test_errors_list_created_if_not_exists(self):
        """Test that errors list is created if not present in symbol_table."""
        node = {"type": "unknown"}
        symbol_table = {}
        _traverse_node(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_handler_called_with_correct_arguments(self):
        """Test that handler receives the exact node and symbol_table references."""
        node = {"type": "block", "line": 5, "column": 10, "extra": "data"}
        symbol_table = {"errors": [], "variables": {}}

        with patch('._handle_block_package._handle_block_src._handle_block') as mock_handler:
            _traverse_node(node, symbol_table)
            mock_handler.assert_called_once_with(node, symbol_table)

    def test_multiple_errors_accumulated(self):
        """Test that multiple unknown types accumulate errors."""
        symbol_table = {"errors": []}

        node1 = {"type": "unknown1", "line": 1, "column": 1}
        node2 = {"type": "unknown2", "line": 2, "column": 2}

        _traverse_node(node1, symbol_table)
        _traverse_node(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "Unknown node type: unknown1")
        self.assertEqual(symbol_table["errors"][1]["message"], "Unknown node type: unknown2")


if __name__ == "__main__":
    unittest.main()
