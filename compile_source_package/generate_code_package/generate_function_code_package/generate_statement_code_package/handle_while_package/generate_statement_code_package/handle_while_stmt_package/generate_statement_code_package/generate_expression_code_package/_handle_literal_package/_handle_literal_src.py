# === std / third-party imports ===
from typing import Any, Tuple

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
# No complex ADTs needed for this simple function

# === main function ===
def _handle_literal(value: Any, next_offset: int) -> Tuple[str, int, int]:
    """
    Generate LOAD_CONST instruction for literal values.
    
    Args:
        value: The literal value (int, float, str, bool, None, list, dict)
        next_offset: Current next available stack offset
    
    Returns:
        Tuple of (assembly_code, stack_offset, next_offset+1)
    """
    assembly = f"LOAD_CONST {repr(value)}\n"
    return (assembly, next_offset, next_offset + 1)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
