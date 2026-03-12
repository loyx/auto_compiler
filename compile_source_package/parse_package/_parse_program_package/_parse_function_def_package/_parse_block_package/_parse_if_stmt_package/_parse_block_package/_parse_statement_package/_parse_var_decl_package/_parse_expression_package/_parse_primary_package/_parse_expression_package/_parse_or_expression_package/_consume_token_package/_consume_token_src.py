# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume current token if it matches expected type.
    
    Resource IO (GLOBAL_STATE - DIRECT_RESOURCE_RW):
    - READ: parser_state["tokens"], parser_state["pos"]
    - WRITE: parser_state["pos"] (increment on success), parser_state["error"] (on failure)
    
    Side effects: modifies parser_state["pos"] or parser_state["error"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we've reached end of input
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    current_token = tokens[pos]
    
    # Check if token type matches expected
    if current_token["type"] == expected_type:
        parser_state["pos"] = pos + 1
        return current_token
    else:
        parser_state["error"] = f"Expected {expected_type} but got {current_token['type']}"
        return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
