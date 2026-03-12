#!/usr/bin/env python3
"""
Integration test for _build_symbol_table function.
Tests the function through real module boundaries with minimal mocking.
"""

import sys

# Add project root to path
project_root = "/Users/loyx/projects/autoapp_workspace/workspace/projects/cc/files"
sys.path.insert(0, project_root)

from main_package.compile_source_package.analyze_package._build_symbol_table_package._build_symbol_table_src import (
    _build_symbol_table,
)


def _create_empty_symbol_table():
    """Create a properly initialized empty symbol table."""
    return {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": [],
    }


def test_empty_ast():
    """Test with empty AST - should not modify symbol table."""
    symbol_table = _create_empty_symbol_table()
    ast = {"type": "program", "children": []}
    
    _build_symbol_table(ast, symbol_table)
    
    assert symbol_table["variables"] == {}
    assert symbol_table["functions"] == {}
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


def test_single_function_definition():
    """Test with a single function definition."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "function_def",
                "value": "main",
                "data_type": "int",
                "line": 1,
                "column": 0,
                "children": [],
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    assert "main" in symbol_table["functions"]
    assert symbol_table["functions"]["main"]["return_type"] == "int"
    assert symbol_table["functions"]["main"]["line"] == 1
    assert symbol_table["functions"]["main"]["column"] == 0
    assert symbol_table["functions"]["main"]["params"] == []


def test_function_with_parameters():
    """Test function with parameter list."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "function_def",
                "value": "foo",
                "data_type": "int",
                "line": 1,
                "column": 0,
                "children": [
                    {
                        "type": "param_list",
                        "children": [
                            {
                                "type": "param",
                                "value": "x",
                                "data_type": "int",
                                "line": 1,
                                "column": 10,
                            },
                            {
                                "type": "param",
                                "value": "y",
                                "data_type": "char",
                                "line": 1,
                                "column": 15,
                            },
                        ],
                    },
                    {
                        "type": "block",
                        "children": [
                            {
                                "type": "variable_decl",
                                "value": "z",
                                "data_type": "int",
                                "line": 2,
                                "column": 4,
                            },
                        ],
                    },
                ],
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    # Verify function is recorded
    assert "foo" in symbol_table["functions"]
    assert symbol_table["functions"]["foo"]["return_type"] == "int"
    assert symbol_table["functions"]["foo"]["params"] == ["x", "y"]
    assert symbol_table["functions"]["foo"]["line"] == 1
    assert symbol_table["functions"]["foo"]["column"] == 0
    
    # Verify parameters are recorded as variables
    assert "x" in symbol_table["variables"]
    assert symbol_table["variables"]["x"]["data_type"] == "int"
    assert symbol_table["variables"]["x"]["scope_level"] == 1
    
    assert "y" in symbol_table["variables"]
    assert symbol_table["variables"]["y"]["data_type"] == "char"
    assert symbol_table["variables"]["y"]["scope_level"] == 1
    
    # Verify local variable is recorded
    assert "z" in symbol_table["variables"]
    assert symbol_table["variables"]["z"]["data_type"] == "int"
    assert symbol_table["variables"]["z"]["scope_level"] == 2


def test_multiple_functions():
    """Test with multiple function definitions."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "function_def",
                "value": "func1",
                "data_type": "int",
                "line": 1,
                "column": 0,
                "children": [],
            },
            {
                "type": "function_def",
                "value": "func2",
                "data_type": "char",
                "line": 5,
                "column": 0,
                "children": [],
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    assert len(symbol_table["functions"]) == 2
    assert "func1" in symbol_table["functions"]
    assert "func2" in symbol_table["functions"]
    assert symbol_table["functions"]["func1"]["return_type"] == "int"
    assert symbol_table["functions"]["func2"]["return_type"] == "char"


def test_nested_blocks():
    """Test with nested blocks to verify scope handling."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "function_def",
                "value": "main",
                "data_type": "int",
                "line": 1,
                "column": 0,
                "children": [
                    {
                        "type": "block",
                        "children": [
                            {
                                "type": "variable_decl",
                                "value": "a",
                                "data_type": "int",
                                "line": 2,
                                "column": 4,
                            },
                            {
                                "type": "block",
                                "children": [
                                    {
                                        "type": "variable_decl",
                                        "value": "b",
                                        "data_type": "char",
                                        "line": 3,
                                        "column": 8,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    # Verify both variables are recorded
    assert "a" in symbol_table["variables"]
    assert "b" in symbol_table["variables"]
    
    # Verify scope levels
    assert symbol_table["variables"]["a"]["scope_level"] == 1
    assert symbol_table["variables"]["b"]["scope_level"] == 2
    
    # Verify scope returns to initial state
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


def test_variable_declaration_only():
    """Test with variable declarations at global scope."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "variable_decl",
                "value": "global_var",
                "data_type": "int",
                "line": 1,
                "column": 0,
            },
            {
                "type": "variable_decl",
                "value": "another_var",
                "data_type": "char",
                "line": 2,
                "column": 0,
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    assert len(symbol_table["variables"]) == 2
    assert "global_var" in symbol_table["variables"]
    assert "another_var" in symbol_table["variables"]
    assert symbol_table["variables"]["global_var"]["data_type"] == "int"
    assert symbol_table["variables"]["another_var"]["data_type"] == "char"
    assert symbol_table["variables"]["global_var"]["scope_level"] == 0


def test_char_data_type():
    """Test with char data type."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "variable_decl",
                "value": "c",
                "data_type": "char",
                "line": 1,
                "column": 0,
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    assert "c" in symbol_table["variables"]
    assert symbol_table["variables"]["c"]["data_type"] == "char"


def test_default_data_type():
    """Test that missing data_type defaults to int."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "variable_decl",
                "value": "x",
                "line": 1,
                "column": 0,
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    assert "x" in symbol_table["variables"]
    assert symbol_table["variables"]["x"]["data_type"] == "int"


def test_function_with_block_and_statements():
    """Test function with block containing multiple statement types."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "function_def",
                "value": "test",
                "data_type": "int",
                "line": 1,
                "column": 0,
                "children": [
                    {
                        "type": "block",
                        "children": [
                            {
                                "type": "variable_decl",
                                "value": "local1",
                                "data_type": "int",
                                "line": 2,
                                "column": 4,
                            },
                            {
                                "type": "variable_decl",
                                "value": "local2",
                                "data_type": "char",
                                "line": 3,
                                "column": 4,
                            },
                        ],
                    },
                ],
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    assert "test" in symbol_table["functions"]
    assert "local1" in symbol_table["variables"]
    assert "local2" in symbol_table["variables"]
    assert symbol_table["variables"]["local1"]["scope_level"] == 1
    assert symbol_table["variables"]["local2"]["scope_level"] == 1


def test_scope_stack_management():
    """Test that scope stack is properly managed."""
    symbol_table = _create_empty_symbol_table()
    ast = {
        "type": "program",
        "children": [
            {
                "type": "function_def",
                "value": "outer",
                "data_type": "int",
                "line": 1,
                "column": 0,
                "children": [
                    {
                        "type": "block",
                        "children": [
                            {
                                "type": "function_def",
                                "value": "inner",
                                "data_type": "int",
                                "line": 2,
                                "column": 4,
                                "children": [],
                            },
                        ],
                    },
                ],
            },
        ],
    }
    
    _build_symbol_table(ast, symbol_table)
    
    # Both functions should be recorded
    assert "outer" in symbol_table["functions"]
    assert "inner" in symbol_table["functions"]
    
    # Scope should return to initial state
    assert symbol_table["current_scope"] == 0
    assert symbol_table["scope_stack"] == []


if __name__ == "__main__":
    test_empty_ast()
    print("✓ test_empty_ast passed")
    
    test_single_function_definition()
    print("✓ test_single_function_definition passed")
    
    test_function_with_parameters()
    print("✓ test_function_with_parameters passed")
    
    test_multiple_functions()
    print("✓ test_multiple_functions passed")
    
    test_nested_blocks()
    print("✓ test_nested_blocks passed")
    
    test_variable_declaration_only()
    print("✓ test_variable_declaration_only passed")
    
    test_char_data_type()
    print("✓ test_char_data_type passed")
    
    test_default_data_type()
    print("✓ test_default_data_type passed")
    
    test_function_with_block_and_statements()
    print("✓ test_function_with_block_and_statements passed")
    
    test_scope_stack_management()
    print("✓ test_scope_stack_management passed")
    
    print("\nAll integration tests passed!")
