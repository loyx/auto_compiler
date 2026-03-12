# === std / third-party imports ===
from typing import Dict, List, Tuple

# === sub function imports ===
# No sub functions needed for this simple logic

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # Maps variable name to stack offset
# }

Param = Dict[str, str]
# Param possible fields:
# {
#   "name": str,  # Parameter name
#   "type": str,  # Parameter type
# }

# === main function ===
def build_var_offsets(params: List[Param], param_start_offset: int) -> Tuple[VarOffsets, int]:
    """
    Build variable offset dictionary mapping parameters to stack offsets.
    
    Each parameter occupies 8 bytes on the stack. Offsets are assigned
    sequentially starting from param_start_offset.
    
    Args:
        params: List of parameter dicts with "name" and "type" fields
        param_start_offset: Starting offset (typically 16 for fp/lr save area)
    
    Returns:
        Tuple of (var_offsets dict, next_offset int)
    
    Example:
        Input: params=[{"name": "x", "type": "int"}, {"name": "y", "type": "int"}], 
               param_start_offset=16
        Output: ({"x": 16, "y": 24}, 32)
    """
    var_offsets: VarOffsets = {}
    current_offset = param_start_offset
    
    for param in params:
        var_offsets[param["name"]] = current_offset
        current_offset += 8
    
    next_offset = current_offset
    return var_offsets, next_offset

# === helper functions ===
# No helper functions needed; logic is simple enough for main function

# === OOP compatibility layer ===
# Not needed for this function node (not a framework entry point)
