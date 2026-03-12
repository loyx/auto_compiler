# === std / third-party imports ===
from typing import Dict

# === sub function imports ===
# No sub functions needed for this simple lookup operation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name -> byte offset from FP
# }

# === main function ===
def _eval_identifier(name: str, var_offsets: VarOffsets) -> str:
    """
    Generate ARM assembly to load a variable value from stack into R0.
    
    Looks up variable name in var_offsets to get stack offset,
    then generates LDR instruction with negative offset (locals below FP).
    
    Args:
        name: Variable name to look up in var_offsets
        var_offsets: Dict mapping variable names to byte offsets from FP
    
    Returns:
        ARM assembly instruction string (single line, no trailing newline)
    
    Raises:
        ValueError: If variable name not found in var_offsets
    """
    if name not in var_offsets:
        raise ValueError(f"Undefined variable: {name}")
    
    offset = var_offsets[name]
    return f"LDR R0, [FP, #-{offset}]"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
