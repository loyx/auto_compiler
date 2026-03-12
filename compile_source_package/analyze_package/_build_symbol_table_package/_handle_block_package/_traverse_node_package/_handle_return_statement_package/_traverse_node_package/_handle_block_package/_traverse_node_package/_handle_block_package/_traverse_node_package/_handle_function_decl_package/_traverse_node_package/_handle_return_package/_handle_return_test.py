# === test file for _handle_return ===
import unittest
from typing import Dict

# Relative import from the same package
from ._handle_return_src import _handle_return


class TestHandleReturn(unittest.TestCase):
    """Test cases for _handle_return function."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_node = {
            "type": "return",
            "line": 10,
            "column": 5,
            "children": []
        }
        
        self.base_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def _create_symbol_table(self, current_function: str = None, 
                             functions: Dict = None, errors: list = None):
        """Helper to create symbol table with common fields."""
        st = self.base_symbol_table.copy()
        st["current_function"] = current_function
        st["functions"] = functions if functions else {}
        st["errors"] = errors if errors is not None else []
        return st

    def _create_return_node(self, children: list = None, line: int = 10, column: int = 5):
        """Helper to create return node."""
        node = self.base_node.copy()
        node["children"] = children if children is not None else []
        node["line"] = line
        node["column"] = column
        return node

    # === Happy Path Tests ===

    def test_happy_path_void_function_no_return_value(self):
        """Test void function with no return value - should pass without errors."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_matching_return_type(self):
        """Test function with matching return type - should pass without errors."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(
            children=[{
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 10,
                "column": 12
            }]
        )
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_case_insensitive_void(self):
        """Test VOID (uppercase) is treated as void."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "VOID",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    # === Error Case: Return Outside Function ===

    def test_error_return_outside_function(self):
        """Test return statement outside function context."""
        symbol_table = self._create_symbol_table(current_function=None)
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("return statement outside function", symbol_table["errors"][0])
        self.assertIn("line 10", symbol_table["errors"][0])
        self.assertIn("column 5", symbol_table["errors"][0])

    def test_error_return_outside_function_custom_location(self):
        """Test return outside function with custom line/column."""
        symbol_table = self._create_symbol_table(current_function=None)
        node = self._create_return_node(children=[], line=25, column=15)
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 25", symbol_table["errors"][0])
        self.assertIn("column 15", symbol_table["errors"][0])

    # === Error Case: Function Not Found ===

    def test_error_function_not_in_symbol_table(self):
        """Test when current_function is not found in functions dict."""
        symbol_table = self._create_symbol_table(
            current_function="nonexistent_func",
            functions={}
        )
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("function 'nonexistent_func' not found", symbol_table["errors"][0])

    # === Error Case: Missing Return Value ===

    def test_error_missing_return_value_non_void(self):
        """Test non-void function without return value."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("missing return value", symbol_table["errors"][0])
        self.assertIn("function 'my_func'", symbol_table["errors"][0])
        self.assertIn("int", symbol_table["errors"][0])

    def test_error_missing_return_value_char_type(self):
        """Test char return type without return value."""
        symbol_table = self._create_symbol_table(
            current_function="get_char",
            functions={
                "get_char": {
                    "return_type": "char",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("missing return value", symbol_table["errors"][0])
        self.assertIn("char", symbol_table["errors"][0])

    # === Error Case: Type Mismatch ===

    def test_error_return_type_mismatch(self):
        """Test return type mismatch between declared and actual."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(
            children=[{
                "type": "literal",
                "value": "hello",
                "data_type": "char",
                "line": 10,
                "column": 12
            }]
        )
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("return type mismatch", symbol_table["errors"][0])
        self.assertIn("Expected int", symbol_table["errors"][0])
        self.assertIn("got char", symbol_table["errors"][0])

    def test_error_return_type_mismatch_void_vs_int(self):
        """Test void function with int return value."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(
            children=[{
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 10,
                "column": 12
            }]
        )
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("return value provided in void function", symbol_table["errors"][0])

    # === Error Case: Cannot Determine Return Type ===

    def test_error_cannot_determine_return_type(self):
        """Test when return value node has no data_type."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(
            children=[{
                "type": "literal",
                "value": 42,
                # No data_type field
                "line": 10,
                "column": 12
            }]
        )
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("cannot determine return value type", symbol_table["errors"][0])

    # === Edge Cases ===

    def test_edge_case_no_errors_field_initialized(self):
        """Test that errors list is initialized if not present."""
        symbol_table = {
            "current_function": "my_func",
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        }
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_edge_case_multiple_return_statements_accumulate_errors(self):
        """Test that multiple return statements accumulate errors."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        
        # First return with wrong type
        node1 = self._create_return_node(
            children=[{
                "type": "literal",
                "value": "hello",
                "data_type": "char",
                "line": 10,
                "column": 5
            }]
        )
        _handle_return(node1, symbol_table)
        
        # Second return with missing value
        node2 = self._create_return_node(children=[], line=15, column=5)
        _handle_return(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_edge_case_empty_children_list(self):
        """Test return node with explicitly empty children list."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            }
        )
        node = self._create_return_node(children=[])
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("missing return value", symbol_table["errors"][0])

    def test_edge_case_node_missing_line_column(self):
        """Test error messages when node lacks line/column info."""
        symbol_table = self._create_symbol_table(current_function=None)
        node = {
            "type": "return",
            "children": []
            # No line or column
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("?", symbol_table["errors"][0])

    def test_edge_case_func_info_missing_return_type(self):
        """Test when function info exists but has no return_type."""
        symbol_table = self._create_symbol_table(
            current_function="my_func",
            functions={
                "my_func": {
                    "params": [],
                    "line": 1,
                    "column": 1
                    # No return_type
                }
            }
        )
        node = self._create_return_node(
            children=[{
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 10,
                "column": 12
            }]
        )
        
        _handle_return(node, symbol_table)
        
        # Should treat as void and error
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("return value provided in void function", symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()
