# === std / third-party imports ===
# No external imports needed for this simple function

# === sub function imports ===
# No sub functions to import

# === ADT defines ===
# No complex ADT needed - simple int -> str transformation

# === main function ===
def _generate_const_code(value: int) -> str:
    """
    Generate ARM64 assembly instruction to load integer constant into x0.
    
    Args:
        value: Integer constant value (-32768 to 32767 immediate range)
    
    Returns:
        ARM64 assembly string, e.g., "mov x0, #5"
    """
    return f"mov x0, #{value}"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a simple utility function node