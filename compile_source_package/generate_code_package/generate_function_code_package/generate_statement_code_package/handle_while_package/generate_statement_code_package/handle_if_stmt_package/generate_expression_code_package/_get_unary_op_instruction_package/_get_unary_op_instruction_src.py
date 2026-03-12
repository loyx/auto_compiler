# === std / third-party imports ===
# No external imports needed

# === sub function imports ===
# No subfunctions to import

# === ADT defines ===
# No complex ADTs needed - uses str only

# === main function ===
def _get_unary_op_instruction(op: str) -> str:
    """
    Returns ARM64 assembly instruction string for unary operator.
    
    Assumes x0 contains the operand on entry. Result is placed in x0 register.
    
    Args:
        op: Unary operator name. Must be one of:
            - "neg": numerical negation
            - "not": bitwise NOT
            - "lnot": logical NOT
    
    Returns:
        ARM64 assembly instruction string
    
    Raises:
        ValueError: If op is not a recognized unary operator
    """
    if op == "neg":
        return "neg x0, x0\n"
    elif op == "not":
        return "mvn x0, x0\n"
    elif op == "lnot":
        return "cmp x0, #0\ncset x0, eq\n"
    else:
        raise ValueError(f"Unknown unary operator: {op}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
