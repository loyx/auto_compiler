# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility

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
def _peek_token(parser_state: ParserState) -> Token | None:
    """
    Get the current token without consuming it.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos pointer
        
    Returns:
        The current token dictionary at tokens[pos], or None if at EOF
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return None
    
    return dict(tokens[pos])

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function