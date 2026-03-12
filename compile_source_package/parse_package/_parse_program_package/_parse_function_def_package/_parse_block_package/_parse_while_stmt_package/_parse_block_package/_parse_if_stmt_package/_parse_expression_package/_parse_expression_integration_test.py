#!/usr/bin/env python3
"""
Integration test for _parse_expression function.
Tests the function through real module boundaries with actual token sequences.
"""

import sys
import os

# Add the package directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _parse_expression_src import _parse_expression


def test_parse_literal():
    """Test parsing a simple literal value."""
    tokens = [
        {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc"
    }
    
    result = _parse_expression(parser_state)
    
    assert result["type"] == "LITERAL", f"Expected LITERAL, got {result['type']}"
    assert result["value"] == "42"
    assert parser_state["pos"] == 1, "Position should advance after parsing"


def test_parse_identifier():
    """Test parsing a simple identifier."""
    tokens = [
        {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc"
    }
    
    result = _parse_expression(parser_state)
    
    assert result["type"] == "IDENTIFIER", f"Expected IDENTIFIER, got {result['type']}"
    assert result["value"] == "x"
    assert parser_state["pos"] == 1


def test_parse_unary_expression():
    """Test parsing a unary expression."""
    tokens = [
        {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
        {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc"
    }
    
    result = _parse_expression(parser_state)
    
    assert result["type"] == "UNARY_OP", f"Expected UNARY_OP, got {result['type']}"
    assert result["children"][0]["type"] == "LITERAL"
    assert result["children"][0]["value"] == "5"
    assert parser_state["pos"] == 2


def test_parse_binary_expression():
    """Test parsing a binary expression."""
    tokens = [
        {"type": "NUMBER", "value": "3", "line": 1, "column": 1},
        {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
        {"type": "NUMBER", "value": "4", "line": 1, "column": 3}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc"
    }
    
    result = _parse_expression(parser_state)
    
    assert result["type"] == "BINARY_OP", f"Expected BINARY_OP, got {result['type']}"
    assert result["value"] == "+"
    assert len(result["children"]) == 2
    assert parser_state["pos"] == 3


def test_parse_complex_expression():
    """Test parsing a complex expression with multiple operators."""
    tokens = [
        {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
        {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
        {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
        {"type": "OPERATOR", "value": "*", "line": 1, "column": 4},
        {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc"
    }
    
    result = _parse_expression(parser_state)
    
    # Should parse the full expression
    assert result is not None
    assert parser_state["pos"] == 5


def test_empty_input_raises_syntax_error():
    """Test that empty input raises SyntaxError."""
    tokens = []
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.cc"
    }
    
    try:
        _parse_expression(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e)


def test_position_at_end_raises_syntax_error():
    """Test that position at end of tokens raises SyntaxError."""
    tokens = [
        {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 1,  # Already at end
        "filename": "test.cc"
    }
    
    try:
        _parse_expression(parser_state)
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e)


def test_parse_from_middle_position():
    """Test parsing expression starting from middle position."""
    tokens = [
        {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
        {"type": "NUMBER", "value": "10", "line": 1, "column": 2},
        {"type": "OPERATOR", "value": ">", "line": 1, "column": 3},
        {"type": "NUMBER", "value": "5", "line": 1, "column": 4}
    ]
    parser_state = {
        "tokens": tokens,
        "pos": 1,  # Start from the number
        "filename": "test.cc"
    }
    
    result = _parse_expression(parser_state)
    
    assert result is not None
    assert parser_state["pos"] > 1, "Position should advance from starting point"


if __name__ == "__main__":
    test_parse_literal()
    print("✓ test_parse_literal passed")
    
    test_parse_identifier()
    print("✓ test_parse_identifier passed")
    
    test_parse_unary_expression()
    print("✓ test_parse_unary_expression passed")
    
    test_parse_binary_expression()
    print("✓ test_parse_binary_expression passed")
    
    test_parse_complex_expression()
    print("✓ test_parse_complex_expression passed")
    
    test_empty_input_raises_syntax_error()
    print("✓ test_empty_input_raises_syntax_error passed")
    
    test_position_at_end_raises_syntax_error()
    print("✓ test_position_at_end_raises_syntax_error passed")
    
    test_parse_from_middle_position()
    print("✓ test_parse_from_middle_position passed")
    
    print("\nAll integration tests passed!")
