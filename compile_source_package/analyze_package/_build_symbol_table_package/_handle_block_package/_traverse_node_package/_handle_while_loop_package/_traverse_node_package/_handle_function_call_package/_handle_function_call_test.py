# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === relative imports ===
from ._handle_function_call_src import _handle_function_call

# Import the module to patch _traverse_node in the correct location
# Since _handle_function_call uses lazy import, we need to patch the actual module
import main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src as _traverse_node_module

# === type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_handle_function_call_with_empty_arguments(self):
        """Test function_call node with empty arguments list."""
        node: AST = {
            "type": "function_call",
            "name": "my_function",
            "arguments": []
        }

        # Should not raise and should not call _traverse_node
        with patch.object(_traverse_node_module, '_traverse_node') as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            mock_traverse.assert_not_called()

    def test_handle_function_call_with_single_argument(self):
        """Test function_call node with one argument."""
        arg_node: AST = {
            "type": "identifier",
            "name": "x"
        }
        node: AST = {
            "type": "function_call",
            "name": "my_function",
            "arguments": [arg_node]
        }

        with patch.object(_traverse_node_module, '_traverse_node') as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            mock_traverse.assert_called_once_with(arg_node, self.symbol_table)

    def test_handle_function_call_with_multiple_arguments(self):
        """Test function_call node with multiple arguments."""
        arg1: AST = {"type": "literal", "value": 1}
        arg2: AST = {"type": "identifier", "name": "y"}
        arg3: AST = {"type": "binary_op", "op": "+", "left": arg1, "right": arg2}
        node: AST = {
            "type": "function_call",
            "name": "add",
            "arguments": [arg1, arg2, arg3]
        }

        with patch.object(_traverse_node_module, '_traverse_node') as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            self.assertEqual(mock_traverse.call_count, 3)
            mock_traverse.assert_any_call(arg1, self.symbol_table)
            mock_traverse.assert_any_call(arg2, self.symbol_table)
            mock_traverse.assert_any_call(arg3, self.symbol_table)

    def test_handle_function_call_with_none_arguments(self):
        """Test function_call node with None values in arguments list."""
        arg1: AST = {"type": "literal", "value": 42}
        node: AST = {
            "type": "function_call",
            "name": "func",
            "arguments": [None, arg1, None]
        }

        with patch.object(_traverse_node_module, '_traverse_node') as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            # Only non-None arguments should be traversed
            mock_traverse.assert_called_once_with(arg1, self.symbol_table)

    def test_handle_function_call_with_all_none_arguments(self):
        """Test function_call node where all arguments are None."""
        node: AST = {
            "type": "function_call",
            "name": "func",
            "arguments": [None, None, None]
        }

        with patch.object(_traverse_node_module, '_traverse_node') as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            mock_traverse.assert_not_called()

    def test_handle_function_call_without_arguments_field(self):
        """Test function_call node missing 'arguments' field."""
        node: AST = {
            "type": "function_call",
            "name": "func"
            # No "arguments" field
        }

        with patch.object(_traverse_node_module, '_traverse_node') as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            # Should default to empty list, no calls
            mock_traverse.assert_not_called()

    def test_handle_function_call_mixed_none_and_valid_arguments(self):
        """Test function_call with mixed None and valid argument nodes."""
        arg1: AST = {"type": "literal", "value": 1}
        arg2: AST = {"type": "literal", "value": 2}
        arg3: AST = {"type": "literal", "value": 3}
        node: AST = {
            "type": "function_call",
            "name": "func",
            "arguments": [arg1, None, arg2, None, arg3]
        }

        with patch(".._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            self.assertEqual(mock_traverse.call_count, 3)
            # Verify order is preserved for non-None arguments
            calls = mock_traverse.call_args_list
            self.assertEqual(calls[0], ((arg1, self.symbol_table),))
            self.assertEqual(calls[1], ((arg2, self.symbol_table),))
            self.assertEqual(calls[2], ((arg3, self.symbol_table),))

    def test_handle_function_call_symbol_table_passed_through(self):
        """Test that symbol_table is correctly passed to _traverse_node."""
        arg_node: AST = {"type": "identifier", "name": "x"}
        node: AST = {
            "type": "function_call",
            "name": "func",
            "arguments": [arg_node]
        }

        # Create a modified symbol table to verify it's passed as-is
        custom_symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int"}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }

        with patch(".._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, custom_symbol_table)
            mock_traverse.assert_called_once_with(arg_node, custom_symbol_table)

    def test_handle_function_call_nested_argument_nodes(self):
        """Test function_call with deeply nested argument nodes."""
        inner_node: AST = {"type": "identifier", "name": "z"}
        middle_node: AST = {
            "type": "unary_op",
            "op": "-",
            "operand": inner_node
        }
        outer_node: AST = {
            "type": "binary_op",
            "op": "*",
            "left": middle_node,
            "right": {"type": "literal", "value": 2}
        }
        node: AST = {
            "type": "function_call",
            "name": "compute",
            "arguments": [outer_node]
        }

        with patch(".._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, self.symbol_table)
            # _handle_function_call only calls _traverse_node once for the outer node
            # Nested traversal is _traverse_node's responsibility
            mock_traverse.assert_called_once_with(outer_node, self.symbol_table)


if __name__ == "__main__":
    unittest.main()
