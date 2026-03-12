# === std / third-party imports ===
from typing import Any, Tuple

# === sub function imports ===
# No subfunctions for this leaf node

# === ADT defines ===
# This function uses simple types, no complex ADT needed.
# Input: value (Any - int or bool), next_offset (int)
# Output: Tuple[str, int] - (assembly code string, unchanged next_offset)

# === main function ===
def generate_literal_code(value: Any, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM64 assembly code to load a literal value into x0 register.
    
    Args:
        value: The literal value to load (int or bool). For bool, True=1, False=0.
        next_offset: Current next available stack offset (unchanged since literals don't need stack temps)
    
    Returns:
        Tuple of (assembly code string, unchanged next_offset)
    """
    # Convert boolean to integer
    if isinstance(value, bool):
        value = 1 if value else 0
    
    # Ensure we have an integer
    if not isinstance(value, int):
        raise TypeError(f"Expected int or bool, got {type(value).__name__}")
    
    # Generate appropriate ARM64 instruction based on value range
    if -4096 <= value <= 4095:
        # Small immediate fits in single mov instruction
        code = f"mov x0, #{value}"
    elif value >= 0:
        # Positive large value: use movz for low bits, movk for high bits
        low16 = value & 0xFFFF
        high16 = (value >> 16) & 0xFFFF
        if high16 == 0:
            code = f"movz x0, #{low16}, lsl #0"
        else:
            code = f"movz x0, #{low16}, lsl #0\nmovk x0, #{high16}, lsl #16"
    else:
        # Negative large value: use movn to load inverted value
        inverted = ~value
        low16 = inverted & 0xFFFF
        high16 = (inverted >> 16) & 0xFFFF
        if high16 == 0:
            code = f"movn x0, #{low16}, lsl #0"
        else:
            code = f"movn x0, #{low16}, lsl #0\nmovk x0, #{high16}, lsl #16"
    
    return (code, next_offset)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node