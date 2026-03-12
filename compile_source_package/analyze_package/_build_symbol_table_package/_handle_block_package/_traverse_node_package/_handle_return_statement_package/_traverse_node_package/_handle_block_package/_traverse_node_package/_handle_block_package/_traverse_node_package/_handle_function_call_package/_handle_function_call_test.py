import unittest
from unittest.mock import patch, call
from typing import Any, Dict

# Import the function under test using relative import
from ._handle_function_call_src import _handle_function_call

# Type aliases
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def test_function_declared_correct_params(self):
        """Happy path: function is declared with correct parameter count."""
        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 2}
            ]
        }

        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": ["param1", "param2"],
                    "line": 1,
                    "column": 1
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify no errors were recorded
            self.assertEqual(len(symbol_table["errors"]), 0)

            # Verify _traverse_node was called for each parameter
            self.assertEqual(mock_traverse.call_count, 2)

    def test_function_not_declared(self):
        """Error case: function is not declared."""
        node: AST = {
            "type": "function_call",
            "value": "undefined_func",
            "line": 10,
            "column": 5,
            "children": []
        }

        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify error was recorded
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["type"], "error")
            self.assertIn("undefined_func", error["message"])
            self.assertEqual(error["line"], 10)
            self.assertEqual(error["column"], 5)

            # _traverse_node should not be called when function not declared
            mock_traverse.assert_not_called()

    def test_parameter_count_mismatch(self):
        """Error case: parameter count doesn't match declaration."""
        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1}
            ]
        }

        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": ["param1", "param2"],
                    "line": 1,
                    "column": 1
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify error was recorded for parameter mismatch
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["type"], "error")
            self.assertIn("expects 2 args, got 1", error["message"])

            # _traverse_node should still be called for parameters even with mismatch
            self.assertEqual(mock_traverse.call_count, 1)

    def test_missing_symbol_table_fields(self):
        """Edge case: symbol_table missing functions and errors fields."""
        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "line": 10,
            "column": 5,
            "children": []
        }

        symbol_table: SymbolTable = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify fields were created
            self.assertIn("functions", symbol_table)
            self.assertIn("errors", symbol_table)

            # Should record error for undeclared function
            self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_children(self):
        """Edge case: function call with no parameters."""
        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "line": 10,
            "column": 5,
            "children": []
        }

        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify no errors
            self.assertEqual(len(symbol_table["errors"]), 0)

            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()

    def test_missing_node_fields(self):
        """Edge case: node missing optional fields."""
        node: AST = {
            "type": "function_call",
            "value": "my_func"
        }

        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Should not crash, should use defaults for missing fields
            self.assertIn("errors", symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_parameters_traversed(self):
        """Test multiple parameters are traversed in order."""
        param1: AST = {"type": "literal", "value": 1}
        param2: AST = {"type": "literal", "value": 2}
        param3: AST = {"type": "literal", "value": 3}

        node: AST = {
            "type": "function_call",
            "value": "my_func",
            "line": 10,
            "column": 5,
            "children": [param1, param2, param3]
        }

        symbol_table: SymbolTable = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": ["p1", "p2", "p3"],
                    "line": 1,
                    "column": 1
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify _traverse_node called 3 times with correct arguments
            self.assertEqual(mock_traverse.call_count, 3)
            mock_traverse.assert_has_calls([
                call(param1, symbol_table),
                call(param2, symbol_table),
                call(param3, symbol_table)
            ])

    def test_function_with_zero_expected_params(self):
        """Test function declared with no parameters but called with some."""
        node: AST = {
            "type": "function_call",
            "value": "no_param_func",
            "line": 10,
            "column": 5,
            "children": [
                {"type": "literal", "value": 1}
            ]
        }

        symbol_table: SymbolTable = {
            "functions": {
                "no_param_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify error was recorded
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertIn("expects 0 args, got 1", error["message"])

            # _traverse_node should still be called for the parameter
            self.assertEqual(mock_traverse.call_count, 1)

    def test_error_preserves_existing_errors(self):
        """Test that new errors are appended, not replacing existing ones."""
        node: AST = {
            "type": "function_call",
            "value": "undefined_func",
            "line": 10,
            "column": 5,
            "children": []
        }

        symbol_table: SymbolTable = {
            "functions": {},
            "errors": [
                {"type": "error", "message": "Previous error", "line": 1, "column": 1}
            ]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Verify both errors exist
            self.assertEqual(len(symbol_table["errors"]), 2)
            self.assertEqual(symbol_table["errors"][0]["message"], "Previous error")
            self.assertIn("undefined_func", symbol_table["errors"][1]["message"])

    def test_empty_function_name(self):
        """Edge case: function name is empty string."""
        node: AST = {
            "type": "function_call",
            "value": "",
            "line": 10,
            "column": 5,
            "children": []
        }

        symbol_table: SymbolTable = {
            "functions": {},
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)

            # Should record error for empty function name
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertIn("''", error["message"])


if __name__ == "__main__":
    unittest.main()