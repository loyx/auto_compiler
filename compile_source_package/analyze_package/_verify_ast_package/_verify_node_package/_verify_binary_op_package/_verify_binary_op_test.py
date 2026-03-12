import unittest
from unittest.mock import patch

from ._verify_binary_op_src import _verify_binary_op


class TestVerifyBinaryOp(unittest.TestCase):
    """Test cases for _verify_binary_op function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        self.context_stack = []
        self.filename = "test.c"

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_matching_int_types(self, mock_verify_node):
        """Test binary operation with matching int types."""
        node = {
            "type": "binary_op",
            "operator": "+",
            "line": 1,
            "column": 5,
            "left": {"data_type": "int"},
            "right": {"data_type": "int"}
        }

        _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

        self.assertEqual(node['data_type'], 'int')
        self.assertEqual(mock_verify_node.call_count, 2)

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_matching_char_types(self, mock_verify_node):
        """Test binary operation with matching char types."""
        node = {
            "type": "binary_op",
            "operator": "==",
            "line": 3,
            "column": 10,
            "left": {"data_type": "char"},
            "right": {"data_type": "char"}
        }

        _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

        self.assertEqual(node['data_type'], 'char')

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_type_mismatch_int_vs_char(self, mock_verify_node):
        """Test binary operation raises error on mismatched types (int vs char)."""
        node = {
            "type": "binary_op",
            "operator": "+",
            "line": 5,
            "column": 8,
            "left": {"data_type": "int"},
            "right": {"data_type": "char"}
        }

        with self.assertRaises(ValueError) as context:
            _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

        self.assertIn("test.c:5:8: error: type mismatch: expected 'int' but got 'char'", str(context.exception))

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_type_mismatch_char_vs_int(self, mock_verify_node):
        """Test binary operation raises error on mismatched types (char vs int)."""
        node = {
            "type": "binary_op",
            "operator": "==",
            "line": 10,
            "column": 15,
            "left": {"data_type": "char"},
            "right": {"data_type": "int"}
        }

        with self.assertRaises(ValueError) as context:
            _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

        self.assertIn("test.c:10:15: error: type mismatch: expected 'char' but got 'int'", str(context.exception))

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_calls_verify_node_on_both_operands(self, mock_verify_node):
        """Test that _verify_node is called on both left and right operands."""
        left_node = {"data_type": "int"}
        right_node = {"data_type": "int"}
        node = {
            "type": "binary_op",
            "operator": "*",
            "line": 1,
            "column": 1,
            "left": left_node,
            "right": right_node
        }

        _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

        self.assertEqual(mock_verify_node.call_count, 2)
        mock_verify_node.assert_any_call(left_node, self.symbol_table, self.context_stack, self.filename)
        mock_verify_node.assert_any_call(right_node, self.symbol_table, self.context_stack, self.filename)

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_various_operators(self, mock_verify_node):
        """Test binary operation with various operators."""
        operators = ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||']

        for op in operators:
            node = {
                "type": "binary_op",
                "operator": op,
                "line": 1,
                "column": 1,
                "left": {"data_type": "int"},
                "right": {"data_type": "int"}
            }

            _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

            self.assertEqual(node['data_type'], 'int', f"Failed for operator: {op}")

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_binary_op_package._verify_binary_op_src._verify_node')
    def test_binary_op_preserves_error_location(self, mock_verify_node):
        """Test that error message preserves correct line and column information."""
        node = {
            "type": "binary_op",
            "operator": "+",
            "line": 42,
            "column": 100,
            "left": {"data_type": "int"},
            "right": {"data_type": "char"}
        }

        with self.assertRaises(ValueError) as context:
            _verify_binary_op(node, self.symbol_table, self.context_stack, self.filename)

        self.assertIn("test.c:42:100:", str(context.exception))


if __name__ == '__main__':
    unittest.main()
