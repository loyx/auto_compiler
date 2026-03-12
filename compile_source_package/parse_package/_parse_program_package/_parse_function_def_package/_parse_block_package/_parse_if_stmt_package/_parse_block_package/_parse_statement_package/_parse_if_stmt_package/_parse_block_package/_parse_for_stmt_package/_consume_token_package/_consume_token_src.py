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
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume a token of the expected type from the parser state.
    
    Checks if the current token matches the expected type. If it matches,
    advances the position and returns the token. Otherwise raises SyntaxError.
    
    Side effect: modifies parser_state["pos"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if position is out of bounds
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected {expected_type}")
    
    # Get current token
    token = tokens[pos]
    
    # Check if token type matches expected type
    if token["type"] != expected_type:
        raise SyntaxError(
            f"{filename}:{token['line']}:{token['column']}: "
            f"Expected {expected_type}, got {token['type']}"
        )
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    # Return the consumed token
    return token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
