#!/usr/bin/env python3
"""
Integration test for generate_expression_code function.
Tests the function through its real module boundary with minimal mocking.
"""

import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_expression_code_src import generate_expression_code


def test_const_expression():
    """Test CONST expression type - loads integer constant into x0."""
    expr = {"type": "CONST", "value": 42}
    result = generate_expression_code(expr, "test_func", {})
    
    assert "mov x0, #42" in result
    print("✓ CONST expression test passed")


def test_negative_const_expression():
    """Test CONST expression with negative value."""
    expr = {"type": "CONST", "value": -10}
    result = generate_expression_code(expr, "test_func", {})
    
    assert "mov x0, #-10" in result or "movn" in result.lower()
    print("✓ Negative CONST expression test passed")


def test_var_expression():
    """Test VAR expression type - loads variable from stack into x0."""
    var_offsets = {"x": 16, "y": 24}
    expr = {"type": "VAR", "name": "x"}
    result = generate_expression_code(expr, "test_func", var_offsets)
    
    assert "ldr x0, [sp, #16]" in result
    print("✓ VAR expression test passed")


def test_var_expression_not_found():
    """Test VAR expression with undefined variable raises KeyError."""
    var_offsets = {"x": 16}
    expr = {"type": "VAR", "name": "undefined_var"}
    
    try:
        generate_expression_code(expr, "test_func", var_offsets)
        assert False, "Should have raised KeyError"
    except KeyError:
        print("✓ VAR expression not found test passed")


def test_binop_add_expression():
    """Test BINOP expression with addition operator."""
    var_offsets = {"a": 16, "b": 24}
    expr = {
        "type": "BINOP",
        "op": "+",
        "left": {"type": "VAR", "name": "a"},
        "right": {"type": "VAR", "name": "b"}
    }
    result = generate_expression_code(expr, "test_func", var_offsets)
    
    assert "ldr x0, [sp, #16]" in result  # Load a
    assert "ldr x9, [sp, #24]" in result or "x9" in result  # Save in x9
    assert "add x0, x9, x0" in result or "add x0, x0, x9" in result
    print("✓ BINOP addition test passed")


def test_binop_nested_expression():
    """Test BINOP expression with nested operations: (a + b) * c."""
    var_offsets = {"a": 16, "b": 24, "c": 32}
    expr = {
        "type": "BINOP",
        "op": "*",
        "left": {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "VAR", "name": "b"}
        },
        "right": {"type": "VAR", "name": "c"}
    }
    result = generate_expression_code(expr, "test_func", var_offsets)
    
    # Should contain loads for all three variables
    assert "ldr x0, [sp, #16]" in result  # a
    assert "ldr" in result  # At least one load
    assert "mul x0," in result or "mul x0, x" in result
    print("✓ BINOP nested expression test passed")


def test_binop_comparison_expression():
    """Test BINOP expression with comparison operator."""
    var_offsets = {"x": 16, "y": 24}
    expr = {
        "type": "BINOP",
        "op": "==",
        "left": {"type": "VAR", "name": "x"},
        "right": {"type": "VAR", "name": "y"}
    }
    result = generate_expression_code(expr, "test_func", var_offsets)
    
    assert "cmp" in result.lower() or "cset" in result.lower()
    print("✓ BINOP comparison test passed")


def test_call_expression():
    """Test CALL expression type - function call with arguments."""
    var_offsets = {"arg1": 16}
    expr = {
        "type": "CALL",
        "name": "foo",
        "args": [
            {"type": "CONST", "value": 1},
            {"type": "VAR", "name": "arg1"}
        ]
    }
    result = generate_expression_code(expr, "test_func", var_offsets)
    
    assert "bl foo" in result
    assert "mov x0, #1" in result  # First arg
    print("✓ CALL expression test passed")


def test_call_expression_no_args():
    """Test CALL expression with no arguments."""
    expr = {
        "type": "CALL",
        "name": "bar",
        "args": []
    }
    result = generate_expression_code(expr, "test_func", {})
    
    assert "bl bar" in result
    print("✓ CALL expression no args test passed")


def test_unsupported_expression_type():
    """Test that unsupported expression type raises ValueError."""
    expr = {"type": "UNKNOWN", "data": "something"}
    
    try:
        generate_expression_code(expr, "test_func", {})
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unsupported expression type" in str(e)
        print("✓ Unsupported expression type test passed")


def test_complex_expression():
    """Test complex expression: foo(a + 5) == bar()."""
    var_offsets = {"a": 16}
    expr = {
        "type": "BINOP",
        "op": "==",
        "left": {
            "type": "CALL",
            "name": "foo",
            "args": [
                {
                    "type": "BINOP",
                    "op": "+",
                    "left": {"type": "VAR", "name": "a"},
                    "right": {"type": "CONST", "value": 5}
                }
            ]
        },
        "right": {
            "type": "CALL",
            "name": "bar",
            "args": []
        }
    }
    result = generate_expression_code(expr, "test_func", var_offsets)
    
    assert "bl foo" in result
    assert "bl bar" in result
    assert "cmp" in result.lower() or "cset" in result.lower()
    print("✓ Complex expression test passed")


def test_const_zero():
    """Test CONST expression with zero value."""
    expr = {"type": "CONST", "value": 0}
    result = generate_expression_code(expr, "test_func", {})
    
    assert "mov x0, #0" in result or "x0, #0" in result
    print("✓ CONST zero test passed")


def test_binop_with_const_operands():
    """Test BINOP with constant operands: 10 + 20."""
    expr = {
        "type": "BINOP",
        "op": "+",
        "left": {"type": "CONST", "value": 10},
        "right": {"type": "CONST", "value": 20}
    }
    result = generate_expression_code(expr, "test_func", {})
    
    assert "mov x0, #10" in result
    assert "mov" in result  # At least one mov for constants
    assert "add" in result
    print("✓ BINOP with const operands test passed")


if __name__ == "__main__":
    print("Running integration tests for generate_expression_code...\n")
    
    test_const_expression()
    test_negative_const_expression()
    test_var_expression()
    test_var_expression_not_found()
    test_binop_add_expression()
    test_binop_nested_expression()
    test_binop_comparison_expression()
    test_call_expression()
    test_call_expression_no_args()
    test_unsupported_expression_type()
    test_complex_expression()
    test_const_zero()
    test_binop_with_const_operands()
    
    print("\n" + "="*60)
    print("All integration tests passed!")
    print("="*60)
