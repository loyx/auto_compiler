# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No subfunctions needed for this simple operation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,      # expression type, e.g., "IDENTIFIER"
#   "name": str,      # variable name (for IDENTIFIER type)
# }

# === main function ===
def generate_identifier_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM assembly code for an IDENTIFIER expression.
    
    Looks up the variable name in var_offsets and generates a load instruction.
    Returns the code string and unchanged next_offset.
    Raises KeyError if variable not found in var_offsets.
    """
    var_name = expr["name"]
    
    if var_name not in var_offsets:
        raise KeyError(f"Variable '{var_name}' not found in var_offsets")
    
    offset = var_offsets[var_name]
    code = f"ldr x0, [sp, #{offset}]"
    
    return (code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node