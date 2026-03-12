# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions required for this module

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
def _handle_ident(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """
    Generate assembly code for IDENT expression.
    
    Loads variable from stack slot: 'ldr x0, [sp, #byte_offset]'
    Raises ValueError if variable is not defined in var_offsets.
    """
    var_name = expr["name"]
    
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    
    slot_index = var_offsets[var_name]
    byte_offset = slot_index * 8
    
    assembly = f"    ldr x0, [sp, #{byte_offset}]"
    
    return (assembly, next_offset, "x0")

# === helper functions ===
# No helper functions required

# === OOP compatibility layer ===
# Not required for this function node
