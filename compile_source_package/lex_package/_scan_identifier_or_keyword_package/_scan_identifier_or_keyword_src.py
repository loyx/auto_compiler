# === std / third-party imports ===
from typing import Any, Dict, Set, Tuple

# === sub function imports ===
# No child functions

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (KEYWORD_*, IDENTIFIER)
#   "value": str,            # token value (original string from source)
#   "line": int,             # line number (1-based)
#   "column": int            # column number (1-based)
# }

# === main function ===
def _scan_identifier_or_keyword(source: str, pos: int, line: int, column: int, filename: str) -> Tuple[Token, int, int]:
    """
    Scan an identifier or keyword starting at pos.
    
    Reads consecutive letters, digits, and underscores until a non-identifier
    character is encountered. Checks if the extracted string is a C keyword.
    
    Returns: tuple (token, new_pos, new_column)
    """
    keywords: Set[str] = {
        "int", "char", "if", "else", "while", "for", "return", "break", "continue"
    }
    
    start_pos = pos
    start_column = column
    
    # Scan identifier characters: letters, digits, underscores
    while pos < len(source):
        ch = source[pos]
        if ch.isalnum() or ch == '_':
            pos += 1
            column += 1
        else:
            break
    
    # Extract the identifier string
    identifier = source[start_pos:pos]
    
    # Determine token type
    if identifier in keywords:
        token_type = f"KEYWORD_{identifier.upper()}"
    else:
        token_type = "IDENTIFIER"
    
    # Build token
    token: Token = {
        "type": token_type,
        "value": identifier,
        "line": line,
        "column": start_column
    }
    
    return (token, pos, column)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function node
