# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions required for this helper

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (uppercase string)
#   "value": str,            # token value
#   "line": int,             # line number
#   "column": int            # column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position
#   "filename": str,         # source filename
#   "error": str             # error message (optional)
# }

# === main function ===
def _check(parser_state: ParserState, token_type: str) -> bool:
    """
    Check if current token matches given type without consuming.
    
    Lookahead helper for recursive descent parser.
    Returns True if current token exists and matches token_type.
    Returns False if at end of token stream or type mismatch.
    No side effects - does not modify parser_state.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if position is at or beyond end of tokens
    if pos >= len(tokens):
        return False
    
    # Compare current token type with expected type
    return tokens[pos]["type"] == token_type

# === helper functions ===
# No additional helper functions needed

# === OOP compatibility layer ===
# Not required - this is a pure helper function for parser internal use
