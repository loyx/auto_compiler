# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this utility function

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
    """
    Get the token at the current position in parser state.
    
    Args:
        parser_state: ParserState containing tokens list and current pos
        
    Returns:
        Token dict at the current position
        
    Raises:
        IndexError: If pos is out of range of tokens list
    """
    if parser_state["pos"] >= len(parser_state["tokens"]):
        raise IndexError(f"Position {parser_state['pos']} out of range")
    return parser_state["tokens"][parser_state["pos"]]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
