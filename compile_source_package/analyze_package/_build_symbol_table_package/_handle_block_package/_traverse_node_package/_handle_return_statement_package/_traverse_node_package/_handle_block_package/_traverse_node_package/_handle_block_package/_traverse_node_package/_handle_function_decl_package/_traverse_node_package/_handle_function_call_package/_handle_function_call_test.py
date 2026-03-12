# === Test file for _handle_function_call ===
import unittest
from typing import Any, Dict

# Relative import from the same package
from ._handle_function_call_src import _handle_function_call

# Type aliases for clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def _create_node(
        self,
        func_name: str,
        line: int = 1,
        column: int = 1,
        children: list = None
    ) -> AST:
        """Helper to create a function_call AST node."""
        if children is None:
            children = []
        return {
            "type": "function_call",
            "value": func_name,
            "line": line,
            "column": column,
            "children": children
        }

    def _create_arg_node(self, data_type: str, value: Any = None) -> AST:
        """Helper to create an argument AST node."""
        node = {
            "type": "argument",
            "data_type": data_type,
            "line": 1,
            "column": 1
        }
        if value is not None:
            node["value"] = value
        return node

    def test_happy_path_valid_function_call_no_params(self) -> None:
        """Test valid function call with no parameters."""
        # Setup: declare a function with no params
        self.symbol_table["functions"]["print"] = {
            "return_type": "void",
            "params": [],
            "line": 10,
            "column": 5
        }

        # Create node for function call
        node = self._create_node("print")

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: no errors should be recorded
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_happy_path_valid_function_call_with_params(self) -> None:
        """Test valid function call with matching parameters."""
        # Setup: declare a function with two params
        self.symbol_table["functions"]["add"] = {
            "return_type": "int",
            "params": ["int", "int"],
            "line": 10,
            "column": 5
        }

        # Create node for function call with two int args
        node = self._create_node("add", children=[
            self._create_arg_node("int", 5),
            self._create_arg_node("int", 10)
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: no errors should be recorded
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_undeclared_function_error(self) -> None:
        """Test error when calling an undeclared function."""
        # Setup: no functions declared

        # Create node for function call to undeclared function
        node = self._create_node("unknown_func", line=5, column=10)

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: error should be recorded
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "Function 'unknown_func' is not declared")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
        self.assertEqual(error["error_type"], "undeclared_function")

    def test_param_count_mismatch_too_few(self) -> None:
        """Test error when too few arguments provided."""
        # Setup: declare a function expecting 3 params
        self.symbol_table["functions"]["calculate"] = {
            "return_type": "int",
            "params": ["int", "int", "int"],
            "line": 10,
            "column": 5
        }

        # Create node with only 2 arguments
        node = self._create_node("calculate", line=15, column=20, children=[
            self._create_arg_node("int", 1),
            self._create_arg_node("int", 2)
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: param count mismatch error
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "Function 'calculate' expects 3 arguments, got 2")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 20)
        self.assertEqual(error["error_type"], "param_count_mismatch")

    def test_param_count_mismatch_too_many(self) -> None:
        """Test error when too many arguments provided."""
        # Setup: declare a function expecting 1 param
        self.symbol_table["functions"]["negate"] = {
            "return_type": "int",
            "params": ["int"],
            "line": 10,
            "column": 5
        }

        # Create node with 3 arguments
        node = self._create_node("negate", line=20, column=30, children=[
            self._create_arg_node("int", 1),
            self._create_arg_node("int", 2),
            self._create_arg_node("int", 3)
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: param count mismatch error
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "Function 'negate' expects 1 arguments, got 3")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 30)
        self.assertEqual(error["error_type"], "param_count_mismatch")

    def test_param_type_mismatch_first_arg(self) -> None:
        """Test error when first argument has wrong type."""
        # Setup: declare a function expecting int, int
        self.symbol_table["functions"]["add"] = {
            "return_type": "int",
            "params": ["int", "int"],
            "line": 10,
            "column": 5
        }

        # Create node with char as first arg
        node = self._create_node("add", line=25, column=15, children=[
            self._create_arg_node("char", "a"),
            self._create_arg_node("int", 5)
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: param type mismatch error
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(
            error["message"],
            "Argument 1 of function 'add' has type 'char', expected 'int'"
        )
        self.assertEqual(error["line"], 25)
        self.assertEqual(error["column"], 15)
        self.assertEqual(error["error_type"], "param_type_mismatch")

    def test_param_type_mismatch_second_arg(self) -> None:
        """Test error when second argument has wrong type."""
        # Setup: declare a function expecting int, char
        self.symbol_table["functions"]["process"] = {
            "return_type": "void",
            "params": ["int", "char"],
            "line": 10,
            "column": 5
        }

        # Create node with int as second arg (should be char)
        node = self._create_node("process", line=30, column=40, children=[
            self._create_arg_node("int", 10),
            self._create_arg_node("int", 20)
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: param type mismatch error
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(
            error["message"],
            "Argument 2 of function 'process' has type 'int', expected 'char'"
        )
        self.assertEqual(error["line"], 30)
        self.assertEqual(error["column"], 40)
        self.assertEqual(error["error_type"], "param_type_mismatch")

    def test_empty_function_name(self) -> None:
        """Test handling of empty function name."""
        # Setup: no functions declared

        # Create node with empty function name
        node = self._create_node("", line=1, column=1)

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: error for undeclared function (empty string not in functions)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["message"], "Function '' is not declared")
        self.assertEqual(error["error_type"], "undeclared_function")

    def test_missing_node_fields_uses_defaults(self) -> None:
        """Test that missing node fields use default values."""
        # Setup: no functions declared

        # Create minimal node with missing fields
        node: AST = {
            "type": "function_call",
            "value": "test_func"
            # Missing line, column, children
        }

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: error recorded with default line/column (0)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)

    def test_multiple_errors_not_accumulated_on_early_return(self) -> None:
        """Test that only one error is recorded per call (early return behavior)."""
        # Setup: declare a function expecting int, int
        self.symbol_table["functions"]["add"] = {
            "return_type": "int",
            "params": ["int", "int"],
            "line": 10,
            "column": 5
        }

        # Create node with wrong count AND wrong types
        # Should only report count mismatch (checked first)
        node = self._create_node("add", children=[
            self._create_arg_node("char", "a")  # Wrong type, but count check happens first
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: only one error (param count mismatch), not type mismatch
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "param_count_mismatch")

    def test_no_side_effects_on_valid_call(self) -> None:
        """Test that valid calls don't modify symbol_table except errors list."""
        # Setup
        self.symbol_table["functions"]["valid_func"] = {
            "return_type": "void",
            "params": [],
            "line": 10,
            "column": 5
        }
        original_functions = dict(self.symbol_table["functions"])
        original_variables = dict(self.symbol_table["variables"])

        node = self._create_node("valid_func")

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: no modifications to functions or variables
        self.assertEqual(self.symbol_table["functions"], original_functions)
        self.assertEqual(self.symbol_table["variables"], original_variables)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_char_type_matching(self) -> None:
        """Test that char type arguments match char parameters."""
        # Setup: declare a function expecting char
        self.symbol_table["functions"]["print_char"] = {
            "return_type": "void",
            "params": ["char"],
            "line": 10,
            "column": 5
        }

        # Create node with char arg
        node = self._create_node("print_char", children=[
            self._create_arg_node("char", "x")
        ])

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: no errors
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_error_preserves_existing_errors(self) -> None:
        """Test that new errors are appended, not replacing existing ones."""
        # Setup: add an existing error
        self.symbol_table["errors"].append({
            "message": "Previous error",
            "line": 1,
            "column": 1,
            "error_type": "previous"
        })

        # Create node for undeclared function
        node = self._create_node("new_func")

        # Execute
        _handle_function_call(node, self.symbol_table)

        # Verify: both errors exist
        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(self.symbol_table["errors"][0]["message"], "Previous error")
        self.assertEqual(self.symbol_table["errors"][1]["message"], "Function 'new_func' is not declared")


if __name__ == "__main__":
    unittest.main()
