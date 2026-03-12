# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple accessor

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
def _current_token(parser_state: ParserState) -> Token:
    """
    Get the token at the current position in parser_state.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos index.
        
    Returns:
        The Token object at parser_state["pos"].
        
    Raises:
        SyntaxError: If pos is out of bounds (>= len(tokens) or < 0).
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos < 0 or pos >= len(tokens):
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(f"Unexpected end of input at {filename}:{pos}")
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this internal parser function
