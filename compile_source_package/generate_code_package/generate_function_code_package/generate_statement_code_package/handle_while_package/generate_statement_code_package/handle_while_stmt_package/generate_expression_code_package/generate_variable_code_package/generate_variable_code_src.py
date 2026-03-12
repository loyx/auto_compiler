# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple lookup operation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # Maps variable name to its stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,
#   "value": Any,
#   "var_name": str,
#   "left": dict,
#   "right": dict,
#   "operator": str,
#   "operand": dict,
# }

# === main function ===
def generate_variable_code(var_name: str, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM64 assembly code to load a variable from stack into x0 register.
    
    Args:
        var_name: Name of the variable to load from stack
        var_offsets: Mapping of variable names to their stack offsets (read-only)
        next_offset: Current next available stack offset (unchanged since we're just reading)
    
    Returns:
        Tuple of (assembly code string, unchanged next_offset)
    
    Raises:
        KeyError: If var_name is not found in var_offsets
    """
    if var_name not in var_offsets:
        raise KeyError(f"Variable '{var_name}' not found in var_offsets")
    
    offset = var_offsets[var_name]
    code = f"ldr x0, [sp, #{offset}]"
    return (code, next_offset)

# === helper functions ===
# No helper functions needed for this simple operation

# === OOP compatibility layer ===
# Not needed for this function node