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
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate ARM64 assembly code for an expression."""
    expr_type = expr.get("type")
    
    if expr_type == "VAR":
        name = expr.get("name")
        offset = var_offsets.get(name)
        if offset is None:
            raise ValueError(f"Variable '{name}' not found in var_offsets")
        code = f"    ldr x0, [sp, #{offset}]\n"
        return (code, next_offset, "x0")
    
    elif expr_type == "NUM":
        value = expr.get("value")
        code = f"    mov x0, #{value}\n"
        return (code, next_offset, "x0")
    
    elif expr_type == "BINOP":
        return generate_binop_code(expr, var_offsets, next_offset)
    
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not needed - this is a pure function node