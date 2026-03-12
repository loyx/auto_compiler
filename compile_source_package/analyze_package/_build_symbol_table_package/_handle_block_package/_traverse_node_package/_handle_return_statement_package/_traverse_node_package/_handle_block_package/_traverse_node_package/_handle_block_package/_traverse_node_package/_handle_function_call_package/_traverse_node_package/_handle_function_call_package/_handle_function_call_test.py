import unittest
from unittest.mock import patch, call
from typing import Dict, Any

# Import the function under test using relative import
from ._handle_function_call_src import _handle_function_call


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function"""

    def _create_function_call_node(
        self,
        func_name: str,
        children: list = None,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a function call AST node"""
        return {
            "type": "function_call",
            "value": func_name,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def test_function_declared_no_error(self):
        """Test that calling a declared function does not record an error"""
        symbol_table = {
            "functions": {"my_func": {"return_type": "int", "params": []}}
        }
        
        node = self._create_function_call_node("my_func")
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table.get("errors", [])), 0)
        mock_traverse.assert_not_called()

    def test_function_declared_traverses_parameters(self):
        """Test that parameters are traversed when function is declared"""
        symbol_table = {
            "functions": {"my_func": {"return_type": "int", "params": ["int", "int"]}}
        }
        
        param1 = {"type": "literal", "value": 1, "line": 1, "column": 10}
        param2 = {"type": "literal", "value": 2, "line": 1, "column": 15}
        
        node = self._create_function_call_node("my_func", children=[param1, param2])
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table.get("errors", [])), 0)
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call(param1, symbol_table),
            call(param2, symbol_table)
        ])

    def test_function_not_declared_records_error(self):
        """Test that calling an undeclared function records an error"""
        symbol_table = {
            "functions": {"existing_func": {"return_type": "int", "params": []}},
            "errors": []
        }
        
        node = self._create_function_call_node("unknown_func", line=10, column=5)
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "undeclared_function")
        self.assertEqual(error["func_name"], "unknown_func")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        mock_traverse.assert_not_called()

    def test_function_not_declared_creates_errors_list(self):
        """Test that errors list is created if not present"""
        symbol_table = {
            "functions": {}
        }
        
        node = self._create_function_call_node("unknown_func", line=5, column=3)
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_call(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "undeclared_function")

    def test_no_parameters(self):
        """Test function call with no parameters"""
        symbol_table = {
            "functions": {"my_func": {"return_type": "int", "params": []}}
        }
        
        node = self._create_function_call_node("my_func", children=[])
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table.get("errors", [])), 0)
        mock_traverse.assert_not_called()

    def test_multiple_parameters(self):
        """Test function call with multiple parameters"""
        symbol_table = {
            "functions": {"my_func": {"return_type": "int", "params": ["int", "int", "char"]}}
        }
        
        param1 = {"type": "literal", "value": 1, "line": 1, "column": 10}
        param2 = {"type": "identifier", "value": "x", "line": 1, "column": 15}
        param3 = {"type": "literal", "value": "a", "line": 1, "column": 20}
        
        node = self._create_function_call_node("my_func", children=[param1, param2, param3])
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table.get("errors", [])), 0)
        self.assertEqual(mock_traverse.call_count, 3)

    def test_missing_line_column_defaults_to_zero(self):
        """Test that missing line/column default to 0 in error"""
        symbol_table = {
            "functions": {}
        }
        
        node = {
            "type": "function_call",
            "value": "unknown_func",
            "children": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_missing_functions_key_treated_as_empty(self):
        """Test that missing functions key is treated as empty dict"""
        symbol_table = {}
        
        node = self._create_function_call_node("any_func")
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "undeclared_function")

    def test_error_not_recorded_when_function_exists(self):
        """Test that no error is added when function is declared"""
        symbol_table = {
            "functions": {"printf": {"return_type": "int", "params": ["char"]}},
            "errors": [{"error_type": "some_other_error"}]
        }
        
        node = self._create_function_call_node("printf")
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "some_other_error")


if __name__ == "__main__":
    unittest.main()
