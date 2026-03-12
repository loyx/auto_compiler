# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative import of target function ===
from ._build_symbol_table_src import _build_symbol_table


# === Test Helpers ===
def create_ast_node(
    node_type: str = "",
    value: Any = None,
    data_type: str = "int",
    line: int = 0,
    column: int = 0,
    children: list = None
) -> Dict[str, Any]:
    """Helper to create AST nodes with common fields."""
    return {
        "type": node_type,
        "value": value,
        "data_type": data_type,
        "line": line,
        "column": column,
        "children": children if children is not None else []
    }


def create_empty_symbol_table() -> Dict[str, Any]:
    """Helper to create an empty symbol table."""
    return {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": []
    }


# === Test Cases ===
class TestBuildSymbolTable(unittest.TestCase):
    """Test cases for _build_symbol_table function."""

    def test_empty_ast(self):
        """Test with empty AST - should not modify symbol_table."""
        ast = create_ast_node()
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_single_function_definition(self):
        """Test AST with a single function definition."""
        func_node = create_ast_node(
            node_type="function_def",
            value="main",
            data_type="int",
            line=1,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[func_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(len(symbol_table["functions"]), 1)
        self.assertIn("main", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["main"]["line"], 1)
        self.assertEqual(symbol_table["functions"]["main"]["column"], 0)
        self.assertEqual(symbol_table["functions"]["main"]["params"], [])
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_single_variable_declaration(self):
        """Test AST with a single variable declaration."""
        var_node = create_ast_node(
            node_type="variable_decl",
            value="x",
            data_type="int",
            line=5,
            column=10,
            children=[]
        )
        ast = create_ast_node(children=[var_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(len(symbol_table["variables"]), 1)
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["is_declared"], True)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_function_with_char_return_type(self):
        """Test function definition with char return type."""
        func_node = create_ast_node(
            node_type="function_def",
            value="get_char",
            data_type="char",
            line=3,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[func_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["get_char"]["return_type"], "char")

    def test_variable_with_char_type(self):
        """Test variable declaration with char type."""
        var_node = create_ast_node(
            node_type="variable_decl",
            value="c",
            data_type="char",
            line=2,
            column=5,
            children=[]
        )
        ast = create_ast_node(children=[var_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")

    def test_multiple_functions(self):
        """Test AST with multiple function definitions."""
        func1 = create_ast_node(
            node_type="function_def",
            value="func1",
            data_type="int",
            line=1,
            column=0,
            children=[]
        )
        func2 = create_ast_node(
            node_type="function_def",
            value="func2",
            data_type="char",
            line=10,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[func1, func2])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(len(symbol_table["functions"]), 2)
        self.assertIn("func1", symbol_table["functions"])
        self.assertIn("func2", symbol_table["functions"])

    def test_multiple_variables(self):
        """Test AST with multiple variable declarations."""
        var1 = create_ast_node(
            node_type="variable_decl",
            value="a",
            data_type="int",
            line=1,
            column=0,
            children=[]
        )
        var2 = create_ast_node(
            node_type="variable_decl",
            value="b",
            data_type="int",
            line=2,
            column=0,
            children=[]
        )
        var3 = create_ast_node(
            node_type="variable_decl",
            value="c",
            data_type="char",
            line=3,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[var1, var2, var3])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])

    def test_mixed_functions_and_variables(self):
        """Test AST with both functions and variables."""
        func_node = create_ast_node(
            node_type="function_def",
            value="main",
            data_type="int",
            line=1,
            column=0,
            children=[]
        )
        var_node = create_ast_node(
            node_type="variable_decl",
            value="x",
            data_type="int",
            line=5,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[func_node, var_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(len(symbol_table["functions"]), 1)
        self.assertEqual(len(symbol_table["variables"]), 1)
        self.assertIn("main", symbol_table["functions"])
        self.assertIn("x", symbol_table["variables"])

    def test_nested_nodes_traversal(self):
        """Test that nested nodes are properly traversed."""
        inner_var = create_ast_node(
            node_type="variable_decl",
            value="inner_var",
            data_type="int",
            line=10,
            column=5,
            children=[]
        )
        outer_node = create_ast_node(
            node_type="some_other_type",
            children=[inner_var]
        )
        ast = create_ast_node(children=[outer_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertIn("inner_var", symbol_table["variables"])

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._build_symbol_table_src._handle_block')
    def test_block_node_delegates_to_handle_block(self, mock_handle_block):
        """Test that block nodes are delegated to _handle_block."""
        block_node = create_ast_node(
            node_type="block",
            children=[]
        )
        ast = create_ast_node(children=[block_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        mock_handle_block.assert_called_once()
        call_args = mock_handle_block.call_args
        self.assertEqual(call_args[0][0], block_node)
        self.assertEqual(call_args[0][1], symbol_table)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._build_symbol_table_src._handle_block')
    def test_function_with_block_body(self, mock_handle_block):
        """Test function definition with block body."""
        block_node = create_ast_node(
            node_type="block",
            children=[]
        )
        func_node = create_ast_node(
            node_type="function_def",
            value="main",
            data_type="int",
            line=1,
            column=0,
            children=[block_node]
        )
        ast = create_ast_node(children=[func_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        mock_handle_block.assert_called_once()
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_function_with_param_list(self):
        """Test function definition with parameter list."""
        param1 = create_ast_node(
            node_type="param",
            value="a",
            data_type="int",
            line=1,
            column=10,
            children=[]
        )
        param2 = create_ast_node(
            node_type="param",
            value="b",
            data_type="char",
            line=1,
            column=15,
            children=[]
        )
        param_list = create_ast_node(
            node_type="param_list",
            children=[param1, param2]
        )
        func_node = create_ast_node(
            node_type="function_def",
            value="add",
            data_type="int",
            line=1,
            column=0,
            children=[param_list]
        )
        ast = create_ast_node(children=[func_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertIn("add", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["add"]["params"], ["a", "b"])
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["a"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["b"]["data_type"], "char")

    def test_duplicate_variable_declaration(self):
        """Test that duplicate variable declarations are not added twice."""
        var_node = create_ast_node(
            node_type="variable_decl",
            value="x",
            data_type="int",
            line=1,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[var_node, var_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(len(symbol_table["variables"]), 1)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)

    def test_scope_level_tracking(self):
        """Test that scope level is correctly tracked for variables."""
        var_node = create_ast_node(
            node_type="variable_decl",
            value="global_var",
            data_type="int",
            line=1,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[var_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["global_var"]["scope_level"], 0)

    def test_missing_type_field_defaults_to_int(self):
        """Test that missing data_type defaults to int for functions."""
        func_node = {
            "type": "function_def",
            "value": "no_type",
            "line": 1,
            "column": 0,
            "children": []
        }
        ast = create_ast_node(children=[func_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["no_type"]["return_type"], "int")

    def test_missing_line_column_defaults_to_zero(self):
        """Test that missing line/column defaults to 0."""
        func_node = {
            "type": "function_def",
            "value": "no_location",
            "data_type": "int",
            "children": []
        }
        ast = create_ast_node(children=[func_node])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["no_location"]["line"], 0)
        self.assertEqual(symbol_table["functions"]["no_location"]["column"], 0)

    def test_preserves_existing_symbol_table_entries(self):
        """Test that existing symbol table entries are preserved."""
        var_node = create_ast_node(
            node_type="variable_decl",
            value="new_var",
            data_type="int",
            line=5,
            column=0,
            children=[]
        )
        ast = create_ast_node(children=[var_node])
        symbol_table = create_empty_symbol_table()
        symbol_table["variables"]["existing_var"] = {
            "data_type": "char",
            "is_declared": True,
            "line": 1,
            "column": 0,
            "scope_level": 0
        }
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertIn("existing_var", symbol_table["variables"])
        self.assertIn("new_var", symbol_table["variables"])

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._build_symbol_table_src._handle_block')
    def test_multiple_block_nodes(self, mock_handle_block):
        """Test multiple block nodes in AST."""
        block1 = create_ast_node(node_type="block", children=[])
        block2 = create_ast_node(node_type="block", children=[])
        ast = create_ast_node(children=[block1, block2])
        symbol_table = create_empty_symbol_table()
        
        _build_symbol_table(ast, symbol_table)
        
        self.assertEqual(mock_handle_block.call_count, 2)


if __name__ == "__main__":
    unittest.main()
