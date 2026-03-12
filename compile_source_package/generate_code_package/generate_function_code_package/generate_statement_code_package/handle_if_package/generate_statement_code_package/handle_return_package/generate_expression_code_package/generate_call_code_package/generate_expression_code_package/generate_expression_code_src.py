# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_call_code_package.generate_call_code_src import generate_call_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # expression type: "CALL", "VAR", "NUM", etc.
#   "func_name": str,  # for CALL type
#   "args": list,      # for CALL type
#   "name": str,       # for VAR type
#   "value": int,      # for NUM type
# }


# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """
    Recursively generate ARM64 assembly code for any expression type.
    Dispatches based on expr['type'] to type-specific generators.
    """
    expr_type = expr.get("type")
    if expr_type is None:
        raise ValueError("Expression missing type field")

    if expr_type == "CALL":
        return generate_call_code(expr, var_offsets, next_offset)
    elif expr_type == "VAR":
        return _generate_var_code(expr, var_offsets)
    elif expr_type == "NUM":
        return _generate_num_code(expr)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")


# === helper functions ===
def _generate_var_code(expr: Expr, var_offsets: VarOffsets) -> Tuple[str, int, str]:
    """Generate assembly code for VAR type expressions."""
    var_name = expr.get("name")
    if var_name is None:
        raise ValueError("VAR expression missing name field")
    
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    
    offset = var_offsets[var_name]
    code = f"    ldr x0, [sp, #{offset}]\n"
    return (code, len(var_offsets) * 8, "x0")


def _generate_num_code(expr: Expr) -> Tuple[str, int, str]:
    """Generate assembly code for NUM type expressions."""
    value = expr.get("value")
    if value is None:
        raise ValueError("NUM expression missing value field")
    
    code = f"    mov x0, {value}\n"
    return (code, 0, "x0")
