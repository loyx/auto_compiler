# === std / third-party imports ===
from typing import Any, Dict

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
def _get_current_token(parser_state: ParserState) -> Token:
    """
    Get the token at the current position in parser state.
    
    Args:
        parser_state: Parser state containing tokens list and current position
        
    Returns:
        Current token dict, or EOF token if position is out of bounds
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if position is within valid range
    if pos < 0 or pos >= len(tokens):
        # Return EOF token when out of bounds
        return {
            "type": "EOF",
            "value": "",
            "line": 0,
            "column": 0
        }
    
    # Return the token at current position
    return tokens[pos]

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not required - this is a utility function, not a framework entry point
