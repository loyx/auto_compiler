# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# (no child functions)

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
def _previous(parser_state: ParserState) -> Optional[Token]:
    """
    Get the previously consumed token from parser state.
    
    Returns the token at position (pos - 1), or None if pos is 0
    (indicating no tokens have been consumed yet).
    
    No side effects - does not modify parser_state.
    """
    if parser_state['pos'] == 0:
        return None
    return parser_state['tokens'][parser_state['pos'] - 1]

# === helper functions ===
# (no helper functions needed)

# === OOP compatibility layer ===
# (not needed - this is a parser helper function, not a framework entry point)
