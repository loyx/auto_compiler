# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# === sub function imports ===
from ._handle_program_src import _handle_program

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleProgram(unittest.TestCase):
    """Test cases for _handle_program function."""

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_children(self, mock_traverse_node: MagicMock) -> None:
        """Test _handle_program with a node containing multiple children."""
        # Arrange
        node: AST = {
            "type": "program",
            "children": [
                {"type": "function_declaration", "value": "func1"},
                {"type": "function_declaration", "value": "func2"},
                {"type": "variable_declaration", "value": "var1"},
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

        # Act
        _handle_program(node, symbol_table)

        # Assert
        self.assertEqual(mock_traverse_node.call_count, 3)
        mock_traverse_node.assert_any_call(node["children"][0], symbol_table)
        mock_traverse_node.assert_any_call(node["children"][1], symbol_table)
        mock_traverse_node.assert_any_call(node["children"][2], symbol_table)

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_empty_children(self, mock_traverse_node: MagicMock) -> None:
        """Test _handle_program with a node containing empty children list."""
        # Arrange
        node: AST = {
            "type": "program",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

        # Act
        _handle_program(node, symbol_table)

        # Assert
        mock_traverse_node.assert_not_called()

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_without_children_key(self, mock_traverse_node: MagicMock) -> None:
        """Test _handle_program with a node missing the 'children' key."""
        # Arrange
        node: AST = {
            "type": "program"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

        # Act
        _handle_program(node, symbol_table)

        # Assert
        mock_traverse_node.assert_not_called()

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_preserves_symbol_table_reference(self, mock_traverse_node: MagicMock) -> None:
        """Test that the same symbol_table reference is passed to _traverse_node."""
        # Arrange
        node: AST = {
            "type": "program",
            "children": [{"type": "function_declaration", "value": "func1"}]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

        # Act
        _handle_program(node, symbol_table)

        # Assert
        mock_traverse_node.assert_called_once()
        # Verify the exact same object reference is passed
        called_args = mock_traverse_node.call_args
        self.assertIs(called_args[0][1], symbol_table)

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_single_child(self, mock_traverse_node: MagicMock) -> None:
        """Test _handle_program with a node containing a single child."""
        # Arrange
        node: AST = {
            "type": "program",
            "children": [{"type": "block", "value": "main_block"}]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

        # Act
        _handle_program(node, symbol_table)

        # Assert
        mock_traverse_node.assert_called_once_with(node["children"][0], symbol_table)

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_complex_children(self, mock_traverse_node: MagicMock) -> None:
        """Test _handle_program with children containing nested structures."""
        # Arrange
        node: AST = {
            "type": "program",
            "children": [
                {
                    "type": "function_declaration",
                    "value": "main",
                    "children": [
                        {"type": "block", "value": "body"}
                    ]
                },
                {
                    "type": "variable_declaration",
                    "data_type": "int",
                    "value": "x"
                }
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        # Act
        _handle_program(node, symbol_table)

        # Assert
        self.assertEqual(mock_traverse_node.call_count, 2)
        # Verify children are passed in order
        calls = mock_traverse_node.call_args_list
        self.assertEqual(calls[0][0][0], node["children"][0])
        self.assertEqual(calls[1][0][0], node["children"][1])


if __name__ == "__main__":
    unittest.main()
