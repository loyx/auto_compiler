#!/usr/bin/env python3
"""
Integration test for _parse_comparison_expr function.
Tests the function through real call chains with minimal mocking.
"""

import sys
import os

# Add the project root to path for module resolution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..', '..', '..', '..'))

from main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr


def create_parser_state(tokens, pos=0, filename="test.py"):
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def create_token(token_type, value, line=1, column=1):
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def test_comparison_less():
    """Test parsing 'a < b' expression."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("LESS", "<", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP", f"Expected BINARY_OP, got {result['type']}"
    assert result["value"] == "<", f"Expected '<', got {result['value']}"
    assert len(result["children"]) == 2, f"Expected 2 children, got {len(result['children'])}"
    assert result["line"] == 1, f"Expected line 1, got {result['line']}"
    assert result["column"] == 3, f"Expected column 3, got {result['column']}"
    assert parser_state["pos"] == 3, f"Expected pos 3 after parsing, got {parser_state['pos']}"
    print("✓ test_comparison_less passed")


def test_comparison_greater():
    """Test parsing 'a > b' expression."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("GREATER", ">", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == ">"
    assert len(result["children"]) == 2
    assert result["line"] == 1
    assert result["column"] == 3
    print("✓ test_comparison_greater passed")


def test_comparison_less_eq():
    """Test parsing 'a <= b' expression."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("LESS_EQ", "<=", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == "<="
    assert len(result["children"]) == 2
    print("✓ test_comparison_less_eq passed")


def test_comparison_greater_eq():
    """Test parsing 'a >= b' expression."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("GREATER_EQ", ">=", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == ">="
    assert len(result["children"]) == 2
    print("✓ test_comparison_greater_eq passed")


def test_comparison_eq():
    """Test parsing 'a == b' expression."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("EQ", "==", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == "=="
    assert len(result["children"]) == 2
    print("✓ test_comparison_eq passed")


def test_comparison_neq():
    """Test parsing 'a != b' expression."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("NEQ", "!=", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == "!="
    assert len(result["children"]) == 2
    print("✓ test_comparison_neq passed")


def test_no_comparison_operator():
    """Test parsing expression without comparison operator (should return left operand)."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("PLUS", "+", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    # Should return the result from _parse_additive_expr (not a BINARY_OP for comparison)
    # The pos should not advance past the first token if it's not a comparison op
    assert result["type"] != "BINARY_OP" or result["value"] not in ["<", ">", "<=", ">=", "==", "!="]
    print("✓ test_no_comparison_operator passed")


def test_single_operand():
    """Test parsing single operand without any operator."""
    tokens = [
        create_token("IDENTIFIER", "x", 1, 1)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    # Should return the identifier AST
    assert result is not None
    assert parser_state["pos"] == 1, f"Expected pos 1, got {parser_state['pos']}"
    print("✓ test_single_operand passed")


def test_empty_tokens():
    """Test parsing with empty token list."""
    parser_state = create_parser_state([], pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    # Should handle gracefully (return from _parse_additive_expr)
    assert result is not None
    print("✓ test_empty_tokens passed")


def test_comparison_with_literal():
    """Test parsing '5 < 10' with literals."""
    tokens = [
        create_token("LITERAL", "5", 1, 1),
        create_token("LESS", "<", 1, 3),
        create_token("LITERAL", "10", 1, 5)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == "<"
    assert len(result["children"]) == 2
    print("✓ test_comparison_with_literal passed")


def test_position_at_end():
    """Test when pos is already at end of tokens."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1)
    ]
    parser_state = create_parser_state(tokens, pos=1)  # pos at end
    
    result = _parse_comparison_expr(parser_state)
    
    # Should return left operand without error
    assert result is not None
    print("✓ test_position_at_end passed")


def test_comparison_chain_stops_at_first():
    """Test that only one comparison operator is consumed (not left-associative)."""
    tokens = [
        create_token("IDENTIFIER", "a", 1, 1),
        create_token("LESS", "<", 1, 3),
        create_token("IDENTIFIER", "b", 1, 5),
        create_token("LESS", "<", 1, 7),
        create_token("IDENTIFIER", "c", 1, 9)
    ]
    parser_state = create_parser_state(tokens, pos=0)
    
    result = _parse_comparison_expr(parser_state)
    
    assert result["type"] == "BINARY_OP"
    assert result["value"] == "<"
    # Should have consumed only up to 'b', pos should be 3 (after parsing a < b)
    assert parser_state["pos"] == 3, f"Expected pos 3, got {parser_state['pos']}"
    print("✓ test_comparison_chain_stops_at_first passed")


if __name__ == "__main__":
    print("Running integration tests for _parse_comparison_expr...")
    print("=" * 60)
    
    test_comparison_less()
    test_comparison_greater()
    test_comparison_less_eq()
    test_comparison_greater_eq()
    test_comparison_eq()
    test_comparison_neq()
    test_no_comparison_operator()
    test_single_operand()
    test_empty_tokens()
    test_comparison_with_literal()
    test_position_at_end()
    test_comparison_chain_stops_at_first()
    
    print("=" * 60)
    print("All integration tests passed! ✓")
