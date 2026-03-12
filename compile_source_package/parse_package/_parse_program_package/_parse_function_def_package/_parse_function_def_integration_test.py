# -*- coding: utf-8 -*-
"""
Integration test for _parse_function_def function.
Tests the complete parsing flow through real module boundaries.
"""

import sys
import os

# Add the package directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from _parse_program_package._parse_function_def_package._parse_function_def_src import _parse_function_def


def test_happy_path_simple_function():
    """Test parsing a simple function with no parameters."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
        {"type": "IDENTIFIER", "value": "return", "line": 2, "column": 2},
        {"type": "NUMBER", "value": "0", "line": 2, "column": 9},
        {"type": "SEMICOLON", "value": ";", "line": 2, "column": 10},
        {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_function_def(parser_state)
    
    assert result["type"] == "FUNCTION_DEF"
    assert result["value"] == "main"
    assert result["return_type"] == "int"
    assert result["params"] == []
    assert result["line"] == 1
    assert result["column"] == 5
    assert result["body"]["type"] == "BLOCK"
    assert parser_state["pos"] == 9  # Position after RBRACE


def test_happy_path_function_with_params():
    """Test parsing a function with parameters."""
    tokens = [
        {"type": "IDENTIFIER", "value": "void", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 6},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 10},
        {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 14},
        {"type": "COMMA", "value": ",", "line": 1, "column": 15},
        {"type": "IDENTIFIER", "value": "char", "line": 1, "column": 17},
        {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 22},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 23},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 25},
        {"type": "RBRACE", "value": "}", "line": 2, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_function_def(parser_state)
    
    assert result["type"] == "FUNCTION_DEF"
    assert result["value"] == "foo"
    assert result["return_type"] == "void"
    assert len(result["params"]) == 2
    assert result["params"][0]["type"] == "PARAM"
    assert result["params"][0]["value"] == "x"
    assert result["params"][0]["param_type"] == "int"
    assert result["params"][1]["type"] == "PARAM"
    assert result["params"][1]["value"] == "y"
    assert result["params"][1]["param_type"] == "char"
    assert result["line"] == 1
    assert result["column"] == 6


def test_error_eof_after_return_type():
    """Test error when EOF occurs after return type."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    try:
        _parse_function_def(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "expected function name after return type" in str(e)


def test_error_non_identifier_function_name():
    """Test error when function name is not an identifier."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "NUMBER", "value": "123", "line": 1, "column": 5},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    try:
        _parse_function_def(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "expected function name after return type" in str(e)
        assert "1:5" in str(e)


def test_error_missing_lparen():
    """Test error when left parenthesis is missing."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    try:
        _parse_function_def(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "expected '(' after function name" in str(e)


def test_error_missing_rparen():
    """Test error when right parenthesis is missing."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 11},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    try:
        _parse_function_def(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "expected ')' after parameter list" in str(e)


def test_error_missing_lbrace():
    """Test error when left brace is missing."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "RBRACE", "value": "}", "line": 1, "column": 12},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    try:
        _parse_function_def(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "expected '{' before function body" in str(e)


def test_parser_state_position_update():
    """Test that parser_state position is correctly updated."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
        {"type": "RBRACE", "value": "}", "line": 2, "column": 1},
        {"type": "IDENTIFIER", "value": "next", "line": 3, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_function_def(parser_state)
    
    # Position should be after RBRACE (index 5), ready for next token
    assert parser_state["pos"] == 6
    # Verify we can continue parsing from the updated position
    assert tokens[parser_state["pos"]]["value"] == "next"


def test_function_with_complex_body():
    """Test parsing a function with a more complex body."""
    tokens = [
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "add", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 9},
        {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 13},
        {"type": "COMMA", "value": ",", "line": 1, "column": 14},
        {"type": "IDENTIFIER", "value": "int", "line": 1, "column": 16},
        {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 20},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 21},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 23},
        {"type": "IDENTIFIER", "value": "int", "line": 2, "column": 2},
        {"type": "IDENTIFIER", "value": "result", "line": 2, "column": 6},
        {"type": "ASSIGN", "value": "=", "line": 2, "column": 13},
        {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 15},
        {"type": "PLUS", "value": "+", "line": 2, "column": 17},
        {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 19},
        {"type": "SEMICOLON", "value": ";", "line": 2, "column": 20},
        {"type": "IDENTIFIER", "value": "return", "line": 3, "column": 2},
        {"type": "IDENTIFIER", "value": "result", "line": 3, "column": 9},
        {"type": "SEMICOLON", "value": ";", "line": 3, "column": 15},
        {"type": "RBRACE", "value": "}", "line": 4, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_function_def(parser_state)
    
    assert result["type"] == "FUNCTION_DEF"
    assert result["value"] == "add"
    assert result["return_type"] == "int"
    assert len(result["params"]) == 2
    assert result["body"]["type"] == "BLOCK"
    assert len(result["body"]["children"]) > 0


if __name__ == "__main__":
    test_happy_path_simple_function()
    print("✓ test_happy_path_simple_function passed")
    
    test_happy_path_function_with_params()
    print("✓ test_happy_path_function_with_params passed")
    
    test_error_eof_after_return_type()
    print("✓ test_error_eof_after_return_type passed")
    
    test_error_non_identifier_function_name()
    print("✓ test_error_non_identifier_function_name passed")
    
    test_error_missing_lparen()
    print("✓ test_error_missing_lparen passed")
    
    test_error_missing_rparen()
    print("✓ test_error_missing_rparen passed")
    
    test_error_missing_lbrace()
    print("✓ test_error_missing_lbrace passed")
    
    test_parser_state_position_update()
    print("✓ test_parser_state_position_update passed")
    
    test_function_with_complex_body()
    print("✓ test_function_with_complex_body passed")
    
    print("\nAll integration tests passed!")
