# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions delegated

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
#   "tokens": list,          # list of Token
#   "pos": int,              # current position in tokens
#   "filename": str,         # source filename
#   "error": str             # error message (if any)
# }

# === main function ===
def _expect_token(parser_state: ParserState, token_type: str) -> None:
    """
    Validate current token type matches expected value.
    
    If match: consume token (pos++)
    If no match: raise SyntaxError with detailed message
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check bounds
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of file, expected {token_type} at {filename}"
        )
    
    current_token = tokens[pos]
    actual_type = current_token.get("type", "<unknown>")
    
    # Check type match
    if actual_type != token_type:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise SyntaxError(
            f"Expected {token_type}, got {actual_type} "
            f"at {filename}:{line}:{column}"
        )
    
    # Consume token
    parser_state["pos"] = pos + 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
