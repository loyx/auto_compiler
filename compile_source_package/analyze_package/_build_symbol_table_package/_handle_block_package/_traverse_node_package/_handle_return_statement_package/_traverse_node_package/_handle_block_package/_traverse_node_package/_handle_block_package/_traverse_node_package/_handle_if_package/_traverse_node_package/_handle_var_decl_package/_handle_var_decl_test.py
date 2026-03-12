"""
Unit tests for _handle_var_decl function.
Tests variable declaration handling in AST traversal.
"""

from ._handle_var_decl_src import _handle_var_decl, AST, SymbolTable


def _create_symbol_table() -> SymbolTable:
    """Helper to create a fresh symbol table."""
    return {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": [],
        "current_function": "",
        "errors": []
    }


def _create_var_decl_node(
    var_name: str = "x",
    data_type: str = "int",
    line: int = 1,
    column: int = 1,
    node_type: str = "var_decl"
) -> AST:
    """Helper to create a var_decl AST node."""
    return {
        "type": node_type,
        "value": var_name,
        "data_type": data_type,
        "line": line,
        "column": column,
        "children": []
    }


class TestHandleVarDeclHappyPath:
    """Test happy path scenarios for _handle_var_decl."""

    def test_register_int_variable(self):
        """Test registering a variable with int data type."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="x", data_type="int", line=1, column=1)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "x" in symbol_table["variables"]
        assert symbol_table["variables"]["x"]["data_type"] == "int"
        assert symbol_table["variables"]["x"]["is_declared"] is True
        assert symbol_table["variables"]["x"]["line"] == 1
        assert symbol_table["variables"]["x"]["column"] == 1
        assert symbol_table["variables"]["x"]["scope_level"] == 0

    def test_register_char_variable(self):
        """Test registering a variable with char data type."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="ch", data_type="char", line=5, column=10)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "ch" in symbol_table["variables"]
        assert symbol_table["variables"]["ch"]["data_type"] == "char"
        assert symbol_table["variables"]["ch"]["line"] == 5
        assert symbol_table["variables"]["ch"]["column"] == 10

    def test_register_variable_at_different_scope(self):
        """Test registering a variable at a non-zero scope level."""
        symbol_table = _create_symbol_table()
        symbol_table["current_scope"] = 2
        node = _create_var_decl_node(var_name="y", data_type="int")
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert symbol_table["variables"]["y"]["scope_level"] == 2

    def test_register_multiple_variables(self):
        """Test registering multiple variables sequentially."""
        symbol_table = _create_symbol_table()
        node1 = _create_var_decl_node(var_name="a", data_type="int", line=1, column=1)
        node2 = _create_var_decl_node(var_name="b", data_type="char", line=2, column=1)
        
        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "a" in symbol_table["variables"]
        assert "b" in symbol_table["variables"]
        assert symbol_table["variables"]["a"]["data_type"] == "int"
        assert symbol_table["variables"]["b"]["data_type"] == "char"


class TestHandleVarDeclInvalidDataType:
    """Test invalid data type scenarios."""

    def test_invalid_data_type_float(self):
        """Test error recording for float data type."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="x", data_type="float", line=3, column=5)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert symbol_table["errors"][0]["type"] == "error"
        assert "Invalid data type 'float'" in symbol_table["errors"][0]["message"]
        assert symbol_table["errors"][0]["line"] == 3
        assert symbol_table["errors"][0]["column"] == 5
        assert "x" not in symbol_table["variables"]

    def test_invalid_data_type_string(self):
        """Test error recording for string data type."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="s", data_type="string", line=4, column=2)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "Invalid data type 'string'" in symbol_table["errors"][0]["message"]
        assert "s" not in symbol_table["variables"]

    def test_invalid_data_type_empty(self):
        """Test error recording for empty data type."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="x", data_type="", line=1, column=1)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "Invalid data type ''" in symbol_table["errors"][0]["message"]
        assert "x" not in symbol_table["variables"]

    def test_invalid_data_type_void(self):
        """Test error recording for void data type."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="x", data_type="void", line=1, column=1)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "Invalid data type 'void'" in symbol_table["errors"][0]["message"]


class TestHandleVarDeclMissingVariableName:
    """Test missing variable name scenarios."""

    def test_missing_variable_name_empty_value(self):
        """Test error recording when variable name is empty."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="", data_type="int", line=2, column=3)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert symbol_table["errors"][0]["type"] == "error"
        assert "Variable name not found" in symbol_table["errors"][0]["message"]
        assert symbol_table["errors"][0]["line"] == 2
        assert symbol_table["errors"][0]["column"] == 3

    def test_missing_variable_name_no_value_field(self):
        """Test error recording when value field is missing."""
        symbol_table = _create_symbol_table()
        node = {
            "type": "var_decl",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "Variable name not found" in symbol_table["errors"][0]["message"]


class TestHandleVarDeclDuplicateDeclaration:
    """Test duplicate variable declaration scenarios."""

    def test_duplicate_variable_declaration(self):
        """Test error recording for duplicate variable declaration."""
        symbol_table = _create_symbol_table()
        node1 = _create_var_decl_node(var_name="x", data_type="int", line=1, column=1)
        node2 = _create_var_decl_node(var_name="x", data_type="char", line=5, column=10)
        
        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert symbol_table["errors"][0]["type"] == "error"
        assert "Variable 'x' already declared" in symbol_table["errors"][0]["message"]
        assert symbol_table["errors"][0]["line"] == 5
        assert symbol_table["errors"][0]["column"] == 10
        # Original variable should remain unchanged
        assert symbol_table["variables"]["x"]["data_type"] == "int"
        assert symbol_table["variables"]["x"]["line"] == 1

    def test_duplicate_with_different_data_type(self):
        """Test that duplicate detection works regardless of data type."""
        symbol_table = _create_symbol_table()
        node1 = _create_var_decl_node(var_name="count", data_type="int", line=1, column=1)
        node2 = _create_var_decl_node(var_name="count", data_type="int", line=3, column=1)
        
        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "Variable 'count' already declared" in symbol_table["errors"][0]["message"]


class TestHandleVarDeclEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_missing_line_column_defaults_to_zero(self):
        """Test that missing line/column default to 0 in error messages."""
        symbol_table = _create_symbol_table()
        node = {
            "type": "var_decl",
            "value": "x",
            "data_type": "invalid",
            "children": []
        }
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert symbol_table["errors"][0]["line"] == 0
        assert symbol_table["errors"][0]["column"] == 0

    def test_symbol_table_without_variables_key(self):
        """Test that variables dict is created if not present."""
        symbol_table = {
            "functions": {},
            "current_scope": 0,
            "errors": []
        }
        node = _create_var_decl_node(var_name="x", data_type="int")
        
        _handle_var_decl(node, symbol_table)
        
        assert "variables" in symbol_table
        assert "x" in symbol_table["variables"]
        assert len(symbol_table["errors"]) == 0

    def test_variable_name_from_children_identifier(self):
        """Test extracting variable name from children identifier node."""
        symbol_table = _create_symbol_table()
        node = {
            "type": "var_decl",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "myVar"}
            ]
        }
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "myVar" in symbol_table["variables"]

    def test_variable_name_from_children_string(self):
        """Test extracting variable name from children string node."""
        symbol_table = _create_symbol_table()
        node = {
            "type": "var_decl",
            "data_type": "char",
            "line": 1,
            "column": 1,
            "children": [
                {"type": "string", "value": "chVar"}
            ]
        }
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "chVar" in symbol_table["variables"]

    def test_variable_name_from_children_first_string(self):
        """Test extracting variable name when first child is a string."""
        symbol_table = _create_symbol_table()
        node = {
            "type": "var_decl",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": ["directVar"]
        }
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "directVar" in symbol_table["variables"]

    def test_value_takes_precedence_over_children(self):
        """Test that value field takes precedence over children for variable name."""
        symbol_table = _create_symbol_table()
        node = {
            "type": "var_decl",
            "value": "valueVar",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "childVar"}
            ]
        }
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "valueVar" in symbol_table["variables"]
        assert "childVar" not in symbol_table["variables"]

    def test_case_sensitive_variable_names(self):
        """Test that variable names are case-sensitive."""
        symbol_table = _create_symbol_table()
        node1 = _create_var_decl_node(var_name="Var", data_type="int", line=1, column=1)
        node2 = _create_var_decl_node(var_name="var", data_type="char", line=2, column=1)
        
        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "Var" in symbol_table["variables"]
        assert "var" in symbol_table["variables"]
        assert symbol_table["variables"]["Var"]["data_type"] == "int"
        assert symbol_table["variables"]["var"]["data_type"] == "char"

    def test_special_characters_in_variable_name(self):
        """Test variable names with special characters (should be accepted as-is)."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="_private_var", data_type="int", line=1, column=1)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 0
        assert "_private_var" in symbol_table["variables"]


class TestHandleVarDeclSideEffects:
    """Test that function has correct side effects."""

    def test_does_not_modify_other_symbol_table_fields(self):
        """Test that function only modifies variables and errors fields."""
        symbol_table = _create_symbol_table()
        symbol_table["functions"]["main"] = {"name": "main", "return_type": "int"}
        symbol_table["current_function"] = "main"
        original_functions = symbol_table["functions"].copy()
        original_current_function = symbol_table["current_function"]
        
        node = _create_var_decl_node(var_name="x", data_type="int")
        _handle_var_decl(node, symbol_table)
        
        assert symbol_table["functions"] == original_functions
        assert symbol_table["current_function"] == original_current_function

    def test_error_does_not_add_variable(self):
        """Test that when error occurs, variable is not added to symbol table."""
        symbol_table = _create_symbol_table()
        node = _create_var_decl_node(var_name="x", data_type="invalid", line=1, column=1)
        
        _handle_var_decl(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "x" not in symbol_table["variables"]

    def test_duplicate_error_preserves_original_variable(self):
        """Test that duplicate declaration error preserves original variable info."""
        symbol_table = _create_symbol_table()
        node1 = _create_var_decl_node(var_name="x", data_type="int", line=1, column=1)
        node2 = _create_var_decl_node(var_name="x", data_type="char", line=10, column=5)
        
        _handle_var_decl(node1, symbol_table)
        original_var_info = symbol_table["variables"]["x"].copy()
        _handle_var_decl(node2, symbol_table)
        
        assert symbol_table["variables"]["x"] == original_var_info
        assert len(symbol_table["errors"]) == 1
