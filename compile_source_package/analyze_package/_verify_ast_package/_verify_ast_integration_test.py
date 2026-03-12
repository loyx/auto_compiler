#!/usr/bin/env python3
"""Integration test for _verify_ast function."""

import pytest
from typing import Dict, Any

# Import the main function
from main_package.compile_source_package.analyze_package._verify_ast_package._verify_ast_src import (
    _verify_ast,
)


def create_simple_var_ast(var_name: str, data_type: str, line: int, column: int) -> Dict[str, Any]:
    """Create a simple variable declaration AST."""
    return {
        "type": "var_decl",
        "children": [
            {
                "type": "identifier",
                "value": var_name,
                "line": line,
                "column": column,
            },
            {
                "type": "type_specifier",
                "value": data_type,
                "line": line,
                "column": column,
            },
        ],
        "line": line,
        "column": column,
    }


def create_var_ref_ast(var_name: str, line: int, column: int) -> Dict[str, Any]:
    """Create a variable reference AST."""
    return {
        "type": "var_ref",
        "value": var_name,
        "line": line,
        "column": column,
    }


def create_function_call_ast(func_name: str, args: list, line: int, column: int) -> Dict[str, Any]:
    """Create a function call AST."""
    return {
        "type": "function_call",
        "value": func_name,
        "children": args,
        "line": line,
        "column": column,
    }


def create_block_ast(children: list, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Create a block statement AST."""
    return {
        "type": "block",
        "children": children,
        "line": line,
        "column": column,
    }


def symbol_table_with_variable(var_name: str, data_type: str, line: int, column: int) -> Dict[str, Any]:
    """Create a symbol table with a variable."""
    return {
        "variables": {
            var_name: {
                "data_type": data_type,
                "is_declared": True,
                "line": line,
                "column": column,
                "scope_level": 0,
            }
        },
        "functions": {},
        "current_scope": 0,
        "scope_stack": [0],
    }


def symbol_table_with_function(func_name: str, return_type: str, params: list) -> Dict[str, Any]:
    """Create a symbol table with a function."""
    return {
        "variables": {},
        "functions": {
            func_name: {
                "return_type": return_type,
                "params": params,
                "line": 1,
                "column": 1,
            }
        },
        "current_scope": 0,
        "scope_stack": [0],
    }


class TestVerifyAstIntegration:
    """Integration tests for _verify_ast function."""

    def test_valid_variable_declaration(self):
        """Test that valid variable declaration passes verification."""
        ast = create_simple_var_ast("x", "int", 1, 1)
        symbol_table = symbol_table_with_variable("x", "int", 1, 1)
        context_stack = []
        filename = "test.c"

        _verify_ast(ast, symbol_table, context_stack, filename)

        assert ast.get("data_type") == "int"

    def test_valid_variable_reference(self):
        """Test that valid variable reference passes verification."""
        ast = create_var_ref_ast("x", 1, 1)
        symbol_table = symbol_table_with_variable("x", "int", 1, 1)
        context_stack = []
        filename = "test.c"

        _verify_ast(ast, symbol_table, context_stack, filename)

        assert ast.get("data_type") == "int"

    def test_valid_function_call(self):
        """Test that valid function call passes verification."""
        ast = create_function_call_ast("test_func", [], 1, 1)
        symbol_table = symbol_table_with_function("test_func", "int", [])
        context_stack = []
        filename = "test.c"

        _verify_ast(ast, symbol_table, context_stack, filename)

        assert ast.get("data_type") == "int"

    def test_undeclared_variable_raises_error(self):
        """Test that referencing undeclared variable raises ValueError."""
        ast = create_var_ref_ast("y", 1, 1)
        symbol_table = symbol_table_with_variable("x", "int", 1, 1)
        context_stack = []
        filename = "test.c"

        with pytest.raises(ValueError, match="[Uu]ndeclared"):
            _verify_ast(ast, symbol_table, context_stack, filename)

    def test_function_not_found_raises_error(self):
        """Test that calling undefined function raises ValueError."""
        ast = create_function_call_ast("undefined_func", [], 1, 1)
        symbol_table = symbol_table_with_function("other_func", "int", [])
        context_stack = []
        filename = "test.c"

        with pytest.raises(ValueError, match="[Ff]unction"):
            _verify_ast(ast, symbol_table, context_stack, filename)

    def test_nested_block_structure(self):
        """Test verification of nested block structure."""
        var_decl = create_simple_var_ast("x", "int", 1, 1)
        var_ref = create_var_ref_ast("x", 2, 1)
        block = create_block_ast([var_decl, var_ref])

        symbol_table = symbol_table_with_variable("x", "int", 1, 1)
        context_stack = []
        filename = "test.c"

        _verify_ast(block, symbol_table, context_stack, filename)

        assert var_decl.get("data_type") == "int"
        assert var_ref.get("data_type") == "int"

    def test_empty_ast(self):
        """Test that empty AST is handled gracefully."""
        ast = {}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
        }
        context_stack = []
        filename = "test.c"

        _verify_ast(ast, symbol_table, context_stack, filename)

    def test_empty_symbol_table(self):
        """Test verification with empty symbol table."""
        ast = create_block_ast([])
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
        }
        context_stack = []
        filename = "test.c"

        _verify_ast(ast, symbol_table, context_stack, filename)

    def test_context_stack_modification(self):
        """Test that context stack can be modified during verification."""
        ast = create_block_ast([])
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
        }
        context_stack = []
        filename = "test.c"

        initial_len = len(context_stack)
        _verify_ast(ast, symbol_table, context_stack, filename)

        assert isinstance(context_stack, list)

    def test_complex_expression_tree(self):
        """Test verification of complex expression tree."""
        expr_ast = {
            "type": "binary_op",
            "value": "+",
            "children": [
                create_var_ref_ast("a", 1, 1),
                create_var_ref_ast("b", 1, 3),
            ],
            "line": 1,
            "column": 1,
        }

        symbol_table = {
            "variables": {
                "a": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
                "b": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
        }
        context_stack = []
        filename = "test.c"

        _verify_ast(expr_ast, symbol_table, context_stack, filename)

        assert expr_ast.get("data_type") == "int"
