# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_binary_op_code_package.generate_binary_op_code_src import generate_binary_op_code
from .generate_unary_op_code_package.generate_unary_op_code_src import generate_unary_op_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,
#   "value": Any,
#   "var_name": str,
#   "left": dict,
#   "right": dict,
#   "operator": str,
#   "operand": dict,
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Recursively generate ARM64 assembly code for expression trees."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return _generate_literal_code(expr["value"])
    elif expr_type == "variable":
        return _generate_variable_code(expr["var_name"], var_offsets)
    elif expr_type == "binary_op":
        return generate_binary_op_code(
            expr["left"], expr["right"], expr["operator"], var_offsets, next_offset
        )
    elif expr_type == "unary_op":
        return generate_unary_op_code(
            expr["operand"], expr["operator"], var_offsets, next_offset
        )
    else:
        raise ValueError(f"Invalid expression type: {expr_type}")

# === helper functions ===
def _generate_literal_code(value: Any) -> Tuple[str, int]:
    """Generate MOV instruction for literal value. Result in x0."""
    if isinstance(value, int) and abs(value) <= 0xFFFF:
        return f"    MOV x0, #{value}\n", 0
    elif isinstance(value, int):
        # Handle large values with MOVZ/MOVK sequence
        low = value & 0xFFFF
        high = (value >> 16) & 0xFFFF
        code = f"    MOVZ x0, #{low}\n"
        if high:
            code += f"    MOVK x0, #{high}, LSL #16\n"
        return code, 0
    else:
        return f"    MOV x0, #{value}\n", 0

def _generate_variable_code(var_name: str, var_offsets: VarOffsets) -> Tuple[str, int]:
    """Generate LDR instruction to load variable from stack. Result in x0."""
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    offset = var_offsets[var_name]
    return f"    LDR x0, [sp, #{offset}]\n", 0

# === OOP compatibility layer ===
