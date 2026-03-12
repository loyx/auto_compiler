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
    Consume a token of expected type from the parser state.
    
    Modifies parser_state["pos"] in place to advance to next position.
    Returns the consumed token for caller to use its line/column info.
    Raises SyntaxError if token type doesn't match or end of input reached.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if position is out of range
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected {expected_type}")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches expected type
    if actual_type != expected_type:
        line = current_token["line"]
        column = current_token["column"]
        raise SyntaxError(f"{filename}:{line}:{column}: Expected {expected_type}, got {actual_type}")
    
    # Consume the token by advancing position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function