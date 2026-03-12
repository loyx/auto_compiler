# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions

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
    
    Returns (token, updated_parser_state) if successful.
    Raises SyntaxError if token type doesn't match or end of input.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if position is beyond tokens range
    if pos >= len(tokens):
        raise SyntaxError(f"Syntax error at {filename}: unexpected end of input, expected {token_type}")
    
    # Get current token
    current_token = tokens[pos]
    
    # Check if token type matches
    if current_token["type"] != token_type:
        raise SyntaxError(
            f"Syntax error at {filename}:{current_token['line']}:{current_token['column']}: "
            f"expected {token_type}, got {current_token['type']}"
        )
    
    # Create updated state with pos incremented
    new_state: ParserState = {
        "tokens": tokens,
        "pos": pos + 1,
        "filename": filename,
        "error": parser_state.get("error", "")
    }
    
    return (current_token, new_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
