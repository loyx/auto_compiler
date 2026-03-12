# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "literal" | "variable" | "binary_op" | "unary_op" | "comparison" | "and" | "or"
#   "value": Any,  # for literal type
#   "var_name": str,  # for variable type
#   "left": dict,  # for binary_op/comparison/and/or
#   "right": dict,  # for binary_op/comparison/and/or
#   "operator": str,  # for binary_op/unary_op/comparison
#   "operand": dict,  # for unary_op
# }

# === main function ===
def generate_comparison_code(left: dict, right: dict, operator: str, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 comparison code using cmp + cset pattern."""
    # Condition code mapping
    condition_map = {
        "==": "eq",
        "!=": "ne",
        "<": "lt",
        ">": "gt",
        "<=": "le",
        ">=": "ge",
    }
    
    condition_code = condition_map[operator]
    
    # Generate code for left operand
    left_code, left_offset = generate_expression_code(left, var_offsets, next_offset)
    
    # Generate code for right operand (starting from updated offset)
    right_code, right_offset = generate_expression_code(right, var_offsets, left_offset)
    
    # Build the comparison code pattern
    code_lines = [
        left_code,
        "str x0, [sp, #-8]!",
        right_code,
        "ldr x1, [sp, #8]",
        "add sp, sp, #8",
        f"cmp x1, x0",
        f"cset x0, {condition_code}",
    ]
    
    assembly_code = "\n".join(line for line in code_lines if line)
    
    # Return with updated offset (one temporary used: 8 bytes)
    return (assembly_code, right_offset + 8)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
