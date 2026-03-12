#!/usr/bin/env python3
"""
Integration test for handle_assign_stmt function.
Tests the real integration between handle_assign_stmt and generate_expression_code.
"""

import sys
import os

# Add the package path for imports
package_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, package_dir)

from handle_assign_stmt_package.handle_assign_stmt_src import handle_assign_stmt


def test_assign_new_variable():
    """Test assigning to a new variable - integration with generate_expression_code"""
    var_offsets = {}
    stmt = {
        "type": "ASSIGN",
        "target": "x",
        "value": {"type": "CONST", "value": 42}
    }
    next_offset = 0
    
    code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)
    
    # Verify var_offsets was modified in-place
    assert "x" in var_offsets, "New variable should be added to var_offsets"
    assert var_offsets["x"] == 0, "First variable should get offset 0"
    
    # Verify code generation
    assert "STORE_OFFSET 0" in code, "Should store to offset 0"
    assert new_offset == 8, "Next offset should be 8 after one allocation"
    
    print("✓ test_assign_new_variable passed")


def test_assign_existing_variable():
    """Test assigning to an existing variable"""
    var_offsets = {"y": 16}
    stmt = {
        "type": "ASSIGN",
        "target": "y",
        "value": {"type": "CONST", "value": 100}
    }
    next_offset = 24
    
    code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)
    
    # Verify var_offsets unchanged for existing variable
    assert var_offsets["y"] == 16, "Existing variable offset should not change"
    
    # Verify code generation uses existing offset
    assert "STORE_OFFSET 16" in code, "Should store to existing offset 16"
    # next_offset should not change since no new allocation
    assert new_offset == 24, "Next offset should remain unchanged"
    
    print("✓ test_assign_existing_variable passed")


def test_multiple_assignments():
    """Test multiple sequential assignments - integration test"""
    var_offsets = {}
    next_offset = 0
    
    # First assignment
    stmt1 = {
        "type": "ASSIGN",
        "target": "a",
        "value": {"type": "CONST", "value": 1}
    }
    code1, next_offset = handle_assign_stmt(stmt1, var_offsets, next_offset)
    
    # Second assignment
    stmt2 = {
        "type": "ASSIGN",
        "target": "b",
        "value": {"type": "CONST", "value": 2}
    }
    code2, next_offset = handle_assign_stmt(stmt2, var_offsets, next_offset)
    
    # Verify both variables allocated
    assert var_offsets["a"] == 0, "First variable should get offset 0"
    assert var_offsets["b"] == 8, "Second variable should get offset 8"
    assert next_offset == 16, "Next offset should be 16 after two allocations"
    
    # Verify code
    assert "STORE_OFFSET 0" in code1, "First assignment should store to 0"
    assert "STORE_OFFSET 8" in code2, "Second assignment should store to 8"
    
    print("✓ test_multiple_assignments passed")


def test_assign_with_var_expression():
    """Test assignment with variable reference expression"""
    var_offsets = {"src": 0}
    stmt = {
        "type": "ASSIGN",
        "target": "dest",
        "value": {"type": "VAR", "name": "src"}
    }
    next_offset = 8
    
    code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)
    
    # Verify new variable allocated
    assert "dest" in var_offsets, "New variable should be added"
    assert var_offsets["dest"] == 8, "New variable should get next available offset"
    
    # Verify code contains LOAD for source and STORE for dest
    assert "LOAD_OFFSET 0" in code, "Should load from src offset"
    assert "STORE_OFFSET 8" in code, "Should store to dest offset"
    assert new_offset == 16, "Next offset should increment by 8"
    
    print("✓ test_assign_with_var_expression passed")


def test_assign_non_zero_start_offset():
    """Test assignment starting from non-zero offset"""
    var_offsets = {}
    stmt = {
        "type": "ASSIGN",
        "target": "z",
        "value": {"type": "CONST", "value": 999}
    }
    next_offset = 64
    
    code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)
    
    assert var_offsets["z"] == 64, "Variable should get offset 64"
    assert "STORE_OFFSET 64" in code, "Should store to offset 64"
    assert new_offset == 72, "Next offset should be 72"
    
    print("✓ test_assign_non_zero_start_offset passed")


if __name__ == "__main__":
    test_assign_new_variable()
    test_assign_existing_variable()
    test_multiple_assignments()
    test_assign_with_var_expression()
    test_assign_non_zero_start_offset()
    print("\n✅ All integration tests passed!")
