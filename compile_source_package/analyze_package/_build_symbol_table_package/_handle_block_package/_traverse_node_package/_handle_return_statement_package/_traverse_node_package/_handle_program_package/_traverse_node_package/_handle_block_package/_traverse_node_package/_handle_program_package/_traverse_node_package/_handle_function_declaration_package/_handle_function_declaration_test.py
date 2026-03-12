# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_declaration_src import _handle_function_declaration


# === Type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# === Test Cases ===
class TestHandleFunctionDeclaration(unittest.TestCase):
    """Test cases for _handle_function_declaration function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_happy_path_complete_node(self) -> None:
        """Test valid function declaration with all fields present."""
        node: AST = {
            "type": "function_declaration",
            "value": "my_function",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "params": [
                {"name": "x", "data_type": "int"},
                {"name": "y", "data_type": "char"}
            ]
        }

        _handle_function_declaration(node, self.symbol_table)

        # Verify function registered
        self.assertIn("my_function", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["my_function"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)
        self.assertEqual(len(func_info["params"]), 2)

        # Verify current_function set
        self.assertEqual(self.symbol_table["current_function"], "my_function")

        # Verify no errors
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_happy_path_with_name_field(self) -> None:
        """Test function declaration using 'name' field instead of 'value'."""
        node: AST = {
            "type": "function_declaration",
            "name": "another_func",
            "data_type": "char",
            "line": 20,
            "column": 3
        }

        _handle_function_declaration(node, self.symbol_table)

        self.assertIn("another_func", self.symbol_table["functions"])
        self.assertEqual(self.symbol_table["functions"]["another_func"]["return_type"], "char")
        self.assertEqual(self.symbol_table["current_function"], "another_func")

    def test_happy_path_value_takes_precedence_over_name(self) -> None:
        """Test that 'value' field takes precedence over 'name' field."""
        node: AST = {
            "type": "function_declaration",
            "value": "value_name",
            "name": "name_field",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_function_declaration(node, self.symbol_table)

        self.assertIn("value_name", self.symbol_table["functions"])
        self.assertNotIn("name_field", self.symbol_table["functions"])

    def test_happy_path_params_from_children(self) -> None:
        """Test parameters extracted from 'children' field when 'params' absent."""
        node: AST = {
            "type": "function_declaration",
            "value": "func_with_children",
            "data_type": "int",
            "line": 5,
            "column": 2,
            "children": [
                {"name": "param1", "data_type": "int"}
            ]
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["func_with_children"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "param1")

    def test_happy_path_params_takes_precedence_over_children(self) -> None:
        """Test that 'params' field takes precedence over 'children' field."""
        node: AST = {
            "type": "function_declaration",
            "value": "func_priority",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "params": [{"name": "from_params"}],
            "children": [{"name": "from_children"}]
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["func_priority"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "from_params")

    def test_boundary_default_return_type(self) -> None:
        """Test default return type when 'data_type' field is missing."""
        node: AST = {
            "type": "function_declaration",
            "value": "no_data_type",
            "line": 1,
            "column": 1
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_data_type"]
        self.assertEqual(func_info["return_type"], "int")

    def test_boundary_empty_params(self) -> None:
        """Test function with no parameters."""
        node: AST = {
            "type": "function_declaration",
            "value": "no_params",
            "data_type": "char",
            "line": 1,
            "column": 1,
            "params": []
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_params"]
        self.assertEqual(len(func_info["params"]), 0)

    def test_boundary_missing_line_column(self) -> None:
        """Test function with missing line and column fields."""
        node: AST = {
            "type": "function_declaration",
            "value": "no_position",
            "data_type": "int"
        }

        _handle_function_declaration(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_position"]
        self.assertEqual(func_info["line"], 0)
        self.assertEqual(func_info["column"], 0)

    def test_invalid_missing_function_name(self) -> None:
        """Test error when both 'value' and 'name' fields are missing."""
        node: AST = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 15,
            "column": 8
        }

        _handle_function_declaration(node, self.symbol_table)

        # Verify no function registered
        self.assertEqual(len(self.symbol_table["functions"]), 0)

        # Verify error recorded
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "missing_function_name")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)

        # Verify current_function not set
        self.assertNotIn("current_function", self.symbol_table)

    def test_invalid_return_type(self) -> None:
        """Test error when return type is not 'int' or 'char'."""
        node: AST = {
            "type": "function_declaration",
            "value": "bad_type_func",
            "data_type": "float",
            "line": 25,
            "column": 10
        }

        _handle_function_declaration(node, self.symbol_table)

        # Verify function still registered with default type
        self.assertIn("bad_type_func", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["bad_type_func"]
        self.assertEqual(func_info["return_type"], "int")

        # Verify error recorded
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "invalid_return_type")
        self.assertEqual(error["function"], "bad_type_func")
        self.assertEqual(error["return_type"], "float")

        # Verify current_function set
        self.assertEqual(self.symbol_table["current_function"], "bad_type_func")

    def test_invalid_duplicate_function_declaration(self) -> None:
        """Test error when function is declared twice."""
        node1: AST = {
            "type": "function_declaration",
            "value": "duplicate_func",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        node2: AST = {
            "type": "function_declaration",
            "value": "duplicate_func",
            "data_type": "char",
            "line": 5,
            "column": 3
        }

        # First declaration
        _handle_function_declaration(node1, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

        # Second declaration (duplicate)
        _handle_function_declaration(node2, self.symbol_table)

        # Verify error recorded
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_function_declaration")
        self.assertEqual(error["function"], "duplicate_func")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 3)

        # Verify original function info preserved
        func_info = self.symbol_table["functions"]["duplicate_func"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 1)
        self.assertEqual(func_info["column"], 1)

    def test_multiple_functions_in_symbol_table(self) -> None:
        """Test registering multiple different functions."""
        node1: AST = {
            "type": "function_declaration",
            "value": "func1",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        node2: AST = {
            "type": "function_declaration",
            "value": "func2",
            "data_type": "char",
            "line": 10,
            "column": 5
        }

        _handle_function_declaration(node1, self.symbol_table)
        _handle_function_declaration(node2, self.symbol_table)

        self.assertEqual(len(self.symbol_table["functions"]), 2)
        self.assertIn("func1", self.symbol_table["functions"])
        self.assertIn("func2", self.symbol_table["functions"])
        self.assertEqual(self.symbol_table["current_function"], "func2")

    def test_symbol_table_initialized_without_errors_list(self) -> None:
        """Test that errors list is created if not present in symbol_table."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {}
        }

        node: AST = {
            "type": "function_declaration",
            "data_type": "invalid",
            "line": 1,
            "column": 1
        }

        _handle_function_declaration(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_symbol_table_initialized_without_functions_dict(self) -> None:
        """Test that functions dict is created if not present in symbol_table."""
        symbol_table: SymbolTable = {
            "variables": {}
        }

        node: AST = {
            "type": "function_declaration",
            "value": "new_func",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_function_declaration(node, symbol_table)

        self.assertIn("functions", symbol_table)
        self.assertIn("new_func", symbol_table["functions"])


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
