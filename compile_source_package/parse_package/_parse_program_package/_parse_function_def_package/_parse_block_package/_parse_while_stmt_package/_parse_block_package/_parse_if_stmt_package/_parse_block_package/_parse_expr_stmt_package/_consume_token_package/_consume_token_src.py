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
def _consume_token(parser_state: ParserState, token_type: str) -> bool:
    """
    Consume a token of the specified type.
    
    Args:
        parser_state: Parser state dictionary containing tokens, pos, filename
        token_type: Expected token type to consume (e.g., ";", "IDENT", "NUMBER")
    
    Returns:
        True if token was successfully consumed, False otherwise
    
    Behavior:
        1. Check if current token exists at parser_state["pos"]
        2. Check if token's type or value matches token_type
        3. If matches, increment parser_state["pos"] by 1
        4. Return match result (True/False)
    
    Constraints:
        - Directly modifies parser_state["pos"]
        - Does not set error field (silent failure)
        - Only returns boolean value
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if current position is within bounds
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    
    # Check if token matches (by type or value)
    token_matches = (
        current_token.get("type") == token_type or
        current_token.get("value") == token_type
    )
    
    if token_matches:
        parser_state["pos"] = pos + 1
        return True
    
    return False

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function