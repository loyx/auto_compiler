# === std / third-party imports ===
# No external imports needed for this simple utility

# === sub function imports ===
# No child functions for this simple utility

# === ADT defines ===
# No complex ADTs needed; uses primitive int and str

# === main function ===
def _generate_literal_code(value: int) -> str:
    """
    Generate ARM assembly code to load an integer literal into R0.
    
    Args:
        value: 32-bit signed integer (-2147483648 to 2147483647)
    
    Returns:
        Assembly string (e.g., 'MOV R0, #5' or 'LDR R0, =1000000')
    
    Raises:
        ValueError: If value is outside 32-bit signed integer range
    """
    # Validate 32-bit signed integer range
    if value < -2147483648 or value > 2147483647:
        raise ValueError(
            f"Value {value} is outside 32-bit signed integer range "
            f"(-2147483648 to 2147483647)"
        )
    
    # ARM MOV immediate can encode 8-bit values (0-255) directly
    # For simplicity, use MOV for values in range [-255, 255]
    # Larger values require LDR pseudo-instruction
    if -255 <= value <= 255:
        return f"MOV R0, #{value}"
    else:
        return f"LDR R0, ={value}"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
