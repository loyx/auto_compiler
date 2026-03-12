import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._handle_function_call_src import _handle_function_call

# Type aliases for test clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def test_valid_function_call(self):
        """Test successful function call with correct arguments."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"},
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "add",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 10, "column": 6},
                {"type": "literal", "value": 2, "data_type": "int", "line": 10, "column": 8}
            ]
        }
        symbol_table = {
            "functions": {"add": func_def},
            "errors": []
        }

        with patch("._handle_function_call_src._traverse_node"):
            _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_not_declared(self):
        """Test calling an undeclared function."""
        node = {
            "type": "function_call",
            "name": "unknown_func",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table = {
            "functions": {},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "error")
        self.assertIn("unknown_func", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)

    def test_wrong_argument_count_too_few(self):
        """Test calling function with too few arguments."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"},
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "add",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 10, "column": 6}
            ]
        }
        symbol_table = {
            "functions": {"add": func_def},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expects 2 arguments but got 1", symbol_table["errors"][0]["message"])

    def test_wrong_argument_count_too_many(self):
        """Test calling function with too many arguments."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "func",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 10, "column": 6},
                {"type": "literal", "value": 2, "data_type": "int", "line": 10, "column": 8}
            ]
        }
        symbol_table = {
            "functions": {"func": func_def},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expects 1 arguments but got 2", symbol_table["errors"][0]["message"])

    def test_wrong_argument_type(self):
        """Test calling function with wrong argument type."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"},
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "add",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 10, "column": 6},
                {"type": "literal", "value": "a", "data_type": "char", "line": 10, "column": 8}
            ]
        }
        symbol_table = {
            "functions": {"add": func_def},
            "errors": []
        }

        with patch("._handle_function_call_src._traverse_node"):
            _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Argument 1", symbol_table["errors"][0]["message"])
        self.assertIn("expects type 'int' but got 'char'", symbol_table["errors"][0]["message"])

    def test_multiple_type_mismatches(self):
        """Test multiple argument type mismatches."""
        func_def = {
            "return_type": "void",
            "params": [
                {"type": "int"},
                {"type": "char"},
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "test_func",
            "line": 15,
            "column": 3,
            "children": [
                {"type": "literal", "value": "a", "data_type": "char", "line": 15, "column": 12},
                {"type": "literal", "value": 1, "data_type": "int", "line": 15, "column": 15},
                {"type": "literal", "value": "b", "data_type": "char", "line": 15, "column": 18}
            ]
        }
        symbol_table = {
            "functions": {"test_func": func_def},
            "errors": []
        }

        with patch("._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_call(node, symbol_table)

        # Should have 2 errors (arg 0 and arg 2 mismatch)
        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_no_arguments_no_params(self):
        """Test calling function with no arguments and no parameters."""
        func_def = {
            "return_type": "void",
            "params": [],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "no_args_func",
            "line": 20,
            "column": 1,
            "children": []
        }
        symbol_table = {
            "functions": {"no_args_func": func_def},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_traverse_node_called_for_each_arg(self):
        """Test that _traverse_node is called for each argument."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"},
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "add",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 10, "column": 6},
                {"type": "literal", "value": 2, "data_type": "int", "line": 10, "column": 8}
            ]
        }
        symbol_table = {
            "functions": {"add": func_def},
            "errors": []
        }

        with patch("._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Should be called twice, once for each argument
            self.assertEqual(mock_traverse.call_count, 2)

    def test_early_return_on_function_not_declared(self):
        """Test that function returns early when function is not declared."""
        node = {
            "type": "function_call",
            "name": "unknown",
            "line": 5,
            "column": 2,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 5, "column": 10}
            ]
        }
        symbol_table = {
            "functions": {},
            "errors": []
        }

        with patch("._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Should not call _traverse_node since function is not declared
            mock_traverse.assert_not_called()
            self.assertEqual(len(symbol_table["errors"]), 1)

    def test_early_return_on_wrong_arg_count(self):
        """Test that function returns early on wrong argument count."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "func",
            "line": 5,
            "column": 2,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 5, "column": 10},
                {"type": "literal", "value": 2, "data_type": "int", "line": 5, "column": 12}
            ]
        }
        symbol_table = {
            "functions": {"func": func_def},
            "errors": []
        }

        with patch("._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Should not call _traverse_node since arg count is wrong
            mock_traverse.assert_not_called()
            self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_data_type_in_arg(self):
        """Test handling of argument with missing data_type."""
        func_def = {
            "return_type": "int",
            "params": [
                {"type": "int"}
            ],
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "func",
            "line": 5,
            "column": 2,
            "children": [
                {"type": "literal", "value": 1, "line": 5, "column": 10}
            ]
        }
        symbol_table = {
            "functions": {"func": func_def},
            "errors": []
        }

        with patch("._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_call(node, symbol_table)

        # Should report type mismatch (empty string vs "int")
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expects type 'int' but got ''", symbol_table["errors"][0]["message"])

    def test_missing_params_in_func_def(self):
        """Test handling of function definition with missing params."""
        func_def = {
            "return_type": "int",
            "line": 1,
            "column": 1
        }

        node = {
            "type": "function_call",
            "name": "func",
            "line": 5,
            "column": 2,
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 5, "column": 10}
            ]
        }
        symbol_table = {
            "functions": {"func": func_def},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        # Should report arg count mismatch (0 expected vs 1 actual)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expects 0 arguments but got 1", symbol_table["errors"][0]["message"])

    def test_missing_functions_in_symbol_table(self):
        """Test handling of symbol table without functions key."""
        node = {
            "type": "function_call",
            "name": "func",
            "line": 5,
            "column": 2,
            "children": []
        }
        symbol_table = {
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        # Should report function not declared
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("not declared", symbol_table["errors"][0]["message"])

    def test_missing_line_column_in_node(self):
        """Test handling of node with missing line/column."""
        node = {
            "type": "function_call",
            "name": "unknown",
            "children": []
        }
        symbol_table = {
            "functions": {},
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)


if __name__ == "__main__":
    unittest.main()
