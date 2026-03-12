# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple node creation

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
def make_error_node(pos: int, tokens: list) -> dict:
    """
    Create an ERROR AST node for parse failure.
    
    Extracts line/column from tokens based on position priority:
    1. Last consumed token (tokens[pos - 1]) if pos > 0
    2. Current token (tokens[pos]) if available
    3. Default to line=0, column=0
    """
    line = 0
    column = 0
    
    # Priority 1: Use last consumed token
    if pos > 0 and pos <= len(tokens):
        token = tokens[pos - 1]
        line = token.get("line", 0)
        column = token.get("column", 0)
    # Priority 2: Use current token
    elif pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 0)
        column = token.get("column", 0)
    # Priority 3: Default values (already set)
    
    return {
        "type": "ERROR",
        "value": None,
        "children": [],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node