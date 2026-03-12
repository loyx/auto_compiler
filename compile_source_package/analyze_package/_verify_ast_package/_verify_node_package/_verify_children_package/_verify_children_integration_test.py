#!/usr/bin/env python3
"""
Integration test for _verify_children function.
Tests the real module boundary behavior with minimal mocking.
"""

import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_children_src import _verify_children


def test_empty_children_list():
    """Test that empty children list returns without error."""
    node = {
        "type": "block",
        "children": [],
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {},
        "functions": {},
        "current_scope": 0
    }
    context_stack = []
    filename = "test.py"
    
    # Should not raise any exception
    _verify_children(node, symbol_table, context_stack, filename)
    print("✓ test_empty_children_list passed")


def test_missing_children_key():
    """Test that missing children key returns without error."""
    node = {
        "type": "block",
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {},
        "functions": {},
        "current_scope": 0
    }
    context_stack = []
    filename = "test.py"
    
    # Should not raise any exception
    _verify_children(node, symbol_table, context_stack, filename)
    print("✓ test_missing_children_key passed")


def test_single_valid_child():
    """Test verification of a single valid child node."""
    node = {
        "type": "block",
        "children": [
            {
                "type": "literal",
                "value": 42,
                "line": 2,
                "column": 5
            }
        ],
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {},
        "functions": {},
        "current_scope": 0
    }
    context_stack = []
    filename = "test.py"
    
    # Should not raise any exception for valid literal node
    _verify_children(node, symbol_table, context_stack, filename)
    print("✓ test_single_valid_child passed")


def test_multiple_valid_children():
    """Test verification of multiple valid child nodes."""
    node = {
        "type": "block",
        "children": [
            {
                "type": "literal",
                "value": 42,
                "line": 2,
                "column": 5
            },
            {
                "type": "literal",
                "value": "hello",
                "line": 3,
                "column": 5
            },
            {
                "type": "variable_ref",
                "name": "x",
                "line": 4,
                "column": 5
            }
        ],
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {
            "x": {"type": "int", "scope": 0}
        },
        "functions": {},
        "current_scope": 0
    }
    context_stack = []
    filename = "test.py"
    
    # Should not raise any exception for valid nodes
    _verify_children(node, symbol_table, context_stack, filename)
    print("✓ test_multiple_valid_children passed")


def test_exception_propagation_from_child():
    """Test that exceptions from _verify_node are properly propagated."""
    node = {
        "type": "block",
        "children": [
            {
                "type": "variable_ref",
                "name": "undefined_var",
                "line": 2,
                "column": 5
            }
        ],
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {},
        "functions": {},
        "current_scope": 0
    }
    context_stack = []
    filename = "test.py"
    
    # Should raise exception for undefined variable
    try:
        _verify_children(node, symbol_table, context_stack, filename)
        print("✗ test_exception_propagation_from_child failed: expected exception")
        sys.exit(1)
    except Exception as e:
        # Verify exception contains location info
        assert "test.py" in str(e) or "2" in str(e), f"Exception should contain location info: {e}"
        print("✓ test_exception_propagation_from_child passed")


def test_context_stack_validation():
    """Test that context stack is properly passed to children for control flow validation."""
    # Test break outside loop - should fail
    node = {
        "type": "block",
        "children": [
            {
                "type": "break",
                "line": 2,
                "column": 5
            }
        ],
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {},
        "functions": {},
        "current_scope": 0
    }
    context_stack = []  # No loop context
    filename = "test.py"
    
    try:
        _verify_children(node, symbol_table, context_stack, filename)
        print("✗ test_context_stack_validation failed: break outside loop should raise exception")
        sys.exit(1)
    except Exception as e:
        print("✓ test_context_stack_validation (break outside loop) passed")
    
    # Test break inside loop - should succeed
    context_stack = [{"type": "loop", "stmt_type": "while"}]
    _verify_children(node, symbol_table, context_stack, filename)
    print("✓ test_context_stack_validation (break inside loop) passed")


def test_nested_children_verification():
    """Test that nested children are properly verified through recursion."""
    node = {
        "type": "block",
        "children": [
            {
                "type": "block",
                "children": [
                    {
                        "type": "literal",
                        "value": 123,
                        "line": 3,
                        "column": 9
                    }
                ],
                "line": 2,
                "column": 5
            }
        ],
        "line": 1,
        "column": 1
    }
    symbol_table = {
        "variables": {},
        "functions": {},
        "current_scope": 0
    }
    context_stack = []
    filename = "test.py"
    
    # Should not raise any exception for valid nested structure
    _verify_children(node, symbol_table, context_stack, filename)
    print("✓ test_nested_children_verification passed")


if __name__ == "__main__":
    print("Running _verify_children integration tests...")
    print("=" * 60)
    
    test_empty_children_list()
    test_missing_children_key()
    test_single_valid_child()
    test_multiple_valid_children()
    test_exception_propagation_from_child()
    test_context_stack_validation()
    test_nested_children_verification()
    
    print("=" * 60)
    print("All integration tests passed!")
