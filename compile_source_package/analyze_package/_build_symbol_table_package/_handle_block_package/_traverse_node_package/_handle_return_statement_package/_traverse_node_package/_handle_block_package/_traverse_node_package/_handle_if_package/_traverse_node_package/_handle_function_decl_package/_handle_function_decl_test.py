# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# === relative imports ===
from ._handle_function_decl_src import _handle_function_decl


# === Test Class ===
class TestHandleFunctionDecl(unittest.TestCase):
    """Test cases for _handle_function_decl function."""

    def _create_mock_symbol_table(self) -> Dict[str, Any]:
        """Create a fresh mock symbol table."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def _create_function_node(
        self,
        func_name: str,
        return_type: str,
        line: int,
        column: int,
        params: List[Dict[str, Any]] = None,
        body_children: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a mock function_decl AST node."""
        if params is None:
            params = []
        if body_children is None:
            body_children = []

        param_list_node = {
            "type": "param_list",
            "children": params,
            "line": line,
            "column": column
        }

        body_node = {
            "type": "block",
            "children": body_children,
            "line": line,
            "column": column
        }

        return {
            "type": "function_decl",
            "value": func_name,
            "data_type": return_type,
            "line": line,
            "column": column,
            "children": [param_list_node, body_node]
        }

    def _create_param_node(
        self,
        name: str,
        data_type: str,
        line: int,
        column: int
    ) -> Dict[str, Any]:
        """Create a mock parameter AST node."""
        return {
            "type": "param",
            "name": name,
            "data_type": data_type,
            "line": line,
            "column": column
        }

    @patch('._handle_function_decl_src._traverse_node')
    def test_happy_path_new_function(self, mock_traverse):
        """Test happy path: declaring a new function."""
        symbol_table = self._create_mock_symbol_table()
        node = self._create_function_node(
            func_name="my_func",
            return_type="int",
            line=10,
            column=5,
            params=[],
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        # Verify function info recorded
        self.assertIn("my_func", symbol_table["functions"])
        func_info = symbol_table["functions"]["my_func"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)

        # Verify scope management
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

        # Verify current_function restored
        self.assertIsNone(symbol_table["current_function"])

        # Verify _traverse_node called on body
        mock_traverse.assert_called_once()
        body_node = node["children"][1]
        mock_traverse.assert_called_with(body_node, symbol_table)

        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch('._handle_function_decl_src._traverse_node')
    def test_duplicate_function_declaration(self, mock_traverse):
        """Test error case: duplicate function declaration."""
        symbol_table = self._create_mock_symbol_table()
        
        # Pre-declare the function
        symbol_table["functions"]["my_func"] = {
            "return_type": "int",
            "params": [],
            "line": 5,
            "column": 1
        }

        node = self._create_function_node(
            func_name="my_func",
            return_type="int",
            line=10,
            column=5,
            params=[],
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        # Verify error recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertIn("already declared", error["message"])
        self.assertIn("my_func", error["message"])

        # Verify _traverse_node NOT called (early return)
        mock_traverse.assert_not_called()

        # Verify scope unchanged
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertIsNone(symbol_table["current_function"])

    @patch('._handle_function_decl_src._traverse_node')
    def test_function_with_parameters(self, mock_traverse):
        """Test function declaration with parameters."""
        symbol_table = self._create_mock_symbol_table()
        
        params = [
            self._create_param_node("x", "int", 11, 10),
            self._create_param_node("y", "char", 11, 20)
        ]
        
        node = self._create_function_node(
            func_name="add",
            return_type="int",
            line=10,
            column=5,
            params=params,
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        # Verify function params recorded
        func_info = symbol_table["functions"]["add"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "x")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "y")
        self.assertEqual(func_info["params"][1]["data_type"], "char")

        # Verify parameters added as local variables
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["is_declared"], True)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 11)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)

        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["y"]["is_declared"], True)
        self.assertEqual(symbol_table["variables"]["y"]["line"], 11)
        self.assertEqual(symbol_table["variables"]["y"]["column"], 20)
        self.assertEqual(symbol_table["variables"]["y"]["scope_level"], 1)

    @patch('._handle_function_decl_src._traverse_node')
    def test_scope_management(self, mock_traverse):
        """Test scope stack management during function declaration."""
        symbol_table = self._create_mock_symbol_table()
        
        # Start with existing scope
        symbol_table["current_scope"] = 2
        symbol_table["scope_stack"] = [0, 1]

        node = self._create_function_node(
            func_name="nested_func",
            return_type="char",
            line=15,
            column=3,
            params=[],
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        # Verify scope restored after function processing
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [0, 1])

    @patch('._handle_function_decl_src._traverse_node')
    def test_current_function_tracking(self, mock_traverse):
        """Test current_function is set during body processing."""
        symbol_table = self._create_mock_symbol_table()
        
        node = self._create_function_node(
            func_name="tracked_func",
            return_type="int",
            line=20,
            column=1,
            params=[],
            body_children=[]
        )

        # Mock _traverse_node to capture state during call
        def capture_state(body_node, st):
            # During body processing, current_function should be set
            self.assertEqual(st["current_function"], "tracked_func")
        
        mock_traverse.side_effect = capture_state

        _handle_function_decl(node, symbol_table)

        # Verify restored after processing
        self.assertIsNone(symbol_table["current_function"])

    @patch('._handle_function_decl_src._traverse_node')
    def test_function_with_char_return_type(self, mock_traverse):
        """Test function with char return type."""
        symbol_table = self._create_mock_symbol_table()
        
        node = self._create_function_node(
            func_name="get_char",
            return_type="char",
            line=25,
            column=7,
            params=[],
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["get_char"]
        self.assertEqual(func_info["return_type"], "char")

    @patch('._handle_function_decl_package._handle_function_decl_src._traverse_node')
    def test_multiple_parameters_same_type(self, mock_traverse):
        """Test function with multiple parameters of same type."""
        symbol_table = self._create_mock_symbol_table()
        
        params = [
            self._create_param_node("a", "int", 30, 10),
            self._create_param_node("b", "int", 30, 15),
            self._create_param_node("c", "int", 30, 20)
        ]
        
        node = self._create_function_node(
            func_name="sum_three",
            return_type="int",
            line=30,
            column=5,
            params=params,
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        func_info = symbol_table["functions"]["sum_three"]
        self.assertEqual(len(func_info["params"]), 3)
        
        # Verify all params added as variables
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        
        for param_name in ["a", "b", "c"]:
            self.assertEqual(symbol_table["variables"][param_name]["data_type"], "int")
            self.assertEqual(symbol_table["variables"][param_name]["scope_level"], 1)

    @patch('._handle_function_decl_package._handle_function_decl_src._traverse_node')
    def test_error_does_not_affect_existing_functions(self, mock_traverse):
        """Test that duplicate declaration error doesn't affect existing functions."""
        symbol_table = self._create_mock_symbol_table()
        
        # Pre-declare a function
        symbol_table["functions"]["existing_func"] = {
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 1
        }

        # Try to redeclare
        node = self._create_function_node(
            func_name="existing_func",
            return_type="char",
            line=40,
            column=5,
            params=[],
            body_children=[]
        )

        _handle_function_decl(node, symbol_table)

        # Verify original function info unchanged
        func_info = symbol_table["functions"]["existing_func"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 1)
        self.assertEqual(func_info["column"], 1)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
