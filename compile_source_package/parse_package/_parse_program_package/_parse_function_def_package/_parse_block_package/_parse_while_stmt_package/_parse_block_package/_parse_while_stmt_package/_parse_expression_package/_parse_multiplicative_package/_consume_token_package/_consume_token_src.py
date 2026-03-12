# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none needed)

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
def _consume_token(parser_state: ParserState) -> Token:
    """
    Consume current token and advance position pointer.
    
    Check if parser_state['pos'] is out of tokens list range.
    If out of bounds, return None.
    Otherwise get token at tokens[pos], increment pos by 1, and return the token.
    
    Side effect: modifies parser_state['pos']
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return None
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (none needed - this is a helper function, not a framework entry point)
