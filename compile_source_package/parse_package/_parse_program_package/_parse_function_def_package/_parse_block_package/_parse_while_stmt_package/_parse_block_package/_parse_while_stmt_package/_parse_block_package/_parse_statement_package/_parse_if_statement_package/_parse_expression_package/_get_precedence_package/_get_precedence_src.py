# === std / third-party imports ===
# No imports needed

# === sub function imports ===
# No child functions

# === ADT defines ===
# No ADT needed for this simple function
# Input: op_type (str) - operator token type value
# Output: int precedence level (3=highest, 0=non-operator)

# === main function ===
def _get_precedence(op_type: str) -> int:
    """
    Get operator precedence level.
    
    Input: operator token type string.
    Output: int precedence level (higher = binds tighter).
    No side effects. Returns 0 for non-operators.
    
    Precedence levels:
    - 3: MULTIPLY, DIVIDE, MODULO (* / %)
    - 2: PLUS, MINUS (+ -)
    - 1: EQ, NE, LT, GT, LE, GE (== != < > <= >=)
    - 0: all other tokens (non-operators)
    """
    if op_type in ("MULTIPLY", "DIVIDE", "MODULO"):
        return 3
    elif op_type in ("PLUS", "MINUS"):
        return 2
    elif op_type in ("EQ", "NE", "LT", "GT", "LE", "GE"):
        return 1
    else:
        return 0

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
