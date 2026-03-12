#!/usr/bin/env python3
"""Integration test for handle_expression_stmt function."""

import sys
import os

package_path = "/Users/loyx/projects/autoapp_workspace/workspace/projects/cc/files/main_package/compile_source_package/generate_code_package/generate_function_code_package/generate_statement_code_package/handle_expression_stmt_package"
sys.path.insert(0, os.path.dirname(package_path))

from handle_expression_stmt_package.handle_expression_stmt_src import handle_expression_stmt


def test_empty_args():
    """Test expression statement with no arguments."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "printf",
        "args": []
    }
    result = handle_expression_stmt(stmt, "main", {})
    assert result == "bl printf", f"Expected 'bl printf', got '{result}'"


def test_single_const_arg():
    """Test expression statement with single constant argument."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "printf",
        "args": [
            {"type": "CONST", "value": 42}
        ]
    }
    result = handle_expression_stmt(stmt, "main", {})
    lines = result.split("\n")
    assert "mov x0, #42" in lines, f"Expected 'mov x0, #42' in {lines}"
    assert "bl printf" in lines, f"Expected 'bl printf' in {lines}"
    assert len(lines) == 2, f"Expected 2 lines, got {len(lines)}"


def test_multiple_args():
    """Test expression statement with multiple arguments."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "add",
        "args": [
            {"type": "CONST", "value": 1},
            {"type": "CONST", "value": 2},
            {"type": "CONST", "value": 3}
        ]
    }
    result = handle_expression_stmt(stmt, "main", {})
    lines = result.split("\n")
    assert "mov x0, #1" in lines, f"Expected 'mov x0, #1' in {lines}"
    assert "mov x1, x0" in lines, f"Expected 'mov x1, x0' in {lines}"
    assert "mov x0, #2" in lines, f"Expected 'mov x0, #2' in {lines}"
    assert "mov x2, x0" in lines, f"Expected 'mov x2, x0' in {lines}"
    assert "mov x0, #3" in lines, f"Expected 'mov x0, #3' in {lines}"
    assert "bl add" in lines, f"Expected 'bl add' in {lines}"


def test_eight_args():
    """Test expression statement with exactly 8 arguments (ARM64 limit)."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "func8",
        "args": [{"type": "CONST", "value": i} for i in range(8)]
    }
    result = handle_expression_stmt(stmt, "main", {})
    lines = result.split("\n")
    # Check that each arg value is loaded into x0
    for i in range(8):
        assert f"mov x0, #{i}" in lines, f"Expected 'mov x0, #{i}' in {lines}"
    # Check that x0 is copied to x1-x7
    for i in range(1, 8):
        assert f"mov x{i}, x0" in lines, f"Expected 'mov x{i}, x0' in {lines}"
    assert "bl func8" in lines, f"Expected 'bl func8' in {lines}"


def test_more_than_eight_args():
    """Test expression statement with more than 8 arguments (should truncate)."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "func9",
        "args": [{"type": "CONST", "value": i} for i in range(10)]
    }
    result = handle_expression_stmt(stmt, "main", {})
    lines = result.split("\n")
    # Check that each arg value (0-7) is loaded into x0
    for i in range(8):
        assert f"mov x0, #{i}" in lines, f"Expected 'mov x0, #{i}' in {lines}"
    # Check that x0 is copied to x1-x7
    for i in range(1, 8):
        assert f"mov x{i}, x0" in lines, f"Expected 'mov x{i}, x0' in {lines}"
    # Check that args 8 and 9 are not present
    for i in range(8, 10):
        assert f"mov x0, #{i}" not in result, f"Unexpected 'mov x0, #{i}' in result"
    assert "bl func9" in lines, f"Expected 'bl func9' in {lines}"


def test_variable_arg():
    """Test expression statement with variable argument."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "print",
        "args": [
            {"type": "VAR", "var_name": "x"}
        ]
    }
    var_offsets = {"x": 0}
    result = handle_expression_stmt(stmt, "main", var_offsets)
    lines = result.split("\n")
    assert "ldr x0, [sp, #0]" in lines, f"Expected 'ldr x0, [sp, #0]' in {lines}"
    assert "bl print" in lines, f"Expected 'bl print' in {lines}"


def test_binop_arg():
    """Test expression statement with binary operation argument."""
    stmt = {
        "type": "EXPRESSION",
        "func_name": "print",
        "args": [
            {
                "type": "BINOP",
                "op": "ADD",
                "left": {"type": "CONST", "value": 1},
                "right": {"type": "CONST", "value": 2}
            }
        ]
    }
    result = handle_expression_stmt(stmt, "main", {})
    lines = result.split("\n")
    assert "mov x0, #1" in lines, f"Expected 'mov x0, #1' in {lines}"
    assert "mov x1, x0" in lines, f"Expected 'mov x1, x0' in {lines}"
    assert "mov x0, #2" in lines, f"Expected 'mov x0, #2' in {lines}"
    assert "add x0, x1, x0" in lines, f"Expected 'add x0, x1, x0' in {lines}"
    assert "bl print" in lines, f"Expected 'bl print' in {lines}"


def test_missing_func_name():
    """Test expression statement with missing func_name."""
    stmt = {
        "type": "EXPRESSION",
        "args": []
    }
    result = handle_expression_stmt(stmt, "main", {})
    assert result == "bl ", f"Expected 'bl ', got '{result}'"


if __name__ == "__main__":
    test_empty_args()
    print("✓ test_empty_args passed")
    
    test_single_const_arg()
    print("✓ test_single_const_arg passed")
    
    test_multiple_args()
    print("✓ test_multiple_args passed")
    
    test_eight_args()
    print("✓ test_eight_args passed")
    
    test_more_than_eight_args()
    print("✓ test_more_than_eight_args passed")
    
    test_variable_arg()
    print("✓ test_variable_arg passed")
    
    test_binop_arg()
    print("✓ test_binop_arg passed")
    
    test_missing_func_name()
    print("✓ test_missing_func_name passed")
    
    print("\nAll integration tests passed!")
