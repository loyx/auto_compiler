# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._handle_function_call_src import _handle_function_call


# === type aliases for clarity ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def test_function_exists_with_matching_args_no_error(self):
        """Happy path: function declared with matching argument count."""
        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "arguments": [1, 2, 3],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": ["a", "b", "c"],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_not_declared_records_error(self):
        """Function not in symbol_table should record undefined error."""
        node: AST = {
            "type": "function_call",
            "value": "undefined_func",
            "arguments": [1, 2],
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "functions": {
                "other_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Undefined function: undefined_func")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)

    def test_argument_count_mismatch_records_error(self):
        """Argument count mismatch should record error."""
        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "arguments": [1, 2, 3, 4, 5],  # 5 args
            "line": 20,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": ["a", "b"],  # expects 2 params
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Argument count mismatch for my_func")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 10)

    def test_extract_function_name_from_value_field(self):
        """Function name extracted from 'value' field."""
        node: AST = {
            "type": "function_call",
            "value": "func_from_value",
            "arguments": [],
            "line": 5,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {
                "func_from_value": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_extract_function_name_from_children(self):
        """Function name extracted from children[0]['value'] when 'value' missing."""
        node: AST = {
            "type": "function_call",
            "children": [
                {"type": "identifier", "value": "func_from_children"},
                {"type": "arg", "value": 1}
            ],
            "line": 7,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "functions": {
                "func_from_children": {
                    "return_type": "void",
                    "params": ["x"],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_extract_arguments_from_arguments_field(self):
        """Arguments extracted from 'arguments' field."""
        node: AST = {
            "type": "function_call",
            "value": "test_func",
            "arguments": ["arg1", "arg2"],
            "line": 1,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {
                "test_func": {
                    "return_type": "void",
                    "params": ["p1", "p2"],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_extract_arguments_from_children(self):
        """Arguments extracted from children[1:] when 'arguments' missing."""
        node: AST = {
            "type": "function_call",
            "children": [
                {"type": "identifier", "value": "test_func"},
                {"type": "arg", "value": "arg1"},
                {"type": "arg", "value": "arg2"}
            ],
            "line": 1,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {
                "test_func": {
                    "return_type": "void",
                    "params": ["p1", "p2"],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_zero_arguments_match(self):
        """Function with no parameters called with no arguments."""
        node: AST = {
            "type": "function_call",
            "value": "no_arg_func",
            "arguments": [],
            "line": 1,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {
                "no_arg_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_zero_arguments_mismatch(self):
        """Function expecting args called with no arguments."""
        node: AST = {
            "type": "function_call",
            "value": "needs_args",
            "arguments": [],
            "line": 12,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "functions": {
                "needs_args": {
                    "return_type": "void",
                    "params": ["a", "b", "c"],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "Argument count mismatch for needs_args"
        )

    def test_missing_line_column_defaults_to_zero(self):
        """Missing line/column in node defaults to 0."""
        node: AST = {
            "type": "function_call",
            "value": "missing_pos"
        }
        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_errors_list_created_if_not_exists(self):
        """Errors list should be created if not present in symbol_table."""
        node: AST = {
            "type": "function_call",
            "value": "undefined",
            "line": 1,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {}
        }

        _handle_function_call(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_multiple_errors_accumulated(self):
        """Multiple function call errors should accumulate."""
        node1: AST = {
            "type": "function_call",
            "value": "func1",
            "arguments": [1],
            "line": 1,
            "column": 0
        }
        node2: AST = {
            "type": "function_call",
            "value": "func2",
            "arguments": [1, 2, 3],
            "line": 2,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {
                "func1": {
                    "return_type": "void",
                    "params": ["a", "b"],
                    "line": 1,
                    "column": 0
                },
                "func2": {
                    "return_type": "void",
                    "params": ["x"],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_function_call(node1, symbol_table)
        _handle_function_call(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_empty_function_name_from_missing_fields(self):
        """Empty function name when both value and children missing."""
        node: AST = {
            "type": "function_call",
            "arguments": [],
            "line": 1,
            "column": 0
        }
        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "Undefined function: "
        )


if __name__ == "__main__":
    unittest.main()
