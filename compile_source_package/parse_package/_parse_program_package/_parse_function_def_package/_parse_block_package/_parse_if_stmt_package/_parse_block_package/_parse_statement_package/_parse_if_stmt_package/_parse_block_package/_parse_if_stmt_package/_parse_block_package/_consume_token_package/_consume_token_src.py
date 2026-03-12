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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume a token of expected type from parser state.
    
    Checks if current token matches expected_type. If match, advances pos and returns token.
    If mismatch or EOF, raises SyntaxError with location information.
    
    Side effect: modifies parser_state["pos"]
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # Check bounds - EOF
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}: end of file: unexpected end of input")
    
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check type match
    if actual_type != expected_type:
        line = current_token["line"]
        column = current_token["column"]
        raise SyntaxError(
            f"{filename}:{line}:{column}: expected '{expected_type}', but got '{actual_type}'"
        )
    
    # Advance position and return consumed token
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
