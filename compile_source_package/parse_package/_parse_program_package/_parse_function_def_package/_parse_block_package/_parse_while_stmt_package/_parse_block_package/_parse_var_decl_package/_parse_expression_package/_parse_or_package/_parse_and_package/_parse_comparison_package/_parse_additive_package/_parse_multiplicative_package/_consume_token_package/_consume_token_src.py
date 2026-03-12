# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions for this helper utility

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
def _consume_token(parser_state: ParserState, token_type: str) -> Tuple[Token, ParserState]:
    """
    Consume a token of the specified type from the parser state.
    
    If the current token matches the expected type, return (token, updated_state).
    Otherwise, raise SyntaxError with detailed location information.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if we have a token at current position
    if pos >= len(tokens):
        # EOF case - use last token's position or default
        if tokens:
            last_token = tokens[-1]
            line = last_token.get("line", 0)
            column = last_token.get("column", 0)
        else:
            line = 0
            column = 0
        raise SyntaxError(
            f"Syntax error at {filename}:{line}:{column}: expected {token_type}, got EOF"
        )
    
    current_token = tokens[pos]
    actual_type = current_token.get("type", "UNKNOWN")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # Check if token type matches
    if actual_type != token_type:
        raise SyntaxError(
            f"Syntax error at {filename}:{line}:{column}: expected {token_type}, got {actual_type}"
        )
    
    # Token matches - consume it and advance position
    new_state = parser_state.copy()
    new_state["pos"] = pos + 1
    
    return (current_token, new_state)

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
