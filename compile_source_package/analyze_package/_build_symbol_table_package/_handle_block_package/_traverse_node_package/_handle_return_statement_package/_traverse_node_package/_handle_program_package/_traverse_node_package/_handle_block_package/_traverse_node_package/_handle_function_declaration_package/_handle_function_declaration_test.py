# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._handle_function_declaration_src import _handle_function_declaration, _extract_params


class TestHandleFunctionDeclaration(unittest.TestCase):
    """Test cases for _handle_function_declaration function."""

    def _create_node(
        self,
        func_name: str = "test_func",
        return_type: str = "int",
        line: int = 1,
        column: int = 1,
        children: list = None
    ) -> Dict[str, Any]:
        """Helper to create AST node."""
        return {
            "type": "function_declaration",
            "value": func_name,
            "data_type": return_type,
            "line": line,
            "column": column,
            "children": children or []
        }

    def _create_param_node(self, name: str, data_type: str) -> Dict[str, Any]:
        """Helper to create parameter AST node."""
        return {
            "type": "parameter",
            "value": name,
            "data_type": data_type
        }

    def test_happy_path_simple_function(self):
        """Test normal function declaration without parameters."""
        node = self._create_node("my_func", "int", 5, 10)
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        self.assertIn("my_func", symbol_table["functions"])
        func_info = symbol_table["functions"]["my_func"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 5)
        self.assertEqual(func_info["column"], 10)
        mock_traverse.assert_not_called()

    def test_function_with_parameters(self):
        """Test function declaration with parameters."""
        param_list = {
            "type": "parameter_list",
            "children": [
                self._create_param_node("x", "int"),
                self._create_param_node("y", "char")
            ]
        }
        node = self._create_node("add", "int", 3, 5, [param_list])
        symbol_table: Dict[str, Any] = {"functions": {}}

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        func_info = symbol_table["functions"]["add"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "x")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "y")
        self.assertEqual(func_info["params"][1]["data_type"], "char")

    def test_duplicate_function_name(self):
        """Test duplicate function name records error."""
        node = self._create_node("dup_func", "void", 10, 20)
        symbol_table: Dict[str, Any] = {
            "functions": {
                "dup_func": {"return_type": "int", "params": [], "line": 1, "column": 1}
            }
        }

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Duplicate function name 'dup_func'")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 20)
        self.assertEqual(error["type"], "duplicate_function")

    def test_empty_function_name(self):
        """Test empty function name returns early."""
        node = self._create_node("", "int")
        symbol_table: Dict[str, Any] = {"functions": {}}

        _handle_function_declaration(node, symbol_table)

        self.assertEqual(len(symbol_table["functions"]), 0)

    def test_creates_functions_key_if_missing(self):
        """Test creates 'functions' key if not present."""
        node = self._create_node("new_func")
        symbol_table: Dict[str, Any] = {}

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        self.assertIn("functions", symbol_table)
        self.assertIn("new_func", symbol_table["functions"])

    def test_creates_errors_key_if_missing(self):
        """Test creates 'errors' key if not present on duplicate."""
        node = self._create_node("existing", "void", 5, 5)
        symbol_table: Dict[str, Any] = {"functions": {"existing": {}}}

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        self.assertIn("errors", symbol_table)

    def test_current_function_context_restored(self):
        """Test current_function is restored after traversal."""
        node = self._create_node("temp_func")
        symbol_table: Dict[str, Any] = {
            "functions": {},
            "current_function": "original_func"
        }

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        self.assertEqual(symbol_table["current_function"], "original_func")

    def test_current_function_set_during_traversal(self):
        """Test current_function is set during traversal."""
        node = self._create_node("active_func")
        symbol_table: Dict[str, Any] = {"functions": {}}
        captured_context = []

        def capture_traverse(child, st):
            captured_context.append(st.get("current_function"))

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node", side_effect=capture_traverse):
            _handle_function_declaration(node, symbol_table)

        self.assertEqual(len(captured_context), 0)

    def test_traverses_children(self):
        """Test children are traversed."""
        child1 = {"type": "block", "children": []}
        child2 = {"type": "statement", "children": []}
        node = self._create_node("func_with_body", children=[child1, child2])
        symbol_table: Dict[str, Any] = {"functions": {}}

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        self.assertEqual(mock_traverse.call_count, 2)

    def test_default_return_type_void(self):
        """Test default return type is void when not specified."""
        node = {"type": "function_declaration", "value": "no_type", "line": 1, "column": 1, "children": []}
        symbol_table: Dict[str, Any] = {"functions": {}}

        with patch("compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node"):
            _handle_function_declaration(node, symbol_table)

        self.assertEqual(symbol_table["functions"]["no_type"]["return_type"], "void")


class TestExtractParams(unittest.TestCase):
    """Test cases for _extract_params helper function."""

    def test_empty_children(self):
        """Test with empty children list."""
        node = {"type": "function_declaration", "children": []}
        params = _extract_params(node)
        self.assertEqual(params, [])

    def test_no_parameter_list(self):
        """Test when no parameter_list child exists."""
        node = {
            "type": "function_declaration",
            "children": [{"type": "block"}, {"type": "statement"}]
        }
        params = _extract_params(node)
        self.assertEqual(params, [])

    def test_single_parameter(self):
        """Test with single parameter."""
        node = {
            "type": "function_declaration",
            "children": [{
                "type": "parameter_list",
                "children": [{
                    "type": "parameter",
                    "value": "x",
                    "data_type": "int"
                }]
            }]
        }
        params = _extract_params(node)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["name"], "x")
        self.assertEqual(params[0]["data_type"], "int")

    def test_multiple_parameters(self):
        """Test with multiple parameters."""
        node = {
            "type": "function_declaration",
            "children": [{
                "type": "parameter_list",
                "children": [
                    {"type": "parameter", "value": "a", "data_type": "char"},
                    {"type": "parameter", "value": "b", "data_type": "int"},
                    {"type": "parameter", "value": "c", "data_type": "void"}
                ]
            }]
        }
        params = _extract_params(node)
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0]["name"], "a")
        self.assertEqual(params[1]["name"], "b")
        self.assertEqual(params[2]["name"], "c")

    def test_parameter_list_with_non_parameter_children(self):
        """Test parameter_list with mixed children types."""
        node = {
            "type": "function_declaration",
            "children": [{
                "type": "parameter_list",
                "children": [
                    {"type": "parameter", "value": "x", "data_type": "int"},
                    {"type": "comment", "value": "some comment"},
                    {"type": "parameter", "value": "y", "data_type": "char"}
                ]
            }]
        }
        params = _extract_params(node)
        self.assertEqual(len(params), 2)

    def test_default_param_type_void(self):
        """Test default parameter type is void."""
        node = {
            "type": "function_declaration",
            "children": [{
                "type": "parameter_list",
                "children": [{"type": "parameter", "value": "x"}]
            }]
        }
        params = _extract_params(node)
        self.assertEqual(params[0]["data_type"], "void")


if __name__ == "__main__":
    unittest.main()
