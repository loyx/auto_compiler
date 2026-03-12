# === imports ===
import unittest
from unittest.mock import patch

# === relative import of target function ===
from ._verify_function_call_src import _verify_function_call


class TestVerifyFunctionCall(unittest.TestCase):
    """Test cases for _verify_function_call function."""

    def setUp(self):
        """Set up common test fixtures."""
        self.filename = "test_file.c"
        self.context_stack = []

    def _create_function_call_node(self, name, args, line=10, column=5):
        """Helper to create a function call node."""
        return {
            "type": "function_call",
            "name": name,
            "args": args,
            "line": line,
            "column": column
        }

    def _create_arg_node(self, data_type, value=None, line=10, column=5):
        """Helper to create an argument node."""
        node = {
            "type": "identifier",
            "data_type": data_type,
            "line": line,
            "column": column
        }
        if value is not None:
            node["value"] = value
        return node

    def _create_symbol_table(self, functions=None, variables=None):
        """Helper to create a symbol table."""
        return {
            "functions": functions or {},
            "variables": variables or {},
            "current_scope": 0
        }

    def _create_function_info(self, return_type, params, line=5, column=1):
        """Helper to create function info for symbol table."""
        return {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }

    def _create_param_info(self, name, data_type):
        """Helper to create parameter info."""
        return {
            "name": name,
            "data_type": data_type
        }

    # === Happy Path Tests ===

    def test_valid_function_call_no_args(self):
        """Test valid function call with no arguments."""
        func_info = self._create_function_info("void", [])
        symbol_table = self._create_symbol_table(functions={"print": func_info})
        node = self._create_function_call_node("print", [])

        _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(node["data_type"], "void")

    def test_valid_function_call_with_matching_args(self):
        """Test valid function call with matching argument types."""
        params = [
            self._create_param_info("x", "int"),
            self._create_param_info("y", "int")
        ]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"add": func_info})

        args = [
            self._create_arg_node("int", 5),
            self._create_arg_node("int", 10)
        ]
        node = self._create_function_call_node("add", args)

        with patch("_verify_node_src._verify_node") as mock_verify:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(node["data_type"], "int")
        self.assertEqual(mock_verify.call_count, 2)

    def test_valid_function_call_multiple_types(self):
        """Test valid function call with multiple different argument types."""
        params = [
            self._create_param_info("name", "string"),
            self._create_param_info("age", "int"),
            self._create_param_info("active", "bool")
        ]
        func_info = self._create_function_info("void", params)
        symbol_table = self._create_symbol_table(functions={"register": func_info})

        args = [
            self._create_arg_node("string", "Alice"),
            self._create_arg_node("int", 25),
            self._create_arg_node("bool", True)
        ]
        node = self._create_function_call_node("register", args)

        with patch("_verify_node_src._verify_node") as mock_verify:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(node["data_type"], "void")
        self.assertEqual(mock_verify.call_count, 3)

    # === Error Case: Function Not Declared ===

    def test_undeclared_function_raises_error(self):
        """Test that calling an undeclared function raises ValueError."""
        symbol_table = self._create_symbol_table(functions={})
        node = self._create_function_call_node("unknown_func", [])

        with self.assertRaises(ValueError) as context:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("function 'unknown_func' was not declared", str(context.exception))
        self.assertIn("test_file.c:10:5", str(context.exception))

    def test_undeclared_function_with_custom_line_column(self):
        """Test error message includes correct line and column."""
        symbol_table = self._create_symbol_table(functions={})
        node = self._create_function_call_node("missing", [], line=42, column=15)

        with self.assertRaises(ValueError) as context:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("test_file.c:42:15", str(context.exception))

    # === Error Case: Argument Count Mismatch ===

    def test_too_few_arguments_raises_error(self):
        """Test that too few arguments raises ValueError."""
        params = [
            self._create_param_info("x", "int"),
            self._create_param_info("y", "int"),
            self._create_param_info("z", "int")
        ]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"sum": func_info})

        args = [self._create_arg_node("int", 1)]
        node = self._create_function_call_node("sum", args)

        with self.assertRaises(ValueError) as context:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("function 'sum' expects 3 arguments but got 1", str(context.exception))

    def test_too_many_arguments_raises_error(self):
        """Test that too many arguments raises ValueError."""
        params = [self._create_param_info("x", "int")]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"negate": func_info})

        args = [
            self._create_arg_node("int", 1),
            self._create_arg_node("int", 2),
            self._create_arg_node("int", 3)
        ]
        node = self._create_function_call_node("negate", args)

        with self.assertRaises(ValueError) as context:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("function 'negate' expects 1 arguments but got 3", str(context.exception))

    # === Error Case: Type Mismatch ===

    def test_type_mismatch_raises_error(self):
        """Test that type mismatch raises ValueError."""
        params = [self._create_param_info("x", "int")]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"increment": func_info})

        args = [self._create_arg_node("string", "hello")]
        node = self._create_function_call_node("increment", args)

        with patch("_verify_node_src._verify_node"):
            with self.assertRaises(ValueError) as context:
                _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("type mismatch for argument 1 in function 'increment'", str(context.exception))
        self.assertIn("expected 'int' but got 'string'", str(context.exception))

    def test_type_mismatch_second_argument(self):
        """Test type mismatch on second argument."""
        params = [
            self._create_param_info("x", "int"),
            self._create_param_info("y", "int")
        ]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"add": func_info})

        args = [
            self._create_arg_node("int", 5),
            self._create_arg_node("float", 3.14)
        ]
        node = self._create_function_call_node("add", args)

        with patch("_verify_node_src._verify_node"):
            with self.assertRaises(ValueError) as context:
                _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("type mismatch for argument 2 in function 'add'", str(context.exception))
        self.assertIn("expected 'int' but got 'float'", str(context.exception))

    def test_type_mismatch_exact_string_matching(self):
        """Test that type matching is exact (no coercion)."""
        params = [self._create_param_info("x", "int")]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"func": func_info})

        # unsigned int should not match int
        args = [self._create_arg_node("unsigned int", 5)]
        node = self._create_function_call_node("func", args)

        with patch("_verify_function_call_src._verify_node"):
            with self.assertRaises(ValueError) as context:
                _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("expected 'int' but got 'unsigned int'", str(context.exception))

    # === Edge Cases ===

    def test_empty_symbol_table_functions_key(self):
        """Test handling when symbol_table has no 'functions' key."""
        symbol_table = {"variables": {}, "current_scope": 0}
        node = self._create_function_call_node("func", [])

        with self.assertRaises(ValueError) as context:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("function 'func' was not declared", str(context.exception))

    def test_node_missing_optional_fields(self):
        """Test handling when node is missing optional fields."""
        func_info = self._create_function_info("void", [])
        symbol_table = self._create_symbol_table(functions={"test": func_info})
        node = {"type": "function_call", "name": "test"}

        _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(node["data_type"], "void")

    def test_function_info_missing_params(self):
        """Test handling when function info has no params."""
        func_info = {"return_type": "void", "line": 1, "column": 1}
        symbol_table = self._create_symbol_table(functions={"test": func_info})
        node = self._create_function_call_node("test", [])

        _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(node["data_type"], "void")

    def test_function_info_missing_return_type(self):
        """Test handling when function info has no return_type."""
        func_info = {"params": [], "line": 1, "column": 1}
        symbol_table = self._create_symbol_table(functions={"test": func_info})
        node = self._create_function_call_node("test", [])

        _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(node["data_type"], "")

    def test_arg_node_missing_data_type(self):
        """Test handling when argument node has no data_type."""
        params = [self._create_param_info("x", "int")]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"func": func_info})

        args = [{"type": "identifier", "value": 5}]
        node = self._create_function_call_node("func", args)

        with patch("_verify_function_call_src._verify_node"):
            with self.assertRaises(ValueError) as context:
                _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertIn("expected 'int' but got ''", str(context.exception))

    # === Mock Verification Tests ===

    def test_verify_node_called_for_each_argument(self):
        """Test that _verify_node is called for each argument."""
        params = [
            self._create_param_info("a", "int"),
            self._create_param_info("b", "int"),
            self._create_param_info("c", "int")
        ]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"sum": func_info})

        args = [
            self._create_arg_node("int", 1),
            self._create_arg_node("int", 2),
            self._create_arg_node("int", 3)
        ]
        node = self._create_function_call_node("sum", args)

        with patch("_verify_node_src._verify_node") as mock_verify:
            _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(mock_verify.call_count, 3)
        mock_verify.assert_any_call(args[0], symbol_table, self.context_stack, self.filename)
        mock_verify.assert_any_call(args[1], symbol_table, self.context_stack, self.filename)
        mock_verify.assert_any_call(args[2], symbol_table, self.context_stack, self.filename)

    def test_verify_node_propagates_exception(self):
        """Test that exceptions from _verify_node are propagated."""
        params = [self._create_param_info("x", "int")]
        func_info = self._create_function_info("int", params)
        symbol_table = self._create_symbol_table(functions={"func": func_info})

        args = [self._create_arg_node("int", 1)]
        node = self._create_function_call_node("func", args)

        with patch("_verify_function_call_src._verify_node") as mock_verify:
            mock_verify.side_effect = ValueError("Nested verification error")

            with self.assertRaises(ValueError) as context:
                _verify_function_call(node, symbol_table, self.context_stack, self.filename)

        self.assertEqual(str(context.exception), "Nested verification error")


if __name__ == "__main__":
    unittest.main()
