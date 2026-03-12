# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

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
def _expect_token(parser_state: dict, token_type: str, token_value: str = None) -> dict:
    """
    Validate and consume an expected token from the parser state.
    
    Resource IO:
    - READ: parser_state["tokens"], parser_state["pos"], parser_state["filename"]
    - WRITE: parser_state["pos"] (mutated in-place on success)
    
    Args:
        parser_state: Parser state dict containing tokens, pos, filename
        token_type: Expected token type (e.g., "KEYWORD", "IDENTIFIER")
        token_value: Optional expected token value; if None, only check type
    
    Returns:
        The consumed token dict
    
    Raises:
        SyntaxError: If token doesn't match or if pos is out of bounds
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if pos is within bounds
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input, expected {token_type} token" +
            (f" '{token_value}'" if token_value else "") +
            f" at {filename}:{pos}"
        )
    
    actual_token = tokens[pos]
    
    # Validate token type
    if actual_token["type"] != token_type:
        raise SyntaxError(
            f"Expected {token_type} token" +
            (f" '{token_value}'" if token_value else "") +
            f", got {actual_token.get('type')} '{actual_token.get('value')}' " +
            f"at {filename}:{actual_token.get('line')}:{actual_token.get('column')}"
        )
    
    # Validate token value if specified
    if token_value is not None and actual_token["value"] != token_value:
        raise SyntaxError(
            f"Expected {token_type} token '{token_value}', " +
            f"got {actual_token.get('type')} '{actual_token.get('value')}' " +
            f"at {filename}:{actual_token.get('line')}:{actual_token.get('column')}"
        )
    
    # Success: mutate state and return token
    parser_state["pos"] = pos + 1
    return actual_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
