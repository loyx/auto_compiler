import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._handle_function_declaration_src import _handle_function_declaration


class TestHandleFunctionDeclaration(unittest.TestCase):
    """Test cases for _handle_function_declaration function."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_node = {
            "type": "function_declaration",
            "name": "test_func",
            "params": ["param1", "param2"],
            "body": {"type": "block", "statements": []},
            "return_type": "int",
            "line": 10,
            "column": 5
        }
        self.base_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

    def test_happy_path_registers_function_and_traverses_body(self):
        """Test that function is registered and body is traversed when all fields present."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(self.base_node, symbol_table)

        # Verify function was registered
        self.assertIn("test_func", symbol_table["functions"])
        func_info = symbol_table["functions"]["test_func"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], ["param1", "param2"])
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)

        # Verify body was traversed
        mock_traverse.assert_called_once_with(self.base_node["body"], symbol_table)

    def test_no_registration_when_func_name_is_none(self):
        """Test that function is not registered when name is None."""
        node = self.base_node.copy()
        node["name"] = None
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # Verify function was not registered
        self.assertEqual(len(symbol_table["functions"]), 0)

        # But body should still be traversed
        mock_traverse.assert_called_once()

    def test_no_registration_when_functions_key_missing(self):
        """Test that function is not registered when 'functions' key not in symbol_table."""
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(self.base_node, symbol_table)

        # Verify 'functions' key was not added
        self.assertNotIn("functions", symbol_table)

        # But body should still be traversed
        mock_traverse.assert_called_once()

    def test_no_traverse_when_body_is_none(self):
        """Test that _traverse_node is not called when body is None."""
        node = self.base_node.copy()
        node["body"] = None
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # Verify function was registered
        self.assertIn("test_func", symbol_table["functions"])

        # Verify _traverse_node was not called
        mock_traverse.assert_not_called()

    def test_preserves_existing_functions(self):
        """Test that existing functions in symbol_table are preserved."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {
            "existing_func": {
                "return_type": "void",
                "params": [],
                "line": 1,
                "column": 1
            }
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_declaration(self.base_node, symbol_table)

        # Verify both functions exist
        self.assertIn("existing_func", symbol_table["functions"])
        self.assertIn("test_func", symbol_table["functions"])
        self.assertEqual(len(symbol_table["functions"]), 2)

    def test_handles_missing_optional_fields(self):
        """Test that function handles missing optional fields gracefully."""
        node = {
            "type": "function_declaration",
            "name": "minimal_func"
            # Missing: params, body, return_type, line, column
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # Verify function was registered with None values
        self.assertIn("minimal_func", symbol_table["functions"])
        func_info = symbol_table["functions"]["minimal_func"]
        self.assertIsNone(func_info["return_type"])
        self.assertIsNone(func_info["params"])
        self.assertIsNone(func_info["line"])
        self.assertIsNone(func_info["column"])

        # Verify _traverse_node was not called (body is None)
        mock_traverse.assert_not_called()

    def test_empty_params_list(self):
        """Test function with empty params list."""
        node = self.base_node.copy()
        node["params"] = []
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        # Verify function was registered with empty params
        self.assertIn("test_func", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["test_func"]["params"], [])

    def test_complex_body_traversal(self):
        """Test that complex body is passed to _traverse_node."""
        complex_body = {
            "type": "block",
            "statements": [
                {"type": "variable_declaration", "name": "x"},
                {"type": "return_statement", "expression": {"type": "identifier", "name": "x"}}
            ]
        }
        node = self.base_node.copy()
        node["body"] = complex_body
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"] = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # Verify _traverse_node was called with the complex body
        mock_traverse.assert_called_once_with(complex_body, symbol_table)


if __name__ == '__main__':
    unittest.main()
