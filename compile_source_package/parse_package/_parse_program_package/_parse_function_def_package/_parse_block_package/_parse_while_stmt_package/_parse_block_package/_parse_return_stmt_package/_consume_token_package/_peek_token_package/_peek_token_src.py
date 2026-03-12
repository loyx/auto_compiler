# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions required for this utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
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
def _peek_token(parser_state: dict) -> Optional[dict]:
    """
    Get the token at current position without advancing pos.
    
    Args:
        parser_state: Parser state dictionary with "tokens" list and "pos" int
        
    Returns:
        Token dict at current position, or None if at EOF
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required - this is a utility function, not a framework entry point
