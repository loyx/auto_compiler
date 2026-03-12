# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
# Import the function under test using relative import
from ._handle_if_statement_src import _handle_if_statement


class TestHandleIfStatement(unittest.TestCase):
    """Test cases for _handle_if_statement function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_if_statement_with_all_fields(self, mock_traverse_node):
        """Test if_statement with condition, then_body, and else_body all present."""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_body": {"type": "block", "statements": [{"type": "assignment", "var": "y", "value": "1"}]},
            "else_body": {"type": "block", "statements": [{"type": "assignment", "var": "y", "value": "0"}]}
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should call _traverse_node three times: condition, then_body, else_body
        self.assertEqual(mock_traverse_node.call_count, 3)
        mock_traverse_node.assert_any_call(node["condition"], self.mock_symbol_table)
        mock_traverse_node.assert_any_call(node["then_body"], self.mock_symbol_table)
        mock_traverse_node.assert_any_call(node["else_body"], self.mock_symbol_table)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_without_else_body(self, mock_traverse_node):
        """Test if_statement with condition and then_body but no else_body."""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_body": {"type": "block", "statements": [{"type": "assignment", "var": "y", "value": "1"}]},
            "else_body": None
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should call _traverse_node twice: condition and then_body only
        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_any_call(node["condition"], self.mock_symbol_table)
        mock_traverse_node.assert_any_call(node["then_body"], self.mock_symbol_table)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_without_then_body(self, mock_traverse_node):
        """Test if_statement with condition but no then_body."""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_body": None,
            "else_body": {"type": "block", "statements": [{"type": "assignment", "var": "y", "value": "0"}]}
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should call _traverse_node twice: condition and else_body only
        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_any_call(node["condition"], self.mock_symbol_table)
        mock_traverse_node.assert_any_call(node["else_body"], self.mock_symbol_table)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_condition_only(self, mock_traverse_node):
        """Test if_statement with only condition present."""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_body": None,
            "else_body": None
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should call _traverse_node once: condition only
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["condition"], self.mock_symbol_table)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_empty_node(self, mock_traverse_node):
        """Test if_statement with all fields None or missing."""
        node = {
            "type": "if_statement",
            "condition": None,
            "then_body": None,
            "else_body": None
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should not call _traverse_node at all
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_missing_fields(self, mock_traverse_node):
        """Test if_statement with missing fields (not explicitly None)."""
        node = {
            "type": "if_statement"
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should not call _traverse_node at all
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_preserves_symbol_table(self, mock_traverse_node):
        """Test that symbol_table is passed correctly to _traverse_node."""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_body": {"type": "block"},
            "else_body": {"type": "block"}
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Verify symbol_table is passed as second argument to all calls
        for call in mock_traverse_node.call_args_list:
            self.assertEqual(call[0][1], self.mock_symbol_table)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_call_order(self, mock_traverse_node):
        """Test that _traverse_node is called in correct order: condition, then_body, else_body."""
        node = {
            "type": "if_statement",
            "condition": {"type": "condition_node"},
            "then_body": {"type": "then_node"},
            "else_body": {"type": "else_node"}
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Verify call order
        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][0][0], node["condition"])
        self.assertEqual(calls[1][0][0], node["then_body"])
        self.assertEqual(calls[2][0][0], node["else_body"])

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_returns_none(self, mock_traverse_node):
        """Test that function returns None."""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_body": {"type": "block"},
            "else_body": {"type": "block"}
        }
        
        result = _handle_if_statement(node, self.mock_symbol_table)
        
        self.assertIsNone(result)

    @patch("._handle_if_statement_src._traverse_node")
    def test_handle_if_statement_nested_if(self, mock_traverse_node):
        """Test if_statement with nested if_statement in then_body."""
        nested_if = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_body": {"type": "block"},
            "else_body": None
        }
        
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_body": nested_if,
            "else_body": None
        }
        
        _handle_if_statement(node, self.mock_symbol_table)
        
        # Should call _traverse_node twice: condition and then_body (nested if)
        self.assertEqual(mock_traverse_node.call_count, 2)


if __name__ == "__main__":
    unittest.main()
