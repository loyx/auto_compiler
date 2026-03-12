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
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    Consume a token of expected type from parser state.
    
    Advances parser_state["pos"] on success. Raises SyntaxError on failure.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if pos is out of bounds (no more tokens)
    if pos >= len(tokens):
        line = tokens[-1]["line"] if tokens else 1
        column = tokens[-1]["column"] if tokens else 0
        error_msg = "Unexpected end of input"
        raise SyntaxError(error_msg, (filename, 1, line, column))
    
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches expected type
    if actual_type != token_type:
        line = current_token["line"]
        column = current_token["column"]
        error_msg = f"Expected {token_type}, got {actual_type}"
        raise SyntaxError(error_msg, (filename, 1, line, column))
    
    # Match successful: advance position and return token
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node