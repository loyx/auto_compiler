# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple conversion

# === ADT defines ===
# Re-defining shared types for self-documentation
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_number_value(value_str: str) -> Any:
    """
    Convert a numeric token value string to int or float.
    
    Algorithm:
    1. Check if value_str contains a decimal point "."
    2. If contains ".", return float(value_str)
    3. Otherwise, return int(value_str)
    
    Supports:
    - Integer strings: "0", "123", "-456"
    - Float strings: "3.14", "-0.5"
    
    Errors:
    - Raises ValueError if conversion fails (handled by caller)
    """
    if "." in value_str:
        return float(value_str)
    else:
        return int(value_str)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
