#!/usr/bin/env python3
"""Integration tests for handle_for function."""

import sys

# Add project root to path
project_root = "/Users/loyx/projects/autoapp_workspace/workspace/projects/cc/files"
sys.path.insert(0, project_root)

from main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.handle_for_src import handle_for


def test_complete_for_loop():
    """Test complete FOR loop with all components."""
    label_counter = {}
    var_offsets = {}
    next_offset = 0
    
    stmt = {
        "type": "FOR",
        "init": {
            "type": "ASSIGN",
            "target": {"type": "IDENTIFIER", "name": "i"},
            "value": {"type": "LITERAL", "value": 0}
        },
        "condition": {
            "type": "BINARY_OP",
            "operator": "<",
            "left": {"type": "IDENTIFIER", "name": "i"},
            "right": {"type": "LITERAL", "value": 10}
        },
        "update": {
            "type": "ASSIGN",
            "target": {"type": "IDENTIFIER", "name": "i"},
            "value": {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "IDENTIFIER", "name": "i"},
                "right": {"type": "LITERAL", "value": 1}
            }
        },
        "body": [
            {
                "type": "ASSIGN",
                "target": {"type": "IDENTIFIER", "name": "sum"},
                "value": {
                    "type": "BINARY_OP",
                    "operator": "+",
                    "left": {"type": "IDENTIFIER", "name": "sum"},
                    "right": {"type": "IDENTIFIER", "name": "i"}
                }
            }
        ]
    }
    
    code, next_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # Verify code structure
    assert "test_func_for_cond_0:" in code
    assert "test_func_for_update_0:" in code
    assert "test_func_for_end_0:" in code
    assert "b test_func_for_cond_0" in code
    assert "cbz x0, test_func_for_end_0" in code
    
    # Verify label_counter was updated
    assert label_counter["for_cond"] == 1
    assert label_counter["for_end"] == 1
    assert label_counter["for_update"] == 1
    
    print("✓ test_complete_for_loop passed")


def test_for_without_init():
    """Test FOR loop without init statement."""
    label_counter = {}
    var_offsets = {}
    next_offset = 0
    
    stmt = {
        "type": "FOR",
        "init": None,
        "condition": {
            "type": "BINARY_OP",
            "operator": "<",
            "left": {"type": "IDENTIFIER", "name": "i"},
            "right": {"type": "LITERAL", "value": 10}
        },
        "update": {
            "type": "ASSIGN",
            "target": {"type": "IDENTIFIER", "name": "i"},
            "value": {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "IDENTIFIER", "name": "i"},
                "right": {"type": "LITERAL", "value": 1}
            }
        },
        "body": []
    }
    
    code, next_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # Verify code structure
    assert "test_func_for_cond_0:" in code
    assert "test_func_for_update_0:" in code
    assert "test_func_for_end_0:" in code
    assert "cbz x0, test_func_for_end_0" in code
    
    print("✓ test_for_without_init passed")


def test_for_without_condition():
    """Test FOR loop without condition (infinite loop)."""
    label_counter = {}
    var_offsets = {}
    next_offset = 0
    
    stmt = {
        "type": "FOR",
        "init": None,
        "condition": None,
        "update": None,
        "body": []
    }
    
    code, next_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # Verify code structure - should still have labels but no condition check
    assert "test_func_for_cond_0:" in code
    assert "test_func_for_end_0:" in code
    
    # Should NOT have cbz instruction since no condition
    assert "cbz x0" not in code
    
    print("✓ test_for_without_condition passed")


def test_for_without_update():
    """Test FOR loop without update statement."""
    label_counter = {}
    var_offsets = {}
    next_offset = 0
    
    stmt = {
        "type": "FOR",
        "init": None,
        "condition": {
            "type": "BINARY_OP",
            "operator": "<",
            "left": {"type": "IDENTIFIER", "name": "i"},
            "right": {"type": "LITERAL", "value": 10}
        },
        "update": None,
        "body": []
    }
    
    code, next_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # Verify code structure
    assert "test_func_for_cond_0:" in code
    assert "test_func_for_update_0:" in code
    assert "test_func_for_end_0:" in code
    
    print("✓ test_for_without_update passed")


def test_for_empty_body():
    """Test FOR loop with empty body."""
    label_counter = {}
    var_offsets = {}
    next_offset = 0
    
    stmt = {
        "type": "FOR",
        "init": None,
        "condition": {
            "type": "BINARY_OP",
            "operator": "<",
            "left": {"type": "IDENTIFIER", "name": "i"},
            "right": {"type": "LITERAL", "value": 10}
        },
        "update": None,
        "body": []
    }
    
    code, next_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # Verify code structure
    assert "test_func_for_cond_0:" in code
    assert "test_func_for_end_0:" in code
    assert "b test_func_for_cond_0" in code
    
    print("✓ test_for_empty_body passed")


def test_label_counter_increment():
    """Test that label_counter is properly incremented."""
    label_counter = {
        "for_cond": 5,
        "for_end": 3,
        "for_update": 2
    }
    var_offsets = {}
    next_offset = 0
    
    stmt = {
        "type": "FOR",
        "init": None,
        "condition": None,
        "update": None,
        "body": []
    }
    
    code, next_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # Verify labels use the old counts
    assert "test_func_for_cond_5:" in code
    assert "test_func_for_end_3:" in code
    assert "test_func_for_update_2:" in code
    
    # Verify label_counter was incremented
    assert label_counter["for_cond"] == 6
    assert label_counter["for_end"] == 4
    assert label_counter["for_update"] == 3
    
    print("✓ test_label_counter_increment passed")


def test_next_offset_propagation():
    """Test that next_offset is properly propagated through nested calls."""
    label_counter = {}
    var_offsets = {}
    next_offset = 100  # Start with non-zero offset
    
    stmt = {
        "type": "FOR",
        "init": None,
        "condition": None,
        "update": None,
        "body": []
    }
    
    code, final_offset = handle_for(stmt, "test_func", label_counter, var_offsets, next_offset)
    
    # next_offset should be returned (may change if body has allocations)
    assert final_offset >= 100
    
    print("✓ test_next_offset_propagation passed")


def test_multiple_for_loops():
    """Test multiple FOR loops to verify label uniqueness."""
    label_counter = {}
    var_offsets = {}
    next_offset = 0
    
    stmt1 = {
        "type": "FOR",
        "init": None,
        "condition": None,
        "update": None,
        "body": []
    }
    
    stmt2 = {
        "type": "FOR",
        "init": None,
        "condition": None,
        "update": None,
        "body": []
    }
    
    code1, next_offset = handle_for(stmt1, "test_func", label_counter, var_offsets, next_offset)
    code2, next_offset = handle_for(stmt2, "test_func", label_counter, var_offsets, next_offset)
    
    # First loop should use _0 labels
    assert "test_func_for_cond_0:" in code1
    assert "test_func_for_end_0:" in code1
    
    # Second loop should use _1 labels
    assert "test_func_for_cond_1:" in code2
    assert "test_func_for_end_1:" in code2
    
    # Verify no overlap
    assert "test_func_for_cond_1:" not in code1
    assert "test_func_for_cond_0:" not in code2
    
    print("✓ test_multiple_for_loops passed")


if __name__ == "__main__":
    test_complete_for_loop()
    test_for_without_init()
    test_for_without_condition()
    test_for_without_update()
    test_for_empty_body()
    test_label_counter_increment()
    test_next_offset_propagation()
    test_multiple_for_loops()
    print("\n✅ All integration tests passed!")
