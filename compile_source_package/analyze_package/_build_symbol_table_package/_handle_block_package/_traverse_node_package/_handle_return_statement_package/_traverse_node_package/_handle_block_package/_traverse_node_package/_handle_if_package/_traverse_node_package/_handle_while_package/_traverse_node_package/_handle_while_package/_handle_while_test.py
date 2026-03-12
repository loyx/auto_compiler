# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._handle_while_src import _handle_while


# === Test Cases ===
class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function."""

    def test_happy_path_valid_while_node(self) -> None:
        """Test handling a valid while node with condition and body."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 5, "column": 10},
                {"type": "block", "children": [], "line": 6, "column": 12},
            ],
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call(node["children"][0], symbol_table)
        mock_traverse.assert_any_call(node["children"][1], symbol_table)

    def test_error_missing_children(self) -> None:
        """Test error recording when while node has no children."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "children": [],
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 5)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "while statement requires condition and body",
        )
        mock_traverse.assert_not_called()

    def test_error_only_one_child(self) -> None:
        """Test error recording when while node has only one child."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 5, "column": 10},
            ],
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 5)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        mock_traverse.assert_not_called()

    def test_error_missing_children_key(self) -> None:
        """Test error recording when while node has no 'children' key."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 5)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        mock_traverse.assert_not_called()

    def test_initializes_errors_if_missing(self) -> None:
        """Test that errors list is initialized if not present in symbol_table."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "children": [],
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
        }

        # Act
        with patch("._handle_while_src._traverse_node"):
            _handle_while(node, symbol_table)

        # Assert
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_default_line_column_zero(self) -> None:
        """Test that default line/column values are 0 when not provided."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "children": [],
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node"):
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_traverse_node_called_with_correct_children(self) -> None:
        """Test that _traverse_node is called with correct child nodes."""
        # Arrange
        condition_node: Dict[str, Any] = {
            "type": "binary_op",
            "value": ">",
            "line": 5,
            "column": 15,
        }
        body_node: Dict[str, Any] = {
            "type": "block",
            "children": [],
            "line": 6,
            "column": 12,
        }
        node: Dict[str, Any] = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(mock_traverse.call_count, 2)
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0], condition_node)
        self.assertEqual(calls[0][0][1], symbol_table)
        self.assertEqual(calls[1][0][0], body_node)
        self.assertEqual(calls[1][0][1], symbol_table)

    def test_no_error_on_valid_node_with_extra_children(self) -> None:
        """Test that valid node with more than 2 children is accepted."""
        # Arrange
        node: Dict[str, Any] = {
            "type": "while",
            "children": [
                {"type": "condition", "value": "x > 0"},
                {"type": "block", "children": []},
                {"type": "extra", "value": "ignored"},
            ],
            "line": 5,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        # Act
        with patch("._handle_while_src._traverse_node") as mock_traverse:
            _handle_while(node, symbol_table)

        # Assert
        self.assertEqual(len(symbol_table["errors"]), 0)
        # Only first 2 children should be traversed
        self.assertEqual(mock_traverse.call_count, 2)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
