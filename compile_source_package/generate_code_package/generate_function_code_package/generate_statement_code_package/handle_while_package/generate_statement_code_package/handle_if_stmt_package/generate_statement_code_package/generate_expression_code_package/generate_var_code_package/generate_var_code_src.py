# === std / third-party imports ===
from typing import Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple operation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

CodeResult = Tuple[str, int]
# CodeResult possible fields:
# {
#   [0]: str,  # Generated ARM64 assembly code string
#   [1]: int   # Next available stack offset (unchanged)
# }

# === main function ===
def generate_var_code(var_name: str, var_offsets: VarOffsets, next_offset: int) -> CodeResult:
    """
    Generate ARM64 code to load a variable from stack into x0.
    
    Args:
        var_name: The name of the variable to load
        var_offsets: Dictionary mapping variable names to stack offsets
        next_offset: Current next available stack offset (unchanged by this function)
    
    Returns:
        Tuple of (generated_code, next_offset) where next_offset is unchanged
    
    Raises:
        KeyError: If var_name is not found in var_offsets
    """
    if var_name not in var_offsets:
        raise KeyError(f"Undefined variable: {var_name}")
    
    offset = var_offsets[var_name]
    code = f"LDR x0, [sp, #{offset}]\n"
    
    return (code, next_offset)

# === helper functions ===
# No helper functions needed for this simple operation

# === OOP compatibility layer ===
# Not needed - this is a pure function node, not a framework entry point
