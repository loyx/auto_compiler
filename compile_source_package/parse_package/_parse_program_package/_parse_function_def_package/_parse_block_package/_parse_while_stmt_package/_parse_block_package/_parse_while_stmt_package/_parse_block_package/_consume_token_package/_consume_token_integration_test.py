#!/usr/bin/env python3
"""
Integration test for _consume_token function.
Tests the function through real module boundaries with minimal mocking.
"""

import sys
import os

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..', '..', '..', '..', '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

from main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src import _consume_token


def test_consume_token_without_expected_type():
    """Test consuming token without specifying expected type."""
    parser_state = {
        "tokens": [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
        ],
        "pos": 0,
        "filename": "test.py"
    }
    
    new_state = _consume_token(parser_state)
    
    assert new_state["pos"] == 1
    assert new_state["filename"] == "test.py"
    assert parser_state["pos"] == 0  # Original unchanged


def test_consume_token_with_matching_expected_type():
    """Test consuming token with matching expected type."""
    parser_state = {
        "tokens": [
            {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
        ],
        "pos": 0,
        "filename": "test.py"
    }
    
    new_state = _consume_token(parser_state, expected_type="KEYWORD")
    
    assert new_state["pos"] == 1


def test_consume_token_with_mismatched_type_raises_error():
    """Test that mismatched expected type raises SyntaxError."""
    parser_state = {
        "tokens": [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ],
        "pos": 0,
        "filename": "test.py"
    }
    
    try:
        _consume_token(parser_state, expected_type="KEYWORD")
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Expected token type 'KEYWORD'" in str(e)
        assert "got 'IDENTIFIER'" in str(e)


def test_consume_token_at_eof_without_expected_type():
    """Test consuming token at EOF without expected type."""
    parser_state = {
        "tokens": [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ],
        "pos": 1,  # Already at EOF
        "filename": "test.py"
    }
    
    new_state = _consume_token(parser_state)
    
    assert new_state["pos"] == 1  # pos unchanged at EOF
    assert new_state["filename"] == "test.py"


def test_consume_token_at_eof_with_expected_type_raises_error():
    """Test that consuming at EOF with expected type raises SyntaxError."""
    parser_state = {
        "tokens": [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ],
        "pos": 1,  # Already at EOF
        "filename": "test.py"
    }
    
    try:
        _consume_token(parser_state, expected_type="IDENTIFIER")
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e)
        assert "expected 'IDENTIFIER'" in str(e)


def test_consume_token_from_non_zero_position():
    """Test consuming token from a non-zero position."""
    parser_state = {
        "tokens": [
            {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "cond", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 12},
        ],
        "pos": 1,  # Start at second token
        "filename": "test.py"
    }
    
    new_state = _consume_token(parser_state, expected_type="LPAREN")
    
    assert new_state["pos"] == 2


def test_consume_token_preserves_original_state():
    """Test that original parser_state is not modified."""
    parser_state = {
        "tokens": [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ],
        "pos": 0,
        "filename": "test.py"
    }
    
    new_state = _consume_token(parser_state)
    
    assert parser_state["pos"] == 0
    assert new_state["pos"] == 1
    assert parser_state is not new_state


def test_consume_token_empty_tokens_list():
    """Test consuming token from empty tokens list (EOF immediately)."""
    parser_state = {
        "tokens": [],
        "pos": 0,
        "filename": "test.py"
    }
    
    new_state = _consume_token(parser_state)
    
    assert new_state["pos"] == 0


def test_consume_token_empty_tokens_with_expected_type_raises_error():
    """Test that empty tokens list with expected type raises SyntaxError."""
    parser_state = {
        "tokens": [],
        "pos": 0,
        "filename": "test.py"
    }
    
    try:
        _consume_token(parser_state, expected_type="IDENTIFIER")
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e)


def test_consume_token_multiple_sequential_calls():
    """Test multiple sequential consume calls."""
    parser_state = {
        "tokens": [
            {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
        ],
        "pos": 0,
        "filename": "test.py"
    }
    
    state1 = _consume_token(parser_state, expected_type="KEYWORD")
    assert state1["pos"] == 1
    
    state2 = _consume_token(state1, expected_type="LPAREN")
    assert state2["pos"] == 2
    
    state3 = _consume_token(state2, expected_type="IDENTIFIER")
    assert state3["pos"] == 3


if __name__ == "__main__":
    test_consume_token_without_expected_type()
    print("✓ test_consume_token_without_expected_type passed")
    
    test_consume_token_with_matching_expected_type()
    print("✓ test_consume_token_with_matching_expected_type passed")
    
    test_consume_token_with_mismatched_type_raises_error()
    print("✓ test_consume_token_with_mismatched_type_raises_error passed")
    
    test_consume_token_at_eof_without_expected_type()
    print("✓ test_consume_token_at_eof_without_expected_type passed")
    
    test_consume_token_at_eof_with_expected_type_raises_error()
    print("✓ test_consume_token_at_eof_with_expected_type_raises_error passed")
    
    test_consume_token_from_non_zero_position()
    print("✓ test_consume_token_from_non_zero_position passed")
    
    test_consume_token_preserves_original_state()
    print("✓ test_consume_token_preserves_original_state passed")
    
    test_consume_token_empty_tokens_list()
    print("✓ test_consume_token_empty_tokens_list passed")
    
    test_consume_token_empty_tokens_with_expected_type_raises_error()
    print("✓ test_consume_token_empty_tokens_with_expected_type_raises_error passed")
    
    test_consume_token_multiple_sequential_calls()
    print("✓ test_consume_token_multiple_sequential_calls passed")
    
    print("\nAll integration tests passed!")
