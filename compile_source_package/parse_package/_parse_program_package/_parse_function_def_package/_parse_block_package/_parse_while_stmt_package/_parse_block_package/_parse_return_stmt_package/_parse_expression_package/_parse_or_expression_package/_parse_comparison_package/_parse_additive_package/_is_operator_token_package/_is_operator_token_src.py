# === std / third-party imports ===
from typing import Any, Dict, List, Optional

# === sub function imports ===
# (none - no subfunctions needed)

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

# === main function ===
def _is_operator_token(token: Optional[Token], operators: List[str]) -> bool:
    """Check if token is one of the specified operators.
    
    Args:
        token: Optional Token dictionary, or None if no token exists.
        operators: List of operator strings to check against (e.g., ['+', '-']).
    
    Returns:
        True if token exists and its value is in operators list, False otherwise.
    """
    if token is None:
        return False
    return token.get("value") in operators

# === helper functions ===
# (none needed - logic is simple enough)

# === OOP compatibility layer ===
# (not needed - this is a pure helper function, not a framework entry point)
