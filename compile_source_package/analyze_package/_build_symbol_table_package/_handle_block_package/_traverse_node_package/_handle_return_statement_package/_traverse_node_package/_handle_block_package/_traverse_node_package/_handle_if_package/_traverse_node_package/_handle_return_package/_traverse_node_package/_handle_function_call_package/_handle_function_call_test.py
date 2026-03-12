# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of target function ===
from ._handle_function_call_src import _handle_function_call, _add_undefined_function_error


# === Type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def test_function_exists_returns_return_type(self):
        """Happy path: function exists in symbol table, returns its return_type."""
        node: AST = {
            "type": "function_call",
            "function_name": "my_function",
            "arguments": [],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "my_function": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "current_scope": 0,
            "scope_stack": [0],
            "current_function": "main",
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "int")
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_exists_returns_void_type(self):
        """Function exists with void return_type."""
        node: AST = {
            "type": "function_call",
            "function_name": "print_msg",
            "line": 15
        }
        symbol_table: SymbolTable = {
            "functions": {
                "print_msg": {
                    "return_type": "void",
                    "params": [{"name": "msg", "type": "string"}],
                    "line": 5,
                    "column": 0
                }
            },
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_not_found_returns_void_and_adds_error(self):
        """Function not in symbol table: returns 'void' and adds error."""
        node: AST = {
            "type": "function_call",
            "function_name": "undefined_func",
            "line": 20,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "functions": {
                "other_function": {
                    "return_type": "string",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("undefined function 'undefined_func' at line 20", symbol_table["errors"])

    def test_function_not_found_creates_errors_list(self):
        """When errors list doesn't exist, it should be created."""
        node: AST = {
            "type": "function_call",
            "function_name": "missing_func",
            "line": 5
        }
        symbol_table: SymbolTable = {
            "functions": {}
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_function_name(self):
        """Edge case: empty function_name in node."""
        node: AST = {
            "type": "function_call",
            "function_name": "",
            "line": 1
        }
        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("undefined function '' at line 1", symbol_table["errors"])

    def test_node_missing_function_name_field(self):
        """Edge case: node missing function_name field (uses default empty string)."""
        node: AST = {
            "type": "function_call",
            "line": 30
        }
        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_node_missing_line_field(self):
        """Edge case: node missing line field (uses default 0)."""
        node: AST = {
            "type": "function_call",
            "function_name": "test_func"
        }
        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertIn("at line 0", symbol_table["errors"][0])

    def test_empty_symbol_table(self):
        """Edge case: completely empty symbol table."""
        node: AST = {
            "type": "function_call",
            "function_name": "any_func",
            "line": 1
        }
        symbol_table: SymbolTable = {}

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_function_with_custom_return_type(self):
        """Function with various custom return types."""
        test_cases = [
            ("float_func", "float"),
            ("string_func", "string"),
            ("bool_func", "bool"),
            ("array_func", "array"),
            ("custom_type_func", "MyCustomType")
        ]

        for func_name, expected_type in test_cases:
            with self.subTest(func_name=func_name):
                node: AST = {
                    "type": "function_call",
                    "function_name": func_name,
                    "line": 1
                }
                symbol_table: SymbolTable = {
                    "functions": {
                        func_name: {
                            "return_type": expected_type,
                            "params": [],
                            "line": 1,
                            "column": 0
                        }
                    },
                    "errors": []
                }

                result = _handle_function_call(node, symbol_table)

                self.assertEqual(result, expected_type)
                self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_without_return_type_field(self):
        """Function definition missing return_type field defaults to 'void'."""
        node: AST = {
            "type": "function_call",
            "function_name": "incomplete_func",
            "line": 1
        }
        symbol_table: SymbolTable = {
            "functions": {
                "incomplete_func": {
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        result = _handle_function_call(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 0)


class TestAddUndefinedFunctionError(unittest.TestCase):
    """Test cases for _add_undefined_function_error helper function."""

    def test_add_error_to_existing_list(self):
        """Add error to existing errors list."""
        symbol_table: SymbolTable = {
            "errors": ["existing error"]
        }

        _add_undefined_function_error(symbol_table, "test_func", 42)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1], "undefined function 'test_func' at line 42")

    def test_create_errors_list_when_missing(self):
        """Create errors list when it doesn't exist."""
        symbol_table: SymbolTable = {}

        _add_undefined_function_error(symbol_table, "missing_func", 10)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0], "undefined function 'missing_func' at line 10")

    def test_error_message_format(self):
        """Verify error message format with special characters in function name."""
        symbol_table: SymbolTable = {
            "errors": []
        }

        _add_undefined_function_error(symbol_table, "func_with_underscore", 99)

        self.assertEqual(
            symbol_table["errors"][0],
            "undefined function 'func_with_underscore' at line 99"
        )


if __name__ == "__main__":
    unittest.main()
