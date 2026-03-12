# === std / third-party imports ===
from typing import Dict

# === sub function imports ===
# No subfunctions for this leaf node

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

# === main function ===
def _generate_var_code(var_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate ARM64 assembly code to load a variable from stack into x0.
    
    Args:
        var_name: Name of the variable to load from the stack.
        var_offsets: Immutable lookup dict mapping variable names to stack offsets.
    
    Returns:
        ARM64 assembly instruction string.
    
    Raises:
        KeyError: If var_name is not found in var_offsets.
    """
    if var_name not in var_offsets:
        raise KeyError(f"Undefined variable: {var_name}")
    
    offset = var_offsets[var_name]
    return f"ldr x0, [sp, #{offset}]"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this utility function