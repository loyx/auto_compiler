# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# === relative imports ===
from ._handle_if_statement_src import _handle_if_statement

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIfStatement(unittest.TestCase):
    """Test cases for _handle_if_statement function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_traverse_node = MagicMock()

    def _create_mock_symbol_table(self) -> SymbolTable:
        """Create a mock symbol table with all required fields."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def _create_if_node(
        self,
        line: int = 1,
        column: int = 1,
        has_else: bool = False,
        then_children: list = None,
        else_children: list = None,
        condition_children: list = None
    ) -> AST:
        """Helper to create an if_statement AST node."""
        condition_node = {
            "type": "expression",
            "children": condition_children or [],
            "line": line,
            "column": column
        }
        then_block_node = {
            "type": "block",
            "children": then_children or [],
            "line": line,
            "column": column
        }
        children = [condition_node, then_block_node]
        
        if has_else:
            else_block_node = {
                "type": "block",
                "children": else_children or [],
                "line": line,
                "column": column
            }
            children.append(else_block_node)
        
        return {
            "type": "if_statement",
            "children": children,
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node')
    def test_happy_path_with_then_block_only(self, mock_traverse):
        """Test valid if_statement with only then-block (no else)."""
        node = self._create_if_node(
            line=5,
            column=10,
            has_else=False,
            then_children=[
                {"type": "statement", "line": 6, "column": 4},
                {"type": "statement", "line": 7, "column": 4}
            ],
            condition_children=[{"type": "binary_op", "line": 5, "column": 13}]
        )
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Verify condition was traversed (first call)
        self.assertEqual(mock_traverse.call_count, 3)  # condition + 2 then statements
        
        # Verify scope management
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(len(symbol_table["scope_stack"]), 0)
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node')
    def test_happy_path_with_else_block(self, mock_traverse):
        """Test valid if_statement with both then and else blocks."""
        node = self._create_if_node(
            line=10,
            column=1,
            has_else=True,
            then_children=[{"type": "statement", "line": 11, "column": 4}],
            else_children=[{"type": "statement", "line": 13, "column": 4}],
            condition_children=[{"type": "binary_op", "line": 10, "column": 3}]
        )
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Verify all nodes were traversed: condition + 1 then + 1 else
        self.assertEqual(mock_traverse.call_count, 3)
        
        # Verify scope management (should return to original)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(len(symbol_table["scope_stack"]), 0)
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node')
    def test_error_less_than_two_children(self, mock_traverse):
        """Test if_statement with less than 2 children should append error."""
        node = {
            "type": "if_statement",
            "children": [{"type": "expression", "line": 1, "column": 1}],  # Only condition
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Verify error was appended
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("requires at least condition and then-block", symbol_table["errors"][0])
        self.assertIn("line 1", symbol_table["errors"][0])
        self.assertIn("column 1", symbol_table["errors"][0])
        
        # Verify traverse_node was NOT called
        mock_traverse.assert_not_called()

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node')
    def test_error_empty_children(self, mock_traverse):
        """Test if_statement with empty children list should append error."""
        node = {
            "type": "if_statement",
            "children": [],
            "line": 5,
            "column": 10
        }
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Verify error was appended
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("requires at least condition and then-block", symbol_table["errors"][0])
        
        # Verify traverse_node was NOT called
        mock_traverse.assert_not_called()

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_initializes_missing_symbol_table_fields(self, mock_traverse):
        """Test that function initializes missing symbol_table fields."""
        node = self._create_if_node(
            line=1,
            column=1,
            then_children=[{"type": "statement", "line": 2, "column": 4}]
        )
        # Create symbol_table with missing fields
        symbol_table: SymbolTable = {}
        
        _handle_if_statement(node, symbol_table)
        
        # Verify fields were initialized
        self.assertIn("errors", symbol_table)
        self.assertIn("scope_stack", symbol_table)
        self.assertIn("current_scope", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertIsInstance(symbol_table["scope_stack"], list)
        self.assertEqual(symbol_table["current_scope"], 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_scope_management_then_block(self, mock_traverse):
        """Test scope stack management for then-block."""
        node = self._create_if_node(
            line=1,
            column=1,
            then_children=[{"type": "statement", "line": 2, "column": 4}]
        )
        symbol_table = self._create_mock_symbol_table()
        symbol_table["current_scope"] = 5  # Start at scope 5
        
        _handle_if_statement(node, symbol_table)
        
        # Verify scope returned to original value
        self.assertEqual(symbol_table["current_scope"], 5)
        self.assertEqual(len(symbol_table["scope_stack"]), 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_scope_management_with_else_block(self, mock_traverse):
        """Test scope stack management for both then and else blocks."""
        node = self._create_if_node(
            line=1,
            column=1,
            has_else=True,
            then_children=[{"type": "statement", "line": 2, "column": 4}],
            else_children=[{"type": "statement", "line": 4, "column": 4}]
        )
        symbol_table = self._create_mock_symbol_table()
        symbol_table["current_scope"] = 10  # Start at scope 10
        
        _handle_if_statement(node, symbol_table)
        
        # Verify scope returned to original value after both blocks
        self.assertEqual(symbol_table["current_scope"], 10)
        self.assertEqual(len(symbol_table["scope_stack"]), 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_traverse_node_called_with_correct_arguments(self, mock_traverse):
        """Test that _traverse_node is called with correct node and symbol_table."""
        condition_node = {"type": "binary_op", "line": 1, "column": 5}
        then_statement = {"type": "assignment", "line": 2, "column": 4}
        node = self._create_if_node(
            line=1,
            column=1,
            then_children=[then_statement],
            condition_children=[condition_node]
        )
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Verify traverse_node was called with condition node first
        calls = mock_traverse.call_args_list
        self.assertEqual(len(calls), 2)  # condition + 1 then statement
        
        # First call should be condition node
        self.assertEqual(calls[0][0][0], condition_node)
        self.assertEqual(calls[0][0][1], symbol_table)
        
        # Second call should be then statement
        self.assertEqual(calls[1][0][0], then_statement)
        self.assertEqual(calls[1][0][1], symbol_table)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_empty_then_block(self, mock_traverse):
        """Test if_statement with empty then-block."""
        node = self._create_if_node(
            line=1,
            column=1,
            then_children=[]  # Empty then block
        )
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Only condition should be traversed
        self.assertEqual(mock_traverse.call_count, 1)
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_empty_else_block(self, mock_traverse):
        """Test if_statement with empty else-block."""
        node = self._create_if_node(
            line=1,
            column=1,
            has_else=True,
            then_children=[{"type": "statement", "line": 2, "column": 4}],
            else_children=[]  # Empty else block
        )
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Condition + 1 then statement should be traversed (else is empty)
        self.assertEqual(mock_traverse.call_count, 2)
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._traverse_node')
    def test_multiple_else_statements(self, mock_traverse):
        """Test if_statement with multiple statements in else-block."""
        node = self._create_if_node(
            line=1,
            column=1,
            has_else=True,
            then_children=[{"type": "statement", "line": 2, "column": 4}],
            else_children=[
                {"type": "statement", "line": 4, "column": 4},
                {"type": "statement", "line": 5, "column": 4},
                {"type": "statement", "line": 6, "column": 4}
            ]
        )
        symbol_table = self._create_mock_symbol_table()
        
        _handle_if_statement(node, symbol_table)
        
        # Condition + 1 then + 3 else statements
        self.assertEqual(mock_traverse.call_count, 5)
        
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
