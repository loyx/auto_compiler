# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No subfunctions needed for this simple handler

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # maps variable name to stack slot index
# }

Expr = Dict[str, Any]
# Expr possible fields by type:
# LITERAL: {"type": "LITERAL", "value": int|float}
# IDENT: {"type": "IDENT", "name": str}
# BINARY: {"type": "BINARY", "op": str, "left": Expr, "right": Expr}
# UNARY: {"type": "UNARY", "op": str, "operand": Expr}

# === main function ===
def _handle_literal(expr: dict, next_offset: int) -> Tuple[str, int, str]:
    """
    Generate assembly code for LITERAL expression.
    
    Args:
        expr: Expression dict with "type" == "LITERAL" and "value" field (int or float)
        next_offset: Current stack slot counter (passed through unchanged for literals)
    
    Returns:
        Tuple[str, int, str]: (assembly_code, next_offset, result_register)
    """
    value = expr["value"]
    
    if isinstance(value, float):
        if value == 0.0:
            asm_code = "    fmov v0, #0.0"
        else:
            asm_code = f"    ldr v0, ={value}"
        result_reg = "v0"
    else:  # int
        asm_code = f"    mov x0, #{value}"
        result_reg = "x0"
    
    return (asm_code, next_offset, result_reg)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
