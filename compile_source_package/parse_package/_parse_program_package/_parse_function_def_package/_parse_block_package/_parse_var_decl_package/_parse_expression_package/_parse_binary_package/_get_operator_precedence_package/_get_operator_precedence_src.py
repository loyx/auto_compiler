# === std / third-party imports ===
from typing import Tuple

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
# No complex ADT needed, using standard Python types
# TokenPrecedence = Tuple[int, bool]
# TokenPrecedence possible fields:
# {
#   [0]: int - precedence level (higher = binds tighter)
#   [1]: bool - is_right_associative
# }

# === main function ===
def _get_operator_precedence(token_type: str) -> Tuple[int, bool]:
    """
    Get operator precedence and associativity for a given token type.
    
    Args:
        token_type: str - Operator token type (e.g., "PLUS", "STAR", "POWER")
    
    Returns:
        Tuple[int, bool]: (precedence, is_right_associative)
        - precedence: 0-70 (higher = binds tighter), 0 for non-operators
        - is_right_associative: True for right-associative operators
    
    Operator Precedence Table (low to high):
        10: Assignment (=, +=, -=, *=, /=, %=) - right associative
        20: Logical OR (||, or) - left associative
        30: Logical AND (&&, and) - left associative
        40: Comparison (==, !=, <, >, <=, >=, in, is) - left associative
        50: Additive (+, -) - left associative
        60: Multiplicative (*, /, %) - left associative
        70: Power (**) - right associative
    """
    # Precedence mapping: token_type -> (precedence, is_right_associative)
    OPERATOR_PRECEDENCE = {
        # Assignment operators (precedence 10, right associative)
        "EQUAL": (10, True),
        "PLUS_EQUAL": (10, True),
        "MINUS_EQUAL": (10, True),
        "STAR_EQUAL": (10, True),
        "SLASH_EQUAL": (10, True),
        "PERCENT_EQUAL": (10, True),
        
        # Logical OR (precedence 20, left associative)
        "OR": (20, False),
        "LOGICAL_OR": (20, False),
        
        # Logical AND (precedence 30, left associative)
        "AND": (30, False),
        "LOGICAL_AND": (30, False),
        
        # Comparison operators (precedence 40, left associative)
        "EQUAL_EQUAL": (40, False),
        "NOT_EQUAL": (40, False),
        "LESS": (40, False),
        "GREATER": (40, False),
        "LESS_EQUAL": (40, False),
        "GREATER_EQUAL": (40, False),
        "IN": (40, False),
        "IS": (40, False),
        
        # Additive operators (precedence 50, left associative)
        "PLUS": (50, False),
        "MINUS": (50, False),
        
        # Multiplicative operators (precedence 60, left associative)
        "STAR": (60, False),
        "SLASH": (60, False),
        "PERCENT": (60, False),
        
        # Power operator (precedence 70, right associative)
        "POWER": (70, True),
        "STAR_STAR": (70, True),
    }
    
    # Return precedence for known operators, default for non-operators
    return OPERATOR_PRECEDENCE.get(token_type, (0, False))

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
