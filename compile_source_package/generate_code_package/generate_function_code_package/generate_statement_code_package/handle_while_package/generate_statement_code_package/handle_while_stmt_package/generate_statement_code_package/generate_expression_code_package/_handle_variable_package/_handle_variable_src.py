# === std / third-party imports ===
from typing import Dict, Tuple

# === sub function imports ===
# No sub functions needed for this simple lookup operation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to its stack slot offset
# }

# === main function ===
def _handle_variable(name: str, var_offsets: Dict[str, int], next_offset: int) -> Tuple[str, int, int]:
    """
    Generate LOAD instruction for variable lookup.
    
    Args:
        name: The variable name to look up
        var_offsets: Mapping of variable names to their stack slot offsets
        next_offset: Current next available stack offset
    
    Returns:
        Tuple of (assembly_code_string, slot_offset, next_offset)
    
    Raises:
        KeyError: If variable name is not found in var_offsets
    """
    # Look up the variable name in var_offsets to get its stack slot
    slot_offset = var_offsets[name]  # Raises KeyError if not found
    
    # Emit a LOAD instruction to load from that slot
    # Assembly format: "LOAD {slot_offset}" followed by newline
    assembly_code = f"LOAD {slot_offset}\n"
    
    # Return tuple: (assembly_code_string, slot_offset, next_offset)
    # next_offset does not change because variable value is already at slot_offset
    return (assembly_code, slot_offset, next_offset)

# === helper functions ===
# No helper functions needed for this simple operation

# === OOP compatibility layer ===
# Not needed - this is a simple function node, not a framework entry point