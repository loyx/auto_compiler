# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this atomic operation

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _get_current_token(parser_state: ParserState) -> Token:
    """Get the token at current parser position.
    
    Args:
        parser_state: Parser state containing tokens, pos, filename
        
    Returns:
        Token dict at current position
        
    Raises:
        IndexError: If pos is out of token range, with filename and position info
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    if pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise IndexError(f"Token index {pos} out of range in {filename}")
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed for this atomic operation

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
