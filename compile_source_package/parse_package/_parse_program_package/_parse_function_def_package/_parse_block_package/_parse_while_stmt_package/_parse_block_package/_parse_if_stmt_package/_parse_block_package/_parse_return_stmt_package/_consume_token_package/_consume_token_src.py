# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this helper

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
#   "filename": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str = None) -> Token:
    """
    Consume current token and advance parser position.
    
    Args:
        parser_state: Mutable parser state dict containing tokens, pos, filename
        expected_type: Optional token type constraint. If provided and current
                      token type doesn't match, raises SyntaxError.
    
    Returns:
        The consumed Token dict
    
    Raises:
        SyntaxError: If expected_type is provided and doesn't match current token type
    """
    current_token = parser_state["tokens"][parser_state["pos"]]
    
    if expected_type is not None and current_token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{current_token['type']}'"
        )
    
    parser_state["pos"] += 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function