# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple utility

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
#   "tokens": list[Token],
#   "pos": int,
#   "filename": str,
#   "error": str (optional)
# }

# === main function ===
def _consume_token(parser_state: ParserState, token_type: str) -> ParserState:
    """
    Consume a token of specified type from parser state.
    
    Args:
        parser_state: Current parser state containing tokens, pos, filename, error
        token_type: Expected token type to consume (e.g., "BREAK", "SEMICOLON")
    
    Returns:
        Updated parser_state with pos advanced by 1, or error set if mismatch
    
    Constraints:
        - Does not modify input tokens list
        - Only updates pos and possible error field
        - Returns the parser_state dict (may be in-place modified)
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if current token exists
    if pos >= len(tokens):
        parser_state["error"] = f"Unexpected end of tokens, expected {token_type}"
        return parser_state
    
    current_token = tokens[pos]
    
    # Check if current token type matches expected type
    if current_token.get("type") == token_type:
        # Match: advance position and clear any existing error
        parser_state["pos"] = pos + 1
        if "error" in parser_state:
            del parser_state["error"]
        return parser_state
    else:
        # Mismatch: set error
        actual_type = current_token.get("type", "UNKNOWN")
        parser_state["error"] = f"Expected token type {token_type}, got {actual_type}"
        return parser_state

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
