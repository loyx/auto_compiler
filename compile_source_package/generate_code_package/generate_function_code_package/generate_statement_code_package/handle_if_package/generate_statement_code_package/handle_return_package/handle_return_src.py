# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT define ===
Expr = Dict[str, Any]
# Expr possible fields for BINOP:
# {
#   "type": "binop",
#   "op": str,         # "+", "-", "*", "/"
#   "left": Expr,      # left operand
#   "right": Expr,     # right operand
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

# === main function ===
def generate_binop_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate assembly code for binary operation expression."""
    code_lines = []
    
    # Generate code for left operand
    left_code, offset_after_left, left_reg = generate_expression_code(
        expr["left"], var_offsets, next_offset
    )
    code_lines.append(left_code)
    
    # Generate code for right operand
    right_code, offset_after_right, right_reg = generate_expression_code(
        expr["right"], var_offsets, offset_after_left
    )
    code_lines.append(right_code)
    
    # Perform the operation, result in x0
    op = expr["op"]
    asm_op = {
        "+": "add",
        "-": "sub",
        "*": "mul",
        "/": "sdiv"
    }.get(op, "add")
    
    code_lines.append(f"    {asm_op} x0, {left_reg}, {right_reg}")
    
    # Join all code lines
    assembled_code = "\n".join(code_lines)
    
    return (assembled_code, offset_after_right, "x0")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a function node, not a framework entry point
