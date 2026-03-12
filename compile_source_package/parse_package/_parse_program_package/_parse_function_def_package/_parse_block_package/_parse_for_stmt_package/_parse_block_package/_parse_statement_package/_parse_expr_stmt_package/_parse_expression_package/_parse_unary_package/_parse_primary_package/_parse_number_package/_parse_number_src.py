# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple parser

# === ADT defines ===
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

# === main function ===
def _parse_number(token: Token) -> AST:
    """
    Parse NUMBER token into AST node.
    
    Converts token value to int or float based on decimal point presence.
    Returns AST node with type, value, line, and column.
    """
    value_str = token["value"]
    
    # Determine if value is int or float based on decimal point
    if "." in value_str:
        value = float(value_str)
    else:
        value = int(value_str)
    
    return {
        "type": "NUMBER",
        "value": value,
        "line": token["line"],
        "column": token["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
