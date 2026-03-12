# === std / third-party imports ===
from typing import Any, Dict, Tuple

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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, token_type: str) -> Tuple[Token, ParserState]:
    """
    Consume a token of specified type from the parser state.
    
    Returns (token, updated_parser_state) if the current token matches.
    Raises SyntaxError if the token type doesn't match or end of tokens.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        raise SyntaxError(
            f"Syntax error at {filename}: unexpected end of input, expected {token_type}"
        )
    
    current_token = tokens[pos]
    actual_type = current_token.get("type", "UNKNOWN")
    
    # Check if token type matches
    if actual_type != token_type:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        raise SyntaxError(
            f"Syntax error at {filename}:{line}:{column}: expected {token_type}, got {actual_type}"
        )
    
    # Token matches - create updated parser state with pos incremented
    updated_state = {
        "tokens": tokens,
        "pos": pos + 1,
        "filename": filename
    }
    if "error" in parser_state:
        updated_state["error"] = parser_state["error"]
    
    return (current_token, updated_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
