# === std / third-party imports ===
from typing import Any, Tuple

# === sub function imports ===
# No child functions needed - logic is inline

# === ADT defines ===
# No complex ADTs - uses basic types (Any, Tuple[str, int])

# === main function ===
def generate_literal_code(value: Any, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM64 assembly code to load a literal value into x0.
    
    Args:
        value: The literal value to load (int or bool supported)
        next_offset: Current stack offset (unchanged by this function)
    
    Returns:
        Tuple of (assembly_code_string, next_offset)
    
    Raises:
        ValueError: If value type is not int or bool
    """
    # Handle bool type (must check before int since bool is subclass of int)
    if isinstance(value, bool):
        if value:
            return ("MOV x0, #1\n", next_offset)
        else:
            return ("MOV x0, #0\n", next_offset)
    
    # Handle int type
    if isinstance(value, int):
        # Check if value fits in single MOV instruction (16-bit signed)
        if -65536 <= value <= 65535:
            return (f"MOV x0, #{value}\n", next_offset)
        else:
            # Large value: use MOVZ/MOVK sequence
            return (_generate_large_int_code(value), next_offset)
    
    # Unsupported type
    raise ValueError(f"Literal type not supported: {type(value)}")

# === helper functions ===
def _generate_large_int_code(value: int) -> str:
    """
    Generate MOVZ/MOVK sequence for large integers (>65535 or <-65536).
    
    Args:
        value: The integer value to encode
    
    Returns:
        Assembly code string with MOVZ/MOVK instructions
    """
    # Convert to unsigned 64-bit representation for bit manipulation
    if value < 0:
        unsigned_val = value & 0xFFFFFFFFFFFFFFFF
    else:
        unsigned_val = value
    
    # Extract 16-bit chunks (little-endian order for shifts)
    chunks = []
    for shift in [0, 16, 32, 48]:
        chunk = (unsigned_val >> shift) & 0xFFFF
        chunks.append((shift, chunk))
    
    # Find the highest non-zero chunk to start with MOVZ
    code_lines = []
    started = False
    
    # Process from highest to lowest chunk
    for shift, chunk in reversed(chunks):
        if chunk != 0 or (not started and shift == 0):
            if not started:
                # First non-zero chunk uses MOVZ
                code_lines.append(f"MOVZ x0, #{chunk}, LSL #{shift}")
                started = True
            else:
                # Subsequent chunks use MOVK
                code_lines.append(f"MOVK x0, #{chunk}, LSL #{shift}")
    
    # Ensure at least one instruction (for value 0, though it should be handled by small int path)
    if not code_lines:
        code_lines.append("MOVZ x0, #0")
    
    return "\n".join(code_lines) + "\n"

# === OOP compatibility layer ===
# Not needed - this is a utility function node, not a framework entry point
