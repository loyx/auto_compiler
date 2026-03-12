# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions needed for this simple literal handler

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

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

# === main function ===
def _handle_literal(expr: dict, next_offset: int) -> Tuple[str, int]:
    """
    Handle LITERAL expression type.
    
    Generate ARM assembly code to load a literal constant into R0.
    
    Args:
        expr: dict with "type" (must be "LITERAL") and "value" (int)
        next_offset: Current next available stack offset
    
    Returns:
        Tuple[assembly_code, next_offset] where next_offset is unchanged
    
    Example:
        Input: {"type": "LITERAL", "value": 42}, next_offset=10
        Output: ("MOV R0, #42", 10)
    """
    value = expr["value"]
    assembly_code = f"MOV R0, #{value}"
    return (assembly_code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
