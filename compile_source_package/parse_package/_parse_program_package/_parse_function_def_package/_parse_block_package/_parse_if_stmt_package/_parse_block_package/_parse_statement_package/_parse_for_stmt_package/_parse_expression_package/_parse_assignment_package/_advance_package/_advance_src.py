# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple utility

# === ADT defines ===
ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _advance(parser_state: ParserState) -> None:
    """Advance the parser position by one token.
    
    Side effect: modifies parser_state['pos'] in-place.
    Boundary checking is the caller's responsibility.
    """
    parser_state['pos'] += 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function