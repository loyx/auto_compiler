# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Deferred import to avoid circular dependency
def _get_generate_binop_code():
    from .generate_binop_code_package.generate_binop_code_src import generate_binop_code
    return generate_binop_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # "BINOP", "VAR", "LITERAL"
#   "op": str,         # For BINOP: "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="
#   "left": dict,      # For BINOP: left operand expression dict
#   "right": dict,     # For BINOP: right operand expression dict
#   "name": str,       # For VAR: variable name
#   "value": int,      # For LITERAL: integer literal value
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate ARM64 assembly code for an expression.
    Result is always placed in x0 register.
    Dispatches to type-specific generators.
    """
    expr_type = expr.get("type")
    
    if expr_type == "BINOP":
        return _get_generate_binop_code()(expr, func_name, var_offsets)
    elif expr_type == "VAR":
        return _generate_var_code(expr, var_offsets)
    elif expr_type == "LITERAL":
        return _generate_literal_code(expr)
    else:
        raise ValueError(f"Unsupported expression type: {expr_type} in function {func_name}")

# === helper functions ===
def _generate_var_code(expr: Expr, var_offsets: VarOffsets) -> str:
    """Load variable from stack using ldr x0, [sp, #offset]."""
    var_name = expr.get("name")
    if var_name is None:
        raise ValueError("VAR expression missing 'name' field")
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    offset = var_offsets[var_name]
    return f"ldr x0, [sp, #{offset}]"

def _generate_literal_code(expr: Expr) -> str:
    """Load integer literal using movz/movk instructions."""
    value = expr.get("value")
    if value is None:
        raise ValueError("LITERAL expression missing 'value' field")
    if value < 0:
        if -value <= 65536:
            return f"movn x0, #{-value - 1}"
        return f"movz x0, #65535, lsl #16\norr x0, x0, #{value & 0xFFFF}"
    if value <= 65535:
        return f"movz x0, #{value}"
    upper = (value >> 16) & 0xFFFF
    lower = value & 0xFFFF
    if upper == 0:
        return f"movz x0, #{lower}"
    return f"movz x0, #{upper}, lsl #16\nmovk x0, #{lower}"

# === OOP compatibility layer ===
# Not needed - pure function node
