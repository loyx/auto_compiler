# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed for this simple peek operation

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
def _peek_token(parser_state: ParserState) -> Optional[Token]:
    """
    Peek at the current token without consuming it.
    
    Args:
        parser_state: Parser state dictionary containing tokens and position
        
    Returns:
        Current token dictionary or None if at end of token stream
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function