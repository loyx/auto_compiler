#!/usr/bin/env python3
"""
Integration test for _parse_while_stmt function.

Tests the while statement parser with realistic token streams through real module boundaries.
"""

import sys
import os

# Setup path for imports from the parse package
_base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _base_dir)

from _parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt


def test_valid_while_statement():
    """Test parsing a valid while statement with simple condition and empty body."""
    tokens = [
        {"type": "WHILE", "value": "while", "line": 1, "column": 1},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
        {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
        {"type": "GREATER", "value": ">", "line": 1, "column": 10},
        {"type": "INTEGER", "value": 0, "line": 1, "column": 12},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 13},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 15},
        {"type": "RBRACE", "value": "}", "line": 1, "column": 16},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.src"
    }
    
    result = _parse_while_stmt(parser_state)
    
    assert result["type"] == "WHILE_STMT"
    assert result["line"] == 1
    assert result["column"] == 1
    assert len(result["children"]) == 2
    
    condition, body = result["children"]
    assert condition["type"] in ["BINARY_OP", "IDENTIFIER"]
    assert body["type"] == "BLOCK"
    assert parser_state["pos"] == 8


def test_while_with_complex_condition():
    """Test while statement with complex boolean condition."""
    tokens = [
        {"type": "WHILE", "value": "while", "line": 2, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 2, "column": 11},
        {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 12},
        {"type": "AND", "value": "&&", "line": 2, "column": 14},
        {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 17},
        {"type": "RPAREN", "value": ")", "line": 2, "column": 18},
        {"type": "LBRACE", "value": "{", "line": 2, "column": 20},
        {"type": "RBRACE", "value": "}", "line": 2, "column": 21},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.src"
    }
    
    result = _parse_while_stmt(parser_state)
    
    assert result["type"] == "WHILE_STMT"
    assert result["line"] == 2
    assert result["column"] == 5
    assert len(result["children"]) == 2


def test_error_unexpected_end_of_input():
    """Test error when token stream ends unexpectedly after WHILE."""
    tokens = [
        {"type": "WHILE", "value": "while", "line": 1, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.src"
    }
    
    try:
        _parse_while_stmt(parser_state)
        assert False, "Expected SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e)


def test_error_non_while_token():
    """Test error when current token is not WHILE."""
    tokens = [
        {"type": "IF", "value": "if", "line": 3, "column": 1},
        {"type": "LPAREN", "value": "(", "line": 3, "column": 4},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.src"
    }
    
    try:
        _parse_while_stmt(parser_state)
        assert False, "Expected SyntaxError"
    except SyntaxError as e:
        assert "Expected WHILE token" in str(e)


def test_position_advancement():
    """Test that parser position advances correctly after parsing while statement."""
    tokens = [
        {"type": "WHILE", "value": "while", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 7},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
        {"type": "RBRACE", "value": "}", "line": 1, "column": 13},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.src"
    }
    
    _parse_while_stmt(parser_state)
    
    assert parser_state["pos"] == 4


def test_while_with_body_statements():
    """Test while statement with statements in the body block."""
    tokens = [
        {"type": "WHILE", "value": "while", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 7},
        {"type": "LBRACE", "value": "{", "line": 1, "column": 9},
        {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 2},
        {"type": "ASSIGN", "value": "=", "line": 2, "column": 4},
        {"type": "INTEGER", "value": 1, "line": 2, "column": 6},
        {"type": "SEMICOLON", "value": ";", "line": 2, "column": 7},
        {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.src"
    }
    
    result = _parse_while_stmt(parser_state)
    
    assert result["type"] == "WHILE_STMT"
    assert len(result["children"]) == 2
    
    body = result["children"][1]
    assert body["type"] == "BLOCK"


if __name__ == "__main__":
    test_valid_while_statement()
    print("✓ test_valid_while_statement")
    
    test_while_with_complex_condition()
    print("✓ test_while_with_complex_condition")
    
    test_error_unexpected_end_of_input()
    print("✓ test_error_unexpected_end_of_input")
    
    test_error_non_while_token()
    print("✓ test_error_non_while_token")
    
    test_position_advancement()
    print("✓ test_position_advancement")
    
    test_while_with_body_statements()
    print("✓ test_while_with_body_statements")
    
    print("\nAll integration tests passed!")
