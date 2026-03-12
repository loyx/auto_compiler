# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_short_circuit_and_package.generate_short_circuit_and_src import generate_short_circuit_and
from .generate_short_circuit_or_package.generate_short_circuit_or_src import generate_short_circuit_or
from .generate_arithmetic_comparison_code_package.generate_arithmetic_comparison_code_src import generate_arithmetic_comparison_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "skip": int,
#   "true": int,
#   "false": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

ExprDict = Dict[str, Any]
# ExprDict possible fields:
# {
#   "type": str,
#   "operator": str,
#   "left": ExprDict,
#   "right": ExprDict,
#   "value": Any,
#   "name": str,
# }

# === main function ===
def generate_binary_op_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for binary operations."""
    operator = expr.get("operator", "")
    left = expr.get("left")
    right = expr.get("right")
    
    # Handle short-circuit logical operators
    if operator == "AND":
        return generate_short_circuit_and(expr, func_name, label_counter, var_offsets, next_offset)
    elif operator == "OR":
        return generate_short_circuit_or(expr, func_name, label_counter, var_offsets, next_offset)
    
    # Generate code for left operand
    from .generate_expr_code.generate_expr_code_src import generate_expr_code
    left_code_str, next_offset = generate_expr_code(left, func_name, label_counter, var_offsets, next_offset)
    
    # Generate code for right operand
    right_code_str, next_offset = generate_expr_code(right, func_name, label_counter, var_offsets, next_offset)
    
    # Combine with operation instruction
    op_instruction = generate_arithmetic_comparison_code(operator, left_code_str, right_code_str)
    
    # Build final code: left, move to x1, right, operation
    code_lines = [left_code_str, "    mov x1, x0", right_code_str, op_instruction]
    full_code = "\n".join(code_lines)
    
    return full_code, next_offset

# === helper functions ===
# No helper functions - all logic delegated to child nodes

# === OOP compatibility layer ===
# Not required - this is a pure function node
