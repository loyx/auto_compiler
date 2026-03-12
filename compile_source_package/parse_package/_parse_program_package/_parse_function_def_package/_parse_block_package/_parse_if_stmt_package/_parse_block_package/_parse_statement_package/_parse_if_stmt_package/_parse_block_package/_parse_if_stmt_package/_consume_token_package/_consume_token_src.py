# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none)

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
    Consume a token of expected type from the parser state.
    
    Input: parser_state with pos pointing to current token, expected_type string.
    Output: the consumed token.
    Side effect: increments parser_state["pos"] by 1.
    Exception: raises SyntaxError if token type doesn't match or end of input.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if position is out of range (end of input)
    if pos >= len(tokens):
        # Use line 1, column 1 as default for end of input errors
        raise SyntaxError(f"{filename}:1:1: Unexpected end of input, expected {expected_type}")
    
    # Get current token
    token = tokens[pos]
    token_type = token["type"]
    
    # Check if token type matches expected type
    if token_type != expected_type:
        line = token["line"]
        column = token["column"]
        raise SyntaxError(f"{filename}:{line}:{column}: Expected {expected_type}, got {token_type}")
    
    # Consume the token by advancing position
    parser_state["pos"] = pos + 1
    
    return token

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (none needed for this helper function)
