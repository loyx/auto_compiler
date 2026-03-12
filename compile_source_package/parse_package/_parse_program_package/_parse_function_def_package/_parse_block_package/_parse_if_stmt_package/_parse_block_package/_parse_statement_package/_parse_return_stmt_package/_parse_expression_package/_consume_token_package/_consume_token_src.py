# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions - _current_token implemented as helper

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
def _consume_token(parser_state: ParserState) -> Optional[Token]:
    """
    Consume current token and advance position.
    
    Input: parser_state with tokens list and pos index
    Output: consumed Token dict or None if at end
    Side effect: increments parser_state["pos"] by 1
    Resource effect: reads parser_state["tokens"], parser_state["pos"]; writes parser_state["pos"]
    """
    current = _current_token(parser_state)
    if current is None:
        return None
    parser_state["pos"] += 1
    return current

# === helper functions ===
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """
    Get current token without advancing position.
    
    Input: parser_state with tokens list and pos index
    Output: Token dict at current pos or None if out of bounds
    Resource effect: reads parser_state["tokens"], parser_state["pos"]
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < 0 or pos >= len(tokens):
        return None
    return tokens[pos]

# === OOP compatibility layer ===
# Not needed - this is a helper function node