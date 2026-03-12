# === std / third-party imports ===
from typing import Dict, Any

# === sub function imports ===
# No sub functions needed for this simple operation

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
    """
    Advance parser position by incrementing pos field by 1.
    
    Args:
        parser_state: Parser state dictionary containing 'pos' field.
        
    Returns:
        None
        
    Side effect:
        Modifies parser_state['pos'] in-place.
        
    Note:
        Caller is responsible for ensuring pos does not exceed token bounds.
    """
    # Read current position
    current_pos = parser_state.get('pos', 0)
    
    # Increment position by 1
    parser_state['pos'] = current_pos + 1

# === helper functions ===
# No helper functions needed for this simple operation

# === OOP compatibility layer ===
# No OOP wrapper needed for this pure function