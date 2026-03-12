# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "CALL"
#   "value": int,  # for LITERAL
#   "name": str,  # for IDENTIFIER
#   "op": str,  # for BINARY_OP
#   "left": Dict,  # for BINARY_OP
#   "right": Dict,  # for BINARY_OP
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

# === main function ===
def _handle_identifier(expr: Expression, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM assembly code to load a variable from the stack into R0.
    
    Args:
        expr: IDENTIFIER expression dict with "type" and "name" fields
        var_offsets: Mapping from variable names to stack offsets
        next_offset: Current next available stack offset (unchanged for identifiers)
    
    Returns:
        Tuple of (LDR instruction string, unchanged next_offset)
    
    Raises:
        KeyError: If variable name is not found in var_offsets
    """
    var_name = expr["name"]
    
    if var_name not in var_offsets:
        raise KeyError(f"Variable '{var_name}' not found in var_offsets")
    
    offset = var_offsets[var_name]
    assembly_code = f"LDR R0, [FP, #{offset}]"
    
    return (assembly_code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
