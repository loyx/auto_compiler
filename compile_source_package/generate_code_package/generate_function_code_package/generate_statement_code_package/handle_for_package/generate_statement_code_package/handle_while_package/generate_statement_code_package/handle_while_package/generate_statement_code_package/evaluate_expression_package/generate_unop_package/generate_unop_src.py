# === std / third-party imports ===
# No standard library imports needed beyond built-in types

# === sub function imports ===
# No sub functions needed for this simple operation

# === ADT defines ===
# No special ADT needed - using simple string types
# Input: str - unary operator string
# Output: str - ARM32 assembly code

# === main function ===
def generate_unop(op: str) -> str:
    """
    Generate ARM32 assembly code for unary operations.
    
    Assumes operand is already in r0. Result must be placed in r0.
    
    Args:
        op: str - Unary operator string. Valid values: "-", "not"
    
    Returns:
        str - ARM32 assembly code string
    
    Raises:
        ValueError: For unknown operators
    """
    if op == "-":
        # Negation: r0 = 0 - r0
        return "rsb r0, r0, #0"
    elif op == "not":
        # Logical not: return 1 if r0 is 0, 0 if r0 is non-zero
        return "cmp r0, #0\nmoveq r0, #1\nmovne r0, #0"
    else:
        raise ValueError(f"Unknown unary operator: {op}")

# === helper functions ===
# No helper functions needed for this simple implementation

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node