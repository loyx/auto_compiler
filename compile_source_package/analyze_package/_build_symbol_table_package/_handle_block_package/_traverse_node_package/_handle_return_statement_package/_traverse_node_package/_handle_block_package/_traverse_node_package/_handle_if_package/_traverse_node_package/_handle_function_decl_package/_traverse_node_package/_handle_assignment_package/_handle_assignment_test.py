# === test file for _handle_assignment ===
import pytest
from typing import Dict, Any

# Import the function under test using relative import
from ._handle_assignment_src import _handle_assignment


# === Test Helpers ===
def create_ast_node(
    value: str = "x",
    data_type: str = "int",
    line: int = 1,
    column: int = 1
) -> Dict[str, Any]:
    """Helper to create AST node for assignment."""
    return {
        "type": "assignment",
        "value": value,
        "data_type": data_type,
        "line": line,
        "column": column
    }


def create_symbol_table(
    variables: Dict[str, Any] = None,
    errors: list = None
) -> Dict[str, Any]:
    """Helper to create symbol table."""
    table = {}
    if variables is not None:
        table["variables"] = variables
    if errors is not None:
        table["errors"] = errors
    return table


def create_variable_info(
    data_type: str = "int",
    is_declared: bool = True,
    line: int = 1,
    column: int = 1,
    scope_level: int = 0
) -> Dict[str, Any]:
    """Helper to create variable info dict."""
    return {
        "data_type": data_type,
        "is_declared": is_declared,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }


# === Test Cases ===

class TestHandleAssignmentHappyPath:
    """Test successful assignment scenarios."""
    
    def test_assignment_with_declared_variable_same_type_int(self):
        """Test assignment when variable is declared with matching int type."""
        symbol_table = create_symbol_table(
            variables={"x": create_variable_info(data_type="int")},
            errors=[]
        )
        node = create_ast_node(value="x", data_type="int", line=5, column=10)
        
        _handle_assignment(node, symbol_table)
        
        # No errors should be added
        assert len(symbol_table["errors"]) == 0
    
    def test_assignment_with_declared_variable_same_type_char(self):
        """Test assignment when variable is declared with matching char type."""
        symbol_table = create_symbol_table(
            variables={"c": create_variable_info(data_type="char")},
            errors=[]
        )
        node = create_ast_node(value="c", data_type="char", line=3, column=5)
        
        _handle_assignment(node, symbol_table)
        
        # No errors should be added
        assert len(symbol_table["errors"]) == 0


class TestHandleAssignmentUndeclaredVariable:
    """Test error handling for undeclared variables."""
    
    def test_undeclared_variable_adds_error(self):
        """Test that undeclared variable triggers error."""
        symbol_table = create_symbol_table(
            variables={"y": create_variable_info(data_type="int")},
            errors=[]
        )
        node = create_ast_node(value="x", data_type="int", line=10, column=20)
        
        _handle_assignment(node, symbol_table)
        
        # Error should be added
        assert len(symbol_table["errors"]) == 1
        assert "Undeclared variable 'x'" in symbol_table["errors"][0]
        assert "line 10" in symbol_table["errors"][0]
        assert "column 20" in symbol_table["errors"][0]
    
    def test_undeclared_variable_returns_early(self):
        """Test that function returns early after undeclared variable error."""
        symbol_table = create_symbol_table(
            variables={},
            errors=[]
        )
        node = create_ast_node(value="unknown", data_type="int", line=1, column=1)
        
        _handle_assignment(node, symbol_table)
        
        # Only one error, function should have returned early
        assert len(symbol_table["errors"]) == 1


class TestHandleAssignmentTypeMismatch:
    """Test error handling for type mismatches."""
    
    def test_type_mismatch_int_to_char(self):
        """Test error when assigning int to char variable."""
        symbol_table = create_symbol_table(
            variables={"c": create_variable_info(data_type="char")},
            errors=[]
        )
        node = create_ast_node(value="c", data_type="int", line=7, column=15)
        
        _handle_assignment(node, symbol_table)
        
        # Error should be added
        assert len(symbol_table["errors"]) == 1
        assert "Type mismatch" in symbol_table["errors"][0]
        assert "Expected 'char'" in symbol_table["errors"][0]
        assert "got 'int'" in symbol_table["errors"][0]
    
    def test_type_mismatch_char_to_int(self):
        """Test error when assigning char to int variable."""
        symbol_table = create_symbol_table(
            variables={"x": create_variable_info(data_type="int")},
            errors=[]
        )
        node = create_ast_node(value="x", data_type="char", line=12, column=8)
        
        _handle_assignment(node, symbol_table)
        
        # Error should be added
        assert len(symbol_table["errors"]) == 1
        assert "Type mismatch" in symbol_table["errors"][0]
        assert "Expected 'int'" in symbol_table["errors"][0]
        assert "got 'char'" in symbol_table["errors"][0]


class TestHandleAssignmentEdgeCases:
    """Test edge cases and initialization scenarios."""
    
    def test_missing_errors_list_in_symbol_table(self):
        """Test that missing 'errors' list is created automatically."""
        symbol_table = create_symbol_table(
            variables={"x": create_variable_info(data_type="int")}
            # No 'errors' key
        )
        node = create_ast_node(value="x", data_type="int")
        
        _handle_assignment(node, symbol_table)
        
        # errors list should be created
        assert "errors" in symbol_table
        assert isinstance(symbol_table["errors"], list)
    
    def test_missing_variables_dict_in_symbol_table(self):
        """Test that missing 'variables' dict is created automatically."""
        symbol_table = create_symbol_table(
            errors=[]
            # No 'variables' key
        )
        node = create_ast_node(value="x", data_type="int", line=1, column=1)
        
        _handle_assignment(node, symbol_table)
        
        # variables dict should be created
        assert "variables" in symbol_table
        assert isinstance(symbol_table["variables"], dict)
        # Error should be added since variable doesn't exist
        assert len(symbol_table["errors"]) == 1
    
    def test_empty_symbol_table(self):
        """Test handling of completely empty symbol table."""
        symbol_table = {}
        node = create_ast_node(value="x", data_type="int", line=1, column=1)
        
        _handle_assignment(node, symbol_table)
        
        # Both structures should be created
        assert "errors" in symbol_table
        assert "variables" in symbol_table
        # Error should be added for undeclared variable
        assert len(symbol_table["errors"]) == 1
    
    def test_default_line_column_values(self):
        """Test that missing line/column default to 0."""
        symbol_table = create_symbol_table(
            variables={},
            errors=[]
        )
        # Node without line/column
        node = {
            "type": "assignment",
            "value": "x",
            "data_type": "int"
        }
        
        _handle_assignment(node, symbol_table)
        
        assert len(symbol_table["errors"]) == 1
        assert "line 0" in symbol_table["errors"][0]
        assert "column 0" in symbol_table["errors"][0]
    
    def test_multiple_errors_accumulate(self):
        """Test that multiple assignment errors accumulate."""
        symbol_table = create_symbol_table(
            variables={"x": create_variable_info(data_type="int")},
            errors=[]
        )
        
        # First error: undeclared variable
        node1 = create_ast_node(value="y", data_type="int", line=1, column=1)
        _handle_assignment(node1, symbol_table)
        
        # Second error: type mismatch
        node2 = create_ast_node(value="x", data_type="char", line=2, column=2)
        _handle_assignment(node2, symbol_table)
        
        assert len(symbol_table["errors"]) == 2


class TestHandleAssignmentNoSideEffects:
    """Test that function doesn't modify unrelated data."""
    
    def test_does_not_modify_existing_variable_info(self):
        """Test that variable info is not modified on successful assignment."""
        var_info = create_variable_info(data_type="int")
        symbol_table = create_symbol_table(
            variables={"x": var_info},
            errors=[]
        )
        node = create_ast_node(value="x", data_type="int")
        
        _handle_assignment(node, symbol_table)
        
        # Variable info should remain unchanged
        assert symbol_table["variables"]["x"] is var_info
        assert symbol_table["variables"]["x"]["data_type"] == "int"
    
    def test_does_not_modify_other_variables(self):
        """Test that other variables are not affected."""
        symbol_table = create_symbol_table(
            variables={
                "x": create_variable_info(data_type="int"),
                "y": create_variable_info(data_type="char")
            },
            errors=[]
        )
        node = create_ast_node(value="x", data_type="int")
        
        _handle_assignment(node, symbol_table)
        
        # y should be unchanged
        assert symbol_table["variables"]["y"]["data_type"] == "char"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
