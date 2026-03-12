# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions needed for this simple handler

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

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
#   "var_name": str,
#   "var_type": str,
# }

# === main function ===
def handle_decl(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """
    Handle DECL statement code generation.
    
    Allocates stack space for variable declaration and updates var_offsets mapping.
    """
    # Extract variable name from statement
    var_name = stmt["var_name"]
    
    # Mutate var_offsets: map var_name to current next_offset
    var_offsets[var_name] = next_offset
    
    # Generate ARM assembly for stack allocation (4 bytes for int/float)
    asm_code = "SUB SP, SP, #4"
    
    # Calculate updated offset
    updated_offset = next_offset + 4
    
    return (asm_code, updated_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
