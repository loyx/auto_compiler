# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_num_code_package.generate_num_code_src import generate_num_code
from .generate_var_code_package.generate_var_code_src import generate_var_code
from .generate_binop_code_package.generate_binop_code_src import generate_binop_code
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
#   "type": "NUM" | "VAR" | "BINOP" | "CALL",
#   "value": int,           # For NUM: numeric value
#   "name": str,            # For VAR: variable name
#   "op": str,              # For BINOP: "ADD" | "SUB" | "MUL" | "DIV"
#   "left": Expr,           # For BINOP: left operand
#   "right": Expr,          # For BINOP: right operand
#   "func_name": str,       # For CALL: function to call
#   "args": list,           # For CALL: list of argument Expr dicts
# }

# === main function ===
def generate_expression_code(
    expr: Expr,
    var_offsets: VarOffsets,
    next_offset: int
) -> Tuple[str, int, str]:
    """
    Generate ARM64 assembly code for an expression.
    
    Dispatches to type-specific generators based on expr["type"].
    
    Returns:
        (assembly_code, updated_next_offset, result_register)
    """
    expr_type = expr.get("type")
    
    if expr_type == "NUM":
        return generate_num_code(expr, next_offset)
    elif expr_type == "VAR":
        return generate_var_code(expr, var_offsets, next_offset)
    elif expr_type == "BINOP":
        return generate_binop_code(expr, var_offsets, next_offset)
    elif expr_type == "CALL":
        return generate_call_code(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===

# === OOP compatibility layer ===
