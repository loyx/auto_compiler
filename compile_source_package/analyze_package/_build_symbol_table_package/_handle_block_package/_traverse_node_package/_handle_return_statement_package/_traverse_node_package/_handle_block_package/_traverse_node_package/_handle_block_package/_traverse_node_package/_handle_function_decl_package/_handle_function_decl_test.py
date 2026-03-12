import unittest
from unittest.mock import patch, call

# Import the function under test using relative import
from ._handle_function_decl_src import _handle_function_decl


class TestHandleFunctionDecl(unittest.TestCase):
    """Test cases for _handle_function_decl function."""

    def test_happy_path_basic_function_decl(self):
        """Test basic function declaration with all required fields."""
        node = {
            "type": "function_decl",
            "value": "myFunction",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_decl(node, symbol_table)

            # Verify function was registered
            self.assertIn("myFunction", symbol_table["functions"])
            func_info = symbol_table["functions"]["myFunction"]
            self.assertEqual(func_info["return_type"], "int")
            self.assertEqual(func_info["params"], [])
            self.assertEqual(func_info["line"], 10)
            self.assertEqual(func_info["column"], 5)

            # Verify current_function was set and restored
            self.assertIsNone(symbol_table.get("current_function"))

            # Verify _traverse_node was not called (no children)
            mock_traverse.assert_not_called()

    def test_function_with_char_return_type(self):
        """Test function declaration with char return type."""
        node = {
            "type": "function_decl",
            "value": "getString",
            "data_type": "char",
            "line": 15,
            "column": 3,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            self.assertEqual(symbol_table["functions"]["getString"]["return_type"], "char")

    def test_default_return_type_when_missing(self):
        """Test that default return type is 'int' when data_type is missing."""
        node = {
            "type": "function_decl",
            "value": "noReturnType",
            "line": 20,
            "column": 1,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            self.assertEqual(symbol_table["functions"]["noReturnType"]["return_type"], "int")

    def test_duplicate_function_declaration(self):
        """Test that duplicate function declarations are detected and reported."""
        node1 = {
            "type": "function_decl",
            "value": "duplicateFunc",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        node2 = {
            "type": "function_decl",
            "value": "duplicateFunc",
            "data_type": "char",
            "line": 20,
            "column": 8,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            # First declaration should succeed
            _handle_function_decl(node1, symbol_table)
            self.assertEqual(len(symbol_table.get("errors", [])), 0)
            self.assertIn("duplicateFunc", symbol_table["functions"])

            # Second declaration should fail and add error
            _handle_function_decl(node2, symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["type"], "error")
            self.assertIn("duplicateFunc", error["message"])
            self.assertEqual(error["line"], 20)
            self.assertEqual(error["column"], 8)

            # Function info should not be updated
            self.assertEqual(symbol_table["functions"]["duplicateFunc"]["return_type"], "int")

    def test_function_with_param_list(self):
        """Test function declaration with parameter list."""
        param1 = {"type": "param", "value": "x", "data_type": "int"}
        param2 = {"type": "param", "value": "y", "data_type": "char"}
        param_list = {
            "type": "param_list",
            "children": [param1, param2]
        }
        node = {
            "type": "function_decl",
            "value": "funcWithParams",
            "data_type": "int",
            "line": 5,
            "column": 2,
            "children": [param_list]
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            func_info = symbol_table["functions"]["funcWithParams"]
            self.assertEqual(len(func_info["params"]), 2)
            self.assertEqual(func_info["params"][0], param1)
            self.assertEqual(func_info["params"][1], param2)

    def test_function_without_param_list_child(self):
        """Test function declaration without param_list child."""
        body_node = {"type": "block", "children": []}
        node = {
            "type": "function_decl",
            "value": "noParams",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [body_node]
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            self.assertEqual(symbol_table["functions"]["noParams"]["params"], [])

    def test_symbol_table_initialization(self):
        """Test that symbol_table fields are initialized if missing."""
        node = {
            "type": "function_decl",
            "value": "initTest",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            self.assertIn("functions", symbol_table)
            self.assertIn("errors", symbol_table)
            self.assertIsInstance(symbol_table["functions"], dict)
            self.assertIsInstance(symbol_table["errors"], list)

    def test_current_function_save_and_restore(self):
        """Test that current_function is saved and restored after processing."""
        node = {
            "type": "function_decl",
            "value": "innerFunc",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table = {"current_function": "outerFunc"}

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_decl(node, symbol_table)

            # Should be restored to previous value
            self.assertEqual(symbol_table["current_function"], "outerFunc")

    def test_current_function_set_to_none_when_not_exists(self):
        """Test that current_function is set to None when not previously set."""
        node = {
            "type": "function_decl",
            "value": "standaloneFunc",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            # Should be None after restoration (was not set before)
            self.assertIsNone(symbol_table.get("current_function"))

    def test_traverse_node_called_for_all_children(self):
        """Test that _traverse_node is called for each child node."""
        child1 = {"type": "var_decl", "value": "x"}
        child2 = {"type": "block", "children": []}
        child3 = {"type": "assignment", "value": "y"}
        node = {
            "type": "function_decl",
            "value": "funcWithBody",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [child1, child2, child3]
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_decl(node, symbol_table)

            # Should be called 3 times, once for each child
            self.assertEqual(mock_traverse.call_count, 3)
            expected_calls = [
                call(child1, symbol_table),
                call(child2, symbol_table),
                call(child3, symbol_table)
            ]
            mock_traverse.assert_has_calls(expected_calls)

    def test_traverse_node_called_after_function_registration(self):
        """Test that _traverse_node is called after function is registered."""
        child = {"type": "block", "children": []}
        node = {
            "type": "function_decl",
            "value": "registrationOrder",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [child]
        }
        symbol_table = {}

        def check_registration(node_arg, st):
            # Function should already be registered when traverse_node is called
            self.assertIn("registrationOrder", st["functions"])

        with patch("._traverse_node_package._traverse_node_src._traverse_node", side_effect=check_registration):
            _handle_function_decl(node, symbol_table)

    def test_empty_function_name(self):
        """Test function declaration with empty function name."""
        node = {
            "type": "function_decl",
            "value": "",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            # Empty string should still be registered
            self.assertIn("", symbol_table["functions"])

    def test_missing_line_and_column(self):
        """Test that missing line and column default to -1."""
        node = {
            "type": "function_decl",
            "value": "noLocation",
            "data_type": "int",
            "children": []
        }
        symbol_table = {}

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            func_info = symbol_table["functions"]["noLocation"]
            self.assertEqual(func_info["line"], -1)
            self.assertEqual(func_info["column"], -1)

    def test_preserves_existing_symbol_table_data(self):
        """Test that existing symbol table data is preserved."""
        node = {
            "type": "function_decl",
            "value": "newFunc",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table = {
            "variables": {"x": {"data_type": "int"}},
            "functions": {"existingFunc": {"return_type": "char"}},
            "current_scope": 2,
            "scope_stack": [1]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_function_decl(node, symbol_table)

            # Existing data should be preserved
            self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
            self.assertIn("existingFunc", symbol_table["functions"])
            self.assertEqual(symbol_table["current_scope"], 2)
            self.assertEqual(symbol_table["scope_stack"], [1])
            # New function should be added
            self.assertIn("newFunc", symbol_table["functions"])


if __name__ == "__main__":
    unittest.main()
