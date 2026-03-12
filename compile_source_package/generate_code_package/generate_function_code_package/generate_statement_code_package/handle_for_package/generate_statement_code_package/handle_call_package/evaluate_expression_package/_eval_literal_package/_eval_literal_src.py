# === std / third-party imports ===
from typing import Any

# === sub function imports ===

# === ADT defines ===
# No ADT needed for this simple function - uses primitive types

# === main function ===
def _eval_literal(value: Any) -> str:
    """
    Generate ARM assembly instruction to load a literal value into R0.
    
    Rules:
    - bool: True -> MOV R0, #1, False -> MOV R0, #0
    - int: -255 <= value <= 255 -> MOV R0, #value, else -> LDR R0, =value
    - other types: raise ValueError
    """
    # Handle boolean values
    if isinstance(value, bool):
        int_value = 1 if value else 0
        return f"MOV R0, #{int_value}"
    
    # Handle integer values
    if isinstance(value, int):
        if -255 <= value <= 255:
            return f"MOV R0, #{value}"
        else:
            return f"LDR R0, ={value}"
    
    # Handle unsupported types
    type_name = type(value).__name__
    raise ValueError(f"Unsupported literal type: {type_name}")

# === helper functions ===

# === OOP compatibility layer ===
