import unittest
from typing import Any, Dict

# Relative import from the same package
from ._handle_function_decl_src import _handle_function_decl, _extract_params

# Type aliases matching the source module
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionDecl(unittest.TestCase):
    """Test cases for _handle_function_decl function."""

    def test_happy_path_new_function(self):
        """Test adding a new function declaration to symbol table."""
        node: AST = {
            "type": "function_decl",
            "value": "my_function",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        # Verify function was added
        self.assertIn("functions", symbol_table)
        self.assertIn("my_function", symbol_table["functions"])
        func_info = symbol_table["functions"]["my_function"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)
        self.assertEqual(func_info["params"], [])
        # Verify current_function was set
        self.assertEqual(symbol_table["current_function"], "my_function")
        # Verify no errors
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_function_declaration(self):
        """Test detecting duplicate function declaration."""
        # First declaration
        node1: AST = {
            "type": "function_decl",
            "value": "my_function",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {}
        _handle_function_decl(node1, symbol_table)

        # Second declaration (duplicate)
        node2: AST = {
            "type": "function_decl",
            "value": "my_function",
            "data_type": "char",
            "line": 20,
            "column": 8,
            "children": []
        }
        _handle_function_decl(node2, symbol_table)

        # Verify error was recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 8)
        self.assertIn("duplicate function declaration: my_function", error["message"])
        # Verify original function info unchanged
        func_info = symbol_table["functions"]["my_function"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 10)

    def test_function_with_params_param_list_format(self):
        """Test function declaration with parameters in param_list format."""
        node: AST = {
            "type": "function_decl",
            "value": "add",
            "data_type": "int",
            "line": 5,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "a",
                            "data_type": "int"
                        },
                        {
                            "type": "param",
                            "value": "b",
                            "data_type": "int"
                        }
                    ]
                }
            ]
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["add"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "a")
        self.assertEqual(func_info["params"][0]["type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "b")
        self.assertEqual(func_info["params"][1]["type"], "int")

    def test_function_with_direct_param_nodes(self):
        """Test function declaration with direct param nodes (no param_list wrapper)."""
        node: AST = {
            "type": "function_decl",
            "value": "process",
            "data_type": "char",
            "line": 15,
            "column": 3,
            "children": [
                {
                    "type": "param",
                    "value": "input",
                    "data_type": "char"
                },
                {
                    "type": "param",
                    "value": "size",
                    "data_type": "int"
                }
            ]
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["process"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "input")
        self.assertEqual(func_info["params"][0]["type"], "char")
        self.assertEqual(func_info["params"][1]["name"], "size")
        self.assertEqual(func_info["params"][1]["type"], "int")

    def test_default_values_for_missing_fields(self):
        """Test that default values are used when fields are missing."""
        node: AST = {
            "type": "function_decl",
            "value": "minimal_func"
            # Missing: data_type, line, column, children
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["minimal_func"]
        self.assertEqual(func_info["return_type"], "int")  # default
        self.assertEqual(func_info["line"], 0)  # default
        self.assertEqual(func_info["column"], 0)  # default
        self.assertEqual(func_info["params"], [])  # default

    def test_empty_children_list(self):
        """Test function with empty children list."""
        node: AST = {
            "type": "function_decl",
            "value": "no_params",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["no_params"]
        self.assertEqual(func_info["params"], [])

    def test_symbol_table_initialization(self):
        """Test that symbol_table fields are initialized if missing."""
        node: AST = {
            "type": "function_decl",
            "value": "init_test",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {}  # Empty dict

        _handle_function_decl(node, symbol_table)

        # Verify fields were created
        self.assertIn("functions", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["functions"], dict)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_mixed_children_with_non_param_nodes(self):
        """Test that non-param nodes in children are ignored."""
        node: AST = {
            "type": "function_decl",
            "value": "mixed_func",
            "data_type": "int",
            "line": 10,
            "column": 0,
            "children": [
                {
                    "type": "statement",
                    "value": "some_statement"
                },
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "x",
                            "data_type": "int"
                        }
                    ]
                },
                {
                    "type": "block",
                    "children": []
                }
            ]
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["mixed_func"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "x")

    def test_param_without_name_ignored(self):
        """Test that params without names are ignored."""
        node: AST = {
            "type": "function_decl",
            "value": "func_with_bad_param",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [
                {
                    "type": "param",
                    "data_type": "int"
                    # Missing value/name
                },
                {
                    "type": "param",
                    "value": "valid_param",
                    "data_type": "char"
                }
            ]
        }
        symbol_table: SymbolTable = {}

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["func_with_bad_param"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "valid_param")


class TestExtractParams(unittest.TestCase):
    """Test cases for _extract_params helper function."""

    def test_empty_children(self):
        """Test extracting params from empty children list."""
        params = _extract_params([])
        self.assertEqual(params, [])

    def test_param_list_with_multiple_params(self):
        """Test extracting params from param_list node."""
        children = [
            {
                "type": "param_list",
                "children": [
                    {"type": "param", "value": "a", "data_type": "int"},
                    {"type": "param", "value": "b", "data_type": "char"},
                    {"type": "param", "value": "c", "data_type": "int"}
                ]
            }
        ]
        params = _extract_params(children)
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0]["name"], "a")
        self.assertEqual(params[1]["name"], "b")
        self.assertEqual(params[2]["name"], "c")

    def test_direct_param_nodes(self):
        """Test extracting params from direct param nodes."""
        children = [
            {"type": "param", "value": "x", "data_type": "int"},
            {"type": "param", "value": "y", "data_type": "char"}
        ]
        params = _extract_params(children)
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]["name"], "x")
        self.assertEqual(params[1]["name"], "y")

    def test_mixed_param_and_non_param_nodes(self):
        """Test that non-param nodes are ignored."""
        children = [
            {"type": "statement", "value": "stmt"},
            {"type": "param", "value": "p", "data_type": "int"},
            {"type": "block", "children": []}
        ]
        params = _extract_params(children)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["name"], "p")

    def test_param_default_type(self):
        """Test that param defaults to 'int' type when data_type missing."""
        children = [
            {"type": "param", "value": "no_type"}
        ]
        params = _extract_params(children)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["type"], "int")


if __name__ == "__main__":
    unittest.main()
