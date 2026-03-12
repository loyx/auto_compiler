import unittest
from unittest.mock import patch, call, MagicMock
from typing import Any, Dict

# Type aliases matching the source module
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function"""

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_valid_node(self, mock_traverse):
        """Test handling a valid while node with 2 children"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "children": [
                {"type": "binary_op", "value": ">", "line": 5, "column": 10},
                {"type": "block", "children": [], "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 8
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }
        
        _handle_while(node, symbol_table)
        
        # Verify no errors were recorded
        self.assertEqual(len(symbol_table["errors"]), 0)
        
        # Verify _traverse_node was called twice (once for condition, once for body)
        self.assertEqual(mock_traverse.call_count, 2)
        
        # Verify correct arguments were passed
        expected_calls = [
            call(node["children"][0], symbol_table),
            call(node["children"][1], symbol_table)
        ]
        mock_traverse.assert_has_calls(expected_calls)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_no_children(self, mock_traverse):
        """Test error handling when while node has no children"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "children": [],
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }
        
        _handle_while(node, symbol_table)
        
        # Verify error was recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "While node must have 2 children (condition, body)")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        
        # Verify _traverse_node was NOT called
        mock_traverse.assert_not_called()

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_one_child(self, mock_traverse):
        """Test error handling when while node has only 1 child"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "children": [
                {"type": "binary_op", "value": ">", "line": 15, "column": 10}
            ],
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }
        
        _handle_while(node, symbol_table)
        
        # Verify error was recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "While node must have 2 children (condition, body)")
        
        # Verify _traverse_node was NOT called
        mock_traverse.assert_not_called()

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_missing_children_field(self, mock_traverse):
        """Test error handling when children field is missing"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "line": 20,
            "column": 3
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }
        
        _handle_while(node, symbol_table)
        
        # Verify error was recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "While node must have 2 children (condition, body)")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 3)
        
        # Verify _traverse_node was NOT called
        mock_traverse.assert_not_called()

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_creates_errors_list(self, mock_traverse):
        """Test that errors list is created if not present in symbol_table"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "children": [],
            "line": 25,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1
            # No "errors" key
        }
        
        _handle_while(node, symbol_table)
        
        # Verify errors list was created
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_handle_while_preserves_existing_errors(self):
        """Test that existing errors are preserved when adding new error"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "children": [],
            "line": 30,
            "column": 2
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": [
                {"type": "error", "message": "Previous error", "line": 1, "column": 1}
            ]
        }
        
        _handle_while(node, symbol_table)
        
        # Verify both errors exist
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "Previous error")
        self.assertEqual(symbol_table["errors"][1]["message"], "While node must have 2 children (condition, body)")

    def test_handle_while_no_line_column_info(self):
        """Test error handling when node lacks line/column information"""
        from ._handle_while_src import _handle_while
        
        node = {
            "type": "while",
            "children": []
            # No line or column
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }
        
        _handle_while(node, symbol_table)
        
        # Verify error was recorded with default values
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], -1)
        self.assertEqual(error["column"], -1)


if __name__ == '__main__':
    unittest.main()
