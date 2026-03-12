# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions required for this simple operation

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
    """Advance parser state to the next token position.
    
    Side effect: Directly modifies parser_state['pos'] by incrementing it.
    No boundary checking is performed - caller must ensure pos does not exceed tokens length.
    """
    parser_state['pos'] += 1

# === helper functions ===
# No helper functions needed for this simple operation

# === OOP compatibility layer ===
# Not required - this is a simple utility function, not a framework entry point
