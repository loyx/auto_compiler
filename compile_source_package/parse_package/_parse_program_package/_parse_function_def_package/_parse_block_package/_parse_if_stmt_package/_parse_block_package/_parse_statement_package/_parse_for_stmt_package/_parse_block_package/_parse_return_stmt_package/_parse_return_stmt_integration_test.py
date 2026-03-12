#!/usr/bin/env python3
"""Integration test for _parse_return_stmt function."""

import sys

# Project root directory
PROJECT_ROOT = "/Users/loyx/projects/autoapp_workspace/workspace"
sys.path.insert(0, PROJECT_ROOT)

from projects.cc.files.main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src import (
    _parse_return_stmt,
)


def test_bare_return_integration():
    """Test bare return statement (return;) through real parsing flow."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 1, "column": 5},
        {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
        {"type": "EOF", "value": "", "line": 1, "column": 12},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc",
    }
    
    result = _parse_return_stmt(parser_state)
    
    assert result["type"] == "RETURN", f"Expected type RETURN, got {result['type']}"
    assert result["value"] is None, f"Expected value None for bare return, got {result['value']}"
    assert result["line"] == 1, f"Expected line 1, got {result['line']}"
    assert result["column"] == 5, f"Expected column 5, got {result['column']}"
    assert parser_state["pos"] == 2, f"Expected pos 2 after parsing, got {parser_state['pos']}"
    print("✓ test_bare_return_integration passed")


def test_return_with_expression_integration():
    """Test return with expression (return x + 1;) through real parsing flow."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 2, "column": 3},
        {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 10},
        {"type": "PLUS", "value": "+", "line": 2, "column": 12},
        {"type": "NUMBER", "value": "1", "line": 2, "column": 14},
        {"type": "SEMICOLON", "value": ";", "line": 2, "column": 15},
        {"type": "EOF", "value": "", "line": 2, "column": 16},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc",
    }
    
    result = _parse_return_stmt(parser_state)
    
    assert result["type"] == "RETURN", f"Expected type RETURN, got {result['type']}"
    assert result["value"] is not None, "Expected value AST for return with expression"
    assert result["value"]["type"] in ["BINARY", "IDENTIFIER", "NUMBER"], f"Expected expression AST, got {result['value']}"
    assert result["line"] == 2, f"Expected line 2, got {result['line']}"
    assert result["column"] == 3, f"Expected column 3, got {result['column']}"
    assert parser_state["pos"] == 5, f"Expected pos 5 after parsing, got {parser_state['pos']}"
    print("✓ test_return_with_expression_integration passed")


def test_return_number_literal_integration():
    """Test return with number literal (return 42;) through real parsing flow."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 3, "column": 1},
        {"type": "NUMBER", "value": "42", "line": 3, "column": 8},
        {"type": "SEMICOLON", "value": ";", "line": 3, "column": 10},
        {"type": "EOF", "value": "", "line": 3, "column": 11},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc",
    }
    
    result = _parse_return_stmt(parser_state)
    
    assert result["type"] == "RETURN", f"Expected type RETURN, got {result['type']}"
    assert result["value"] is not None, "Expected value AST for return with expression"
    assert result["value"]["type"] == "NUMBER", f"Expected NUMBER AST, got {result['value']}"
    assert result["value"]["value"] == "42", f"Expected value 42, got {result['value'].get('value')}"
    assert parser_state["pos"] == 3, f"Expected pos 3 after parsing, got {parser_state['pos']}"
    print("✓ test_return_number_literal_integration passed")


def test_return_function_call_integration():
    """Test return with function call (return foo(a, b);) through real parsing flow."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 4, "column": 2},
        {"type": "IDENTIFIER", "value": "foo", "line": 4, "column": 9},
        {"type": "LPAREN", "value": "(", "line": 4, "column": 12},
        {"type": "IDENTIFIER", "value": "a", "line": 4, "column": 13},
        {"type": "COMMA", "value": ",", "line": 4, "column": 14},
        {"type": "IDENTIFIER", "value": "b", "line": 4, "column": 16},
        {"type": "RPAREN", "value": ")", "line": 4, "column": 17},
        {"type": "SEMICOLON", "value": ";", "line": 4, "column": 18},
        {"type": "EOF", "value": "", "line": 4, "column": 19},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc",
    }
    
    result = _parse_return_stmt(parser_state)
    
    assert result["type"] == "RETURN", f"Expected type RETURN, got {result['type']}"
    assert result["value"] is not None, "Expected value AST for return with expression"
    assert result["value"]["type"] == "CALL", f"Expected CALL AST, got {result['value']}"
    assert parser_state["pos"] == 8, f"Expected pos 8 after parsing, got {parser_state['pos']}"
    print("✓ test_return_function_call_integration passed")


def test_missing_semicolon_error_integration():
    """Test error handling when semicolon is missing after return expression."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 5, "column": 1},
        {"type": "NUMBER", "value": "100", "line": 5, "column": 8},
        {"type": "EOF", "value": "", "line": 5, "column": 11},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "error_test.cc",
    }
    
    try:
        _parse_return_stmt(parser_state)
        assert False, "Expected SyntaxError for missing semicolon"
    except SyntaxError as e:
        error_msg = str(e)
        assert "error_test.cc:5:1" in error_msg, f"Expected filename:line:column in error, got {error_msg}"
        assert "Expected ';'" in error_msg, f"Expected semicolon error message, got {error_msg}"
        print("✓ test_missing_semicolon_error_integration passed")


def test_missing_expression_error_integration():
    """Test error handling when nothing follows return token."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 6, "column": 1},
        {"type": "EOF", "value": "", "line": 6, "column": 7},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "error_test.cc",
    }
    
    try:
        _parse_return_stmt(parser_state)
        assert False, "Expected SyntaxError for missing expression/semicolon"
    except SyntaxError as e:
        error_msg = str(e)
        assert "error_test.cc:6:1" in error_msg, f"Expected filename:line:column in error, got {error_msg}"
        print("✓ test_missing_expression_error_integration passed")


def test_return_with_default_filename_integration():
    """Test return parsing when filename is not provided in parser_state."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 7, "column": 1},
        {"type": "SEMICOLON", "value": ";", "line": 7, "column": 7},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
    }
    
    result = _parse_return_stmt(parser_state)
    
    assert result["type"] == "RETURN", f"Expected type RETURN, got {result['type']}"
    assert result["value"] is None, f"Expected value None for bare return, got {result['value']}"
    assert parser_state["pos"] == 2, f"Expected pos 2 after parsing, got {parser_state['pos']}"
    print("✓ test_return_with_default_filename_integration passed")


def test_return_with_complex_expression_integration():
    """Test return with complex expression (return (a + b) * c;) through real parsing flow."""
    tokens = [
        {"type": "RETURN", "value": "return", "line": 8, "column": 1},
        {"type": "LPAREN", "value": "(", "line": 8, "column": 8},
        {"type": "IDENTIFIER", "value": "a", "line": 8, "column": 9},
        {"type": "PLUS", "value": "+", "line": 8, "column": 11},
        {"type": "IDENTIFIER", "value": "b", "line": 8, "column": 13},
        {"type": "RPAREN", "value": ")", "line": 8, "column": 14},
        {"type": "STAR", "value": "*", "line": 8, "column": 16},
        {"type": "IDENTIFIER", "value": "c", "line": 8, "column": 18},
        {"type": "SEMICOLON", "value": ";", "line": 8, "column": 19},
        {"type": "EOF", "value": "", "line": 8, "column": 20},
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc",
    }
    
    result = _parse_return_stmt(parser_state)
    
    assert result["type"] == "RETURN", f"Expected type RETURN, got {result['type']}"
    assert result["value"] is not None, "Expected value AST for return with expression"
    assert result["line"] == 8, f"Expected line 8, got {result['line']}"
    assert result["column"] == 1, f"Expected column 1, got {result['column']}"
    assert parser_state["pos"] == 9, f"Expected pos 9 after parsing, got {parser_state['pos']}"
    print("✓ test_return_with_complex_expression_integration passed")


if __name__ == "__main__":
    test_bare_return_integration()
    test_return_with_expression_integration()
    test_return_number_literal_integration()
    test_return_function_call_integration()
    test_missing_semicolon_error_integration()
    test_missing_expression_error_integration()
    test_return_with_default_filename_integration()
    test_return_with_complex_expression_integration()
    print("\n✓ All integration tests passed!")
