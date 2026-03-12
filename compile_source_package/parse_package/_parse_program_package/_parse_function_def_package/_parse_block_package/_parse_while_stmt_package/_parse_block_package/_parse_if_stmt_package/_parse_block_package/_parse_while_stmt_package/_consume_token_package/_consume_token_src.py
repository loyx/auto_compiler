# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this utility function

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
#   "tokens": list[Token],
#   "pos": int,
#   "filename": str,
#   "error": Optional[str]
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Optional[Token]:
    """
    Consume a token of expected type from the parser state.
    
    Args:
        parser_state: Parser state dictionary containing tokens, pos, filename, error
        expected_type: The expected token type to consume (e.g., "WHILE", "LPAREN")
    
    Returns:
        The consumed token dict if successful, None if type mismatch or end of tokens
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        parser_state["error"] = f"Unexpected end of input, expected {expected_type}"
        return None
    
    current_token = tokens[pos]
    
    # Check if token type matches expected type
    if current_token.get("type") != expected_type:
        token_type = current_token.get("type", "UNKNOWN")
        token_value = current_token.get("value", "")
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        parser_state["error"] = (
            f"Expected token type '{expected_type}' but got '{token_type}' "
            f"(value='{token_value}') at line {line}, column {column}"
        )
        return None
    
    # Token matches: consume it by incrementing pos
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
