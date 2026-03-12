# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume current token and validate its type.
    
    Args:
        parser_state: Parser state dictionary containing tokens, pos, filename
        expected_type: Expected token type to validate against
    
    Returns:
        The consumed token dictionary
    
    Raises:
        ValueError: If current token type doesn't match expected_type
        IndexError: If parser_state has no more tokens
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if there are more tokens to consume
    if pos >= len(tokens):
        raise IndexError(
            f"Unexpected end of input at {parser_state.get('filename', 'unknown')}"
        )
    
    current_token = tokens[pos]
    
    # Validate token type
    if current_token["type"] != expected_type:
        raise ValueError(
            f"Expected token type '{expected_type}', "
            f"got '{current_token['type']}' at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}"
        )
    
    # Consume the token by advancing position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
