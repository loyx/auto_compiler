# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions for this module

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "VAR",
#   "name": str,  # variable name for VAR type
# }

# === main function ===
def generate_var_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """
    Generate ARM64 assembly code for VAR expression type.
    
    Loads variable from stack using ldr instruction with offset from var_offsets.
    """
    var_name = expr["name"]
    
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    
    offset = var_offsets[var_name]
    assembly_code = f"    ldr x0, [sp, #{offset}]\n"
    
    return (assembly_code, next_offset, "x0")

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
