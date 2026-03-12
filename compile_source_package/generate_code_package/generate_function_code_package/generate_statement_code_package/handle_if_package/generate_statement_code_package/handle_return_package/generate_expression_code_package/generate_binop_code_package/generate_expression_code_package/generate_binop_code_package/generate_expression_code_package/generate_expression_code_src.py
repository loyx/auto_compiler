# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_binop_code_package.generate_binop_code_src import generate_binop_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "VAR" | "NUM" | "BINOP",
#   "name": str,        # for VAR type: variable name
#   "value": int,       # for NUM type: numeric value
#   "op": str,          # for BINOP type: "ADD" | "SUB" | "MUL" | "DIV"
#   "left": Expr,       # for BINOP type: left operand
#   "right": Expr,      # for BINOP type: right operand
# }

# === main function ===
def generate_expression_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate ARM64 assembly code for any expression type (VAR, NUM, or BINOP)."""
    expr_type = expr["type"]
    
    if expr_type == "VAR":
        offset = var_offsets[expr["name"]]
        code = f"ldr x0, [sp, #{offset}]\n"
        return (code, next_offset, "x0")
    
    elif expr_type == "NUM":
        value = expr["value"]
        code = f"mov x0, #{value}\n"
        return (code, next_offset, "x0")
    
    elif expr_type == "BINOP":
        return generate_binop_code(expr, var_offsets, next_offset)
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - logic is simple dispatch

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a utility function node
