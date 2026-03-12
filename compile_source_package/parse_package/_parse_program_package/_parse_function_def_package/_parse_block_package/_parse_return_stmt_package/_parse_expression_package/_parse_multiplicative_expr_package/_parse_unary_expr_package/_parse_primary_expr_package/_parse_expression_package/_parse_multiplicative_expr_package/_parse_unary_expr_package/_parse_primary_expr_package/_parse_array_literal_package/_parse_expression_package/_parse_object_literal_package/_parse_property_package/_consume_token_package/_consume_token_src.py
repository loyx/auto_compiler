# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none - this is a leaf function)

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
    Consume a token of the expected type from the parser state.
    
    Mutates parser_state["pos"] by incrementing it on success.
    Raises ValueError if pos is out of bounds or token type doesn't match.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        raise ValueError(
            f"Unexpected end of input, expected {expected_type}"
        )
    
    current_token = tokens[pos]
    
    # Check if token type matches expected type
    if current_token["type"] != expected_type:
        raise ValueError(
            f"Expected {expected_type}, got {current_token['type']} "
            f"at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}"
        )
    
    # Consume the token by incrementing position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (none needed - this is a helper function, not a framework entry point)
