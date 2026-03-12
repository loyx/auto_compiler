#!/usr/bin/env python3
"""
Integration tests for handle_assign function.
Tests the real integration between handle_assign and generate_expression_code.
"""

import sys
import os

# Add the package directory to path
sys.path.insert(0, os.path.dirname(__file__))

from handle_assign_src import handle_assign


def test_assign_const_value():
    """Test assignment with a constant integer value."""
    stmt = {
        "type": "ASSIGN",
        "target": "x",
        "value": {"type": "CONST", "value": 42}
    }
    var_offsets = {"x": 8}
    
    result = handle_assign(stmt, "main", var_offsets)
    
    # Should generate const load + store
    assert "mov x0, #42" in result
    assert "str x0, [sp, #8]" in result


def test_assign_binop_expression():
    """Test assignment with a binary operation expression."""
    stmt = {
        "type": "ASSIGN",
        "target": "y",
        "value": {
            "type": "BINOP",
            "op": "ADD",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
    }
    var_offsets = {"y": 16}
    
    result = handle_assign(stmt, "main", var_offsets)
    
    # Should generate binop code + store
    assert "str x0, [sp, #16]" in result


def test_assign_missing_target_offset():
    """Test assignment when target is not in var_offsets (should default to 0)."""
    stmt = {
        "type": "ASSIGN",
        "target": "unknown_var",
        "value": {"type": "CONST", "value": 100}
    }
    var_offsets = {"x": 8}  # unknown_var not present
    
    result = handle_assign(stmt, "main", var_offsets)
    
    # Should default to offset 0
    assert "str x0, [sp, #0]" in result


def test_assign_zero_offset():
    """Test assignment with zero stack offset."""
    stmt = {
        "type": "ASSIGN",
        "target": "z",
        "value": {"type": "CONST", "value": 0}
    }
    var_offsets = {"z": 0}
    
    result = handle_assign(stmt, "main", var_offsets)
    
    assert "mov x0, #0" in result
    assert "str x0, [sp, #0]" in result


def test_assign_nested_expression():
    """Test assignment with nested binary operations."""
    stmt = {
        "type": "ASSIGN",
        "target": "result",
        "value": {
            "type": "BINOP",
            "op": "MUL",
            "left": {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "CONST", "value": 1},
                "right": {"type": "CONST", "value": 2}
            },
            "right": {"type": "CONST", "value": 3}
        }
    }
    var_offsets = {"result": 24}
    
    result = handle_assign(stmt, "main", var_offsets)
    
    # Should generate nested expression code + store
    assert "str x0, [sp, #24]" in result


def test_assign_large_offset():
    """Test assignment with large stack offset."""
    stmt = {
        "type": "ASSIGN",
        "target": "big_offset_var",
        "value": {"type": "CONST", "value": 999}
    }
    var_offsets = {"big_offset_var": 1024}
    
    result = handle_assign(stmt, "main", var_offsets)
    
    assert "str x0, [sp, #1024]" in result


if __name__ == "__main__":
    test_assign_const_value()
    print("✓ test_assign_const_value passed")
    
    test_assign_binop_expression()
    print("✓ test_assign_binop_expression passed")
    
    test_assign_missing_target_offset()
    print("✓ test_assign_missing_target_offset passed")
    
    test_assign_zero_offset()
    print("✓ test_assign_zero_offset passed")
    
    test_assign_nested_expression()
    print("✓ test_assign_nested_expression passed")
    
    test_assign_large_offset()
    print("✓ test_assign_large_offset passed")
    
    print("\nAll integration tests passed!")
