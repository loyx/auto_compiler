# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this simple helper

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
def _match(parser_state: ParserState, token_type: str) -> bool:
    """
    Consume current token if it matches given type.
    
    Input: parser_state with tokens list and pos index; token_type string.
    Output: bool - True if matched and consumed, False otherwise.
    Side effect: Updates parser_state['pos'] if matched.
    """
    pos = parser_state['pos']
    tokens = parser_state['tokens']
    
    # Check bounds
    if pos >= len(tokens):
        return False
    
    # Check if current token matches token_type
    if tokens[pos]['type'] == token_type:
        parser_state['pos'] += 1
        return True
    
    return False

# === helper functions ===
# No additional helpers needed - logic is simple and inline

# === OOP compatibility layer ===
# Not needed for this helper function
