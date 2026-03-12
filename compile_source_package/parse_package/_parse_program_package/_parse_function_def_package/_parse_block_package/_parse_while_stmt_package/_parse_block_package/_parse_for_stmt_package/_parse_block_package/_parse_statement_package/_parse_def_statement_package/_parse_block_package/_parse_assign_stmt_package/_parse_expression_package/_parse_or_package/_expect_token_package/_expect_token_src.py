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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    Consume and validate the current token.
    
    Checks if the current token matches the expected type. If so, advances
    the parser position and returns the token. Otherwise raises SyntaxError.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if we've reached the end of input
    if pos >= len(tokens):
        # Get position info from last token if available, otherwise use 1, 1
        if tokens:
            line = tokens[-1]["line"]
            column = tokens[-1]["column"]
        else:
            line = 1
            column = 1
        raise SyntaxError(f"Unexpected end of input at line {line}, column {column}")
    
    # Get current token
    current_token = tokens[pos]
    
    # Check if token type matches
    if current_token["type"] != token_type:
        raise SyntaxError(
            f"Expected token type {token_type} but got {current_token['type']} "
            f"at line {current_token['line']}, column {current_token['column']}"
        )
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# (none)

# === OOP compatibility layer ===
# (none - this is a helper function, not a framework entry point)
