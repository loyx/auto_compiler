#!/usr/bin/env python3
"""Integration tests for handle_var_decl function."""

import sys
import os

# Add project root to path
# Current file is in: handle_var_decl_package/
# Need to go up 5 levels to reach project root where generate_function_code_package exists
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))

from handle_var_decl_package.handle_var_decl_src import (
    handle_var_decl,
)
from handle_var_decl_package.generate_expression_code_package.generate_expression_code_src import (
    generate_expression_code,
)


def test_var_decl_without_init():
    """Test variable declaration without initialization value."""
    stmt = {
        "type": "VAR_DECL",
        "var_name": "x",
        "var_type": "int",
    }
    var_offsets = {}
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 0)
    
    assert var_offsets["x"] == 0
    assert new_offset == 8
    assert "// VAR_DECL: x (int) at offset 0" in code
    assert "str x0" not in code  # No store instruction without init


def test_var_decl_with_literal_init():
    """Test variable declaration with literal integer initialization."""
    stmt = {
        "type": "VAR_DECL",
        "var_name": "count",
        "var_type": "int",
        "init_value": {
            "type": "LITERAL",
            "value": 42,
        },
    }
    var_offsets = {}
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 0)
    
    assert var_offsets["count"] == 0
    assert new_offset == 8
    assert "// VAR_DECL: count (int) at offset 0" in code
    assert "mov x0, #42" in code
    assert "str x0, [sp, 0]" in code


def test_var_decl_with_bool_init():
    """Test variable declaration with boolean initialization."""
    stmt = {
        "type": "VAR_DECL",
        "var_name": "flag",
        "var_type": "bool",
        "init_value": {
            "type": "LITERAL",
            "value": True,
        },
    }
    var_offsets = {}
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 0)
    
    assert var_offsets["flag"] == 0
    assert new_offset == 8
    assert "// VAR_DECL: flag (bool) at offset 0" in code
    assert "mov x0, #1" in code  # True = 1
    assert "str x0, [sp, 0]" in code


def test_var_decl_with_variable_ref_init():
    """Test variable declaration initialized from another variable."""
    # First declare variable 'a'
    stmt_a = {
        "type": "VAR_DECL",
        "var_name": "a",
        "var_type": "int",
        "init_value": {
            "type": "LITERAL",
            "value": 10,
        },
    }
    var_offsets = {}
    code_a, offset_after_a = handle_var_decl(stmt_a, "main", var_offsets, 0)
    
    # Then declare variable 'b' initialized from 'a'
    stmt_b = {
        "type": "VAR_DECL",
        "var_name": "b",
        "var_type": "int",
        "init_value": {
            "type": "IDENTIFIER",
            "var_name": "a",
        },
    }
    code_b, offset_after_b = handle_var_decl(stmt_b, "main", var_offsets, offset_after_a)
    
    assert var_offsets["a"] == 0
    assert var_offsets["b"] == 8
    assert offset_after_b == 16
    assert "ldr x0, [sp, 0]" in code_b  # Load 'a' from offset 0
    assert "str x0, [sp, 8]" in code_b  # Store to 'b' at offset 8


def test_var_decl_with_binary_op_init():
    """Test variable declaration with binary operation initialization."""
    stmt = {
        "type": "VAR_DECL",
        "var_name": "sum",
        "var_type": "int",
        "init_value": {
            "type": "BINARY_OP",
            "op": "ADD",
            "left": {
                "type": "LITERAL",
                "value": 5,
            },
            "right": {
                "type": "LITERAL",
                "value": 3,
            },
        },
    }
    var_offsets = {}
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 0)
    
    assert var_offsets["sum"] == 0
    assert new_offset == 8
    assert "// VAR_DECL: sum (int) at offset 0" in code
    assert "mov x0, #5" in code
    assert "mov x1, #3" in code
    assert "add x0, x0, x1" in code
    assert "str x0, [sp, 0]" in code


def test_var_decl_with_non_zero_offset():
    """Test variable declaration starting from non-zero offset."""
    stmt = {
        "type": "VAR_DECL",
        "var_name": "local",
        "var_type": "int",
        "init_value": {
            "type": "LITERAL",
            "value": 100,
        },
    }
    var_offsets = {"param1": 0, "param2": 8}  # Simulate existing params
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 16)
    
    assert var_offsets["local"] == 16
    assert new_offset == 24
    assert "// VAR_DECL: local (int) at offset 16" in code
    assert "mov x0, #100" in code
    assert "str x0, [sp, 16]" in code


def test_var_decl_multiple_sequential():
    """Test multiple sequential variable declarations."""
    var_offsets = {}
    offset = 0
    all_code = []
    
    declarations = [
        {"var_name": "x", "value": 1},
        {"var_name": "y", "value": 2},
        {"var_name": "z", "value": 3},
    ]
    
    for decl in declarations:
        stmt = {
            "type": "VAR_DECL",
            "var_name": decl["var_name"],
            "var_type": "int",
            "init_value": {
                "type": "LITERAL",
                "value": decl["value"],
            },
        }
        code, offset = handle_var_decl(stmt, "main", var_offsets, offset)
        all_code.append(code)
    
    assert var_offsets["x"] == 0
    assert var_offsets["y"] == 8
    assert var_offsets["z"] == 16
    assert offset == 24
    
    # Verify each variable is stored at correct offset
    assert "str x0, [sp, 0]" in all_code[0]
    assert "str x0, [sp, 8]" in all_code[1]
    assert "str x0, [sp, 16]" in all_code[2]


def test_var_decl_complex_expression():
    """Test variable declaration with complex nested expression."""
    # (a + b) * 2 where a=5, b=3
    stmt = {
        "type": "VAR_DECL",
        "var_name": "result",
        "var_type": "int",
        "init_value": {
            "type": "BINARY_OP",
            "op": "MUL",
            "left": {
                "type": "BINARY_OP",
                "op": "ADD",
                "left": {
                    "type": "LITERAL",
                    "value": 5,
                },
                "right": {
                    "type": "LITERAL",
                    "value": 3,
                },
            },
            "right": {
                "type": "LITERAL",
                "value": 2,
            },
        },
    }
    var_offsets = {}
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 0)
    
    assert var_offsets["result"] == 0
    assert new_offset == 8
    assert "// VAR_DECL: result (int) at offset 0" in code
    assert "add x0, x0, x1" in code  # 5 + 3
    assert "mul x0, x0, x1" in code  # (5+3) * 2
    assert "str x0, [sp, 0]" in code


def test_var_decl_preserves_existing_offsets():
    """Test that existing variable offsets are preserved."""
    var_offsets = {"existing_var": 0}
    
    stmt = {
        "type": "VAR_DECL",
        "var_name": "new_var",
        "var_type": "int",
        "init_value": {
            "type": "LITERAL",
            "value": 99,
        },
    }
    code, new_offset = handle_var_decl(stmt, "main", var_offsets, 8)
    
    assert var_offsets["existing_var"] == 0  # Unchanged
    assert var_offsets["new_var"] == 8
    assert new_offset == 16


def test_generate_expression_code_direct():
    """Direct test of generate_expression_code integration."""
    # Test that handle_var_decl correctly integrates with generate_expression_code
    expr = {
        "type": "BINARY_OP",
        "op": "SUB",
        "left": {
            "type": "LITERAL",
            "value": 100,
        },
        "right": {
            "type": "LITERAL",
            "value": 37,
        },
    }
    
    # Test generate_expression_code directly
    expr_code = generate_expression_code(expr, "test_func", {})
    assert "mov x0, #100" in expr_code
    assert "mov x1, #37" in expr_code
    assert "sub x0, x0, x1" in expr_code
    
    # Now test through handle_var_decl
    stmt = {
        "type": "VAR_DECL",
        "var_name": "diff",
        "var_type": "int",
        "init_value": expr,
    }
    var_offsets = {}
    code, new_offset = handle_var_decl(stmt, "test_func", var_offsets, 0)
    
    assert var_offsets["diff"] == 0
    assert "sub x0, x0, x1" in code
    assert "str x0, [sp, 0]" in code


if __name__ == "__main__":
    test_var_decl_without_init()
    test_var_decl_with_literal_init()
    test_var_decl_with_bool_init()
    test_var_decl_with_variable_ref_init()
    test_var_decl_with_binary_op_init()
    test_var_decl_with_non_zero_offset()
    test_var_decl_multiple_sequential()
    test_var_decl_complex_expression()
    test_var_decl_preserves_existing_offsets()
    test_generate_expression_code_direct()
    print("All integration tests passed!")
