# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._handle_function_def_src import _handle_function_def, _extract_params


class TestHandleFunctionDef(unittest.TestCase):
    """Test cases for _handle_function_def function."""

    def _create_symbol_table(self) -> Dict[str, Any]:
        """Helper to create a fresh symbol table."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_basic_function_def(self):
        """Test basic function definition with no parameters."""
        node = {
            "type": "function_def",
            "value": "main",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertIn("main", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["main"]["params"], {})
        self.assertEqual(symbol_table["functions"]["main"]["line"], 1)
        self.assertEqual(symbol_table["functions"]["main"]["column"], 0)

    def test_function_with_single_parameter(self):
        """Test function definition with one parameter."""
        node = {
            "type": "function_def",
            "value": "foo",
            "data_type": "char",
            "line": 5,
            "column": 10,
            "children": [
                {"type": "param", "value": "x", "data_type": "int"}
            ]
        }
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertIn("foo", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["foo"]["return_type"], "char")
        self.assertEqual(symbol_table["functions"]["foo"]["params"], {"x": "int"})
        self.assertEqual(symbol_table["functions"]["foo"]["line"], 5)
        self.assertEqual(symbol_table["functions"]["foo"]["column"], 10)

    def test_function_with_multiple_parameters(self):
        """Test function definition with multiple parameters."""
        node = {
            "type": "function_def",
            "value": "add",
            "data_type": "int",
            "line": 10,
            "column": 0,
            "children": [
                {"type": "param", "value": "a", "data_type": "int"},
                {"type": "param", "value": "b", "data_type": "int"}
            ]
        }
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertIn("add", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["add"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["add"]["params"], {"a": "int", "b": "int"})

    def test_function_overwrite(self):
        """Test that existing function is overwritten."""
        symbol_table = self._create_symbol_table()
        symbol_table["functions"]["existing"] = {
            "return_type": "char",
            "params": {"old": "int"},
            "line": 1,
            "column": 0
        }

        node = {
            "type": "function_def",
            "value": "existing",
            "data_type": "int",
            "line": 100,
            "column": 50,
            "children": [
                {"type": "param", "value": "new_param", "data_type": "char"}
            ]
        }

        _handle_function_def(node, symbol_table)

        self.assertEqual(symbol_table["functions"]["existing"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["existing"]["params"], {"new_param": "char"})
        self.assertEqual(symbol_table["functions"]["existing"]["line"], 100)
        self.assertEqual(symbol_table["functions"]["existing"]["column"], 50)

    def test_default_return_type(self):
        """Test that missing data_type defaults to 'int'."""
        node = {
            "type": "function_def",
            "value": "no_type",
            "line": 1,
            "column": 0,
            "children": []
        }
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertEqual(symbol_table["functions"]["no_type"]["return_type"], "int")

    def test_missing_fields(self):
        """Test handling of node with missing optional fields."""
        node = {}
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertIn("", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"][""]["return_type"], "int")
        self.assertEqual(symbol_table["functions"][""]["params"], {})
        self.assertEqual(symbol_table["functions"][""]["line"], 0)
        self.assertEqual(symbol_table["functions"][""]["column"], 0)

    def test_empty_children(self):
        """Test function with empty children list."""
        node = {
            "type": "function_def",
            "value": "empty_params",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertEqual(symbol_table["functions"]["empty_params"]["params"], {})

    def test_missing_children_key(self):
        """Test function when children key is missing."""
        node = {
            "type": "function_def",
            "value": "no_children",
            "data_type": "int",
            "line": 1,
            "column": 0
        }
        symbol_table = self._create_symbol_table()

        _handle_function_def(node, symbol_table)

        self.assertEqual(symbol_table["functions"]["no_children"]["params"], {})


class TestExtractParams(unittest.TestCase):
    """Test cases for _extract_params helper function."""

    def test_empty_children(self):
        """Test with empty children list."""
        result = _extract_params([])
        self.assertEqual(result, {})

    def test_single_parameter(self):
        """Test with single parameter."""
        children = [
            {"type": "param", "value": "x", "data_type": "int"}
        ]
        result = _extract_params(children)
        self.assertEqual(result, {"x": "int"})

    def test_multiple_parameters(self):
        """Test with multiple parameters."""
        children = [
            {"type": "param", "value": "a", "data_type": "int"},
            {"type": "param", "value": "b", "data_type": "char"},
            {"type": "param", "value": "c", "data_type": "int"}
        ]
        result = _extract_params(children)
        self.assertEqual(result, {"a": "int", "b": "char", "c": "int"})

    def test_default_param_type(self):
        """Test that missing data_type defaults to 'int'."""
        children = [
            {"type": "param", "value": "x"}
        ]
        result = _extract_params(children)
        self.assertEqual(result, {"x": "int"})

    def test_empty_param_name_skipped(self):
        """Test that parameters with empty names are skipped."""
        children = [
            {"type": "param", "value": "", "data_type": "int"},
            {"type": "param", "value": "valid", "data_type": "char"}
        ]
        result = _extract_params(children)
        self.assertEqual(result, {"valid": "char"})

    def test_missing_value_key(self):
        """Test parameter node without value key."""
        children = [
            {"type": "param", "data_type": "int"}
        ]
        result = _extract_params(children)
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
