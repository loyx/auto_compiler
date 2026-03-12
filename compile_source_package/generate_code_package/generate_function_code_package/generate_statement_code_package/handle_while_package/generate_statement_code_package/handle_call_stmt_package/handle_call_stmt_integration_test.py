#!/usr/bin/env python3
"""Integration test for handle_call_stmt function."""

import sys
import os

# Get the directory of this test file and add to path
test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, test_dir)

from handle_call_stmt_src import handle_call_stmt


def test_call_with_no_arguments():
    """Test CALL statement with no arguments - should just generate bl instruction."""
    stmt = {
        "type": "CALL",
        "function": "printf",
        "args": []
    }
    var_offsets = {"x": 0}
    next_offset = 100
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    assert code == "bl printf", f"Expected 'bl printf', got '{code}'"
    assert final_offset == 100, f"Expected offset 100, got {final_offset}"
    print("✓ test_call_with_no_arguments passed")


def test_call_with_single_literal_argument():
    """Test CALL statement with single literal argument."""
    stmt = {
        "type": "CALL",
        "function": "puts",
        "args": [
            {"type": "LITERAL", "value": 42}
        ]
    }
    var_offsets = {}
    next_offset = 200
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    lines = code.split("\n")
    assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {lines}"
    assert "MOV x0, #42" in lines[0], f"Expected MOV instruction, got '{lines[0]}'"
    assert lines[1] == "STORE_OFFSET 192", f"Expected STORE_OFFSET 192, got '{lines[1]}'"
    assert lines[2] == "bl puts", f"Expected 'bl puts', got '{lines[2]}'"
    assert final_offset == 200, f"Expected offset 200, got {final_offset}"
    print("✓ test_call_with_single_literal_argument passed")


def test_call_with_multiple_arguments():
    """Test CALL statement with multiple arguments."""
    stmt = {
        "type": "CALL",
        "function": "add_three",
        "args": [
            {"type": "LITERAL", "value": 1},
            {"type": "LITERAL", "value": 2},
            {"type": "LITERAL", "value": 3}
        ]
    }
    var_offsets = {}
    next_offset = 300
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    lines = code.split("\n")
    # Each arg: MOV + STORE_OFFSET, plus final bl = 3*2 + 1 = 7 lines
    assert len(lines) == 7, f"Expected 7 lines, got {len(lines)}: {lines}"
    assert lines[0] == "MOV x0, #1", f"Expected 'MOV x0, #1', got '{lines[0]}'"
    assert lines[1] == "STORE_OFFSET 292", f"Expected STORE_OFFSET 292, got '{lines[1]}'"
    assert lines[2] == "MOV x0, #2", f"Expected 'MOV x0, #2', got '{lines[2]}'"
    assert lines[3] == "STORE_OFFSET 292", f"Expected STORE_OFFSET 292, got '{lines[3]}'"
    assert lines[4] == "MOV x0, #3", f"Expected 'MOV x0, #3', got '{lines[4]}'"
    assert lines[5] == "STORE_OFFSET 292", f"Expected STORE_OFFSET 292, got '{lines[5]}'"
    assert lines[6] == "bl add_three", f"Expected 'bl add_three', got '{lines[6]}'"
    assert final_offset == 300, f"Expected offset 300, got {final_offset}"
    print("✓ test_call_with_multiple_arguments passed")


def test_call_with_variable_argument():
    """Test CALL statement with variable argument."""
    stmt = {
        "type": "CALL",
        "function": "print_value",
        "args": [
            {"type": "VAR", "name": "counter"}
        ]
    }
    var_offsets = {"counter": 64}
    next_offset = 400
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    lines = code.split("\n")
    assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {lines}"
    assert lines[0] == "LOAD_OFFSET 64", f"Expected 'LOAD_OFFSET 64', got '{lines[0]}'"
    assert lines[1] == "STORE_OFFSET 392", f"Expected STORE_OFFSET 392, got '{lines[1]}'"
    assert lines[2] == "bl print_value", f"Expected 'bl print_value', got '{lines[2]}'"
    assert final_offset == 400, f"Expected offset 400, got {final_offset}"
    print("✓ test_call_with_variable_argument passed")


def test_call_with_binary_expression_argument():
    """Test CALL statement with binary expression argument."""
    stmt = {
        "type": "CALL",
        "function": "process",
        "args": [
            {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "LITERAL", "value": 10},
                "right": {"type": "LITERAL", "value": 5}
            }
        ]
    }
    var_offsets = {}
    next_offset = 500
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    lines = code.split("\n")
    # BINOP generates: MOV, STORE_OFFSET, MOV, LOAD_OFFSET, ADD, plus CALL STORE_OFFSET and bl
    assert len(lines) >= 7, f"Expected at least 7 lines, got {len(lines)}: {lines}"
    assert "MOV x0, #10" in lines[0], f"Expected MOV for left operand, got '{lines[0]}'"
    assert "ADD" in code, f"Expected ADD instruction in code, got '{code}'"
    assert "bl process" in lines[-1], f"Expected 'bl process' at end, got '{lines[-1]}'"
    print("✓ test_call_with_binary_expression_argument passed")


def test_call_with_empty_function_name():
    """Test CALL statement with empty function name - should return empty code."""
    stmt = {
        "type": "CALL",
        "function": "",
        "args": [{"type": "LITERAL", "value": 1}]
    }
    var_offsets = {}
    next_offset = 600
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    assert code == "", f"Expected empty code, got '{code}'"
    assert final_offset == 600, f"Expected offset 600, got {final_offset}"
    print("✓ test_call_with_empty_function_name passed")


def test_call_with_missing_function_key():
    """Test CALL statement with missing function key - should return empty code."""
    stmt = {
        "type": "CALL",
        "args": [{"type": "LITERAL", "value": 1}]
    }
    var_offsets = {}
    next_offset = 700
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    assert code == "", f"Expected empty code, got '{code}'"
    assert final_offset == 700, f"Expected offset 700, got {final_offset}"
    print("✓ test_call_with_missing_function_key passed")


def test_call_offset_propagation():
    """Test that offsets are properly propagated through argument generation."""
    stmt = {
        "type": "CALL",
        "function": "test_func",
        "args": [
            {"type": "LITERAL", "value": 1},
            {"type": "LITERAL", "value": 2}
        ]
    }
    var_offsets = {}
    next_offset = 800
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    # Each literal takes 8 bytes (one instruction slot)
    # After 2 args, offset should still be 800 (generate_expression_code returns same offset for literals)
    assert final_offset == 800, f"Expected offset 800, got {final_offset}"
    print("✓ test_call_offset_propagation passed")


def test_call_mixed_argument_types():
    """Test CALL statement with mixed argument types."""
    stmt = {
        "type": "CALL",
        "function": "mixed_call",
        "args": [
            {"type": "LITERAL", "value": 100},
            {"type": "VAR", "name": "x"},
            {"type": "LITERAL", "value": 200}
        ]
    }
    var_offsets = {"x": 128}
    next_offset = 900
    
    code, final_offset = handle_call_stmt(stmt, var_offsets, next_offset)
    
    lines = code.split("\n")
    assert len(lines) == 7, f"Expected 7 lines, got {len(lines)}: {lines}"
    assert lines[0] == "MOV x0, #100", f"Expected 'MOV x0, #100', got '{lines[0]}'"
    assert lines[2] == "LOAD_OFFSET 128", f"Expected 'LOAD_OFFSET 128', got '{lines[2]}'"
    assert lines[4] == "MOV x0, #200", f"Expected 'MOV x0, #200', got '{lines[4]}'"
    assert lines[6] == "bl mixed_call", f"Expected 'bl mixed_call', got '{lines[6]}'"
    print("✓ test_call_mixed_argument_types passed")


if __name__ == "__main__":
    print("Running integration tests for handle_call_stmt...\n")
    
    test_call_with_no_arguments()
    test_call_with_single_literal_argument()
    test_call_with_multiple_arguments()
    test_call_with_variable_argument()
    test_call_with_binary_expression_argument()
    test_call_with_empty_function_name()
    test_call_with_missing_function_key()
    test_call_offset_propagation()
    test_call_mixed_argument_types()
    
    print("\n✓ All integration tests passed!")
