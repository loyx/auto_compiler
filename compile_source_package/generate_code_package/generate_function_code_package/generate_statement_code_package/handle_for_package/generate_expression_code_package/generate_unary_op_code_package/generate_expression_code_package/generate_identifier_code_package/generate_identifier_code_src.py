# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple operation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name -> stack offset
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "UNARY_OP" | "CALL"
#   "name": str,  # For IDENTIFIER type
# }

# === main function ===
def generate_identifier_code(expr: Expression, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM assembly code to load a variable from stack into x0 register.
    
    Args:
        expr: Expression dict with type="IDENTIFIER" and "name" field
        var_offsets: Mapping from variable names to stack offsets
        next_offset: Current next available stack offset (unchanged by this function)
    
    Returns:
        Tuple of (generated ARM code, next_offset unchanged)
    
    Raises:
        KeyError: If variable name is not found in var_offsets
    """
    var_name = expr["name"]
    offset = var_offsets[var_name]  # Raises KeyError if not found
    code = f"ldr x0, [sp, #{offset}]"
    return code, next_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a pure function node, not a framework entry point
