# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (INT_CONST)
#   "value": str,            # token value (original string from source)
#   "line": int,             # line number (1-based)
#   "column": int            # column number (1-based)
# }

# === main function ===
def _scan_number(source: str, pos: int, line: int, column: int, filename: str) -> tuple:
    """
    Scan an integer constant starting at pos.
    
    Input: source, pos, line, column, filename
    Output: tuple (token, new_pos, new_column)
    
    Scans consecutive decimal digits (0-9) and returns INT_CONST token.
    """
    start_pos = pos
    start_column = column
    
    # Scan consecutive decimal digits
    while pos < len(source) and source[pos].isdigit():
        pos += 1
        column += 1
    
    # Extract the digit string
    value = source[start_pos:pos]
    
    # Build token
    token: Token = {
        "type": "INT_CONST",
        "value": value,
        "line": line,
        "column": start_column
    }
    
    return (token, pos, column)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
