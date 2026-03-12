# === std / third-party imports ===
from typing import Any, Dict

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

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume the current token and validate its type.
    
    Args:
        parser_state: Parser state dictionary containing tokens, pos, filename
        expected_type: The expected token type string
        
    Returns:
        The consumed token
        
    Raises:
        SyntaxError: When token is None or type doesn't match
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input: expected {expected_type}, "
            f"but no more tokens available"
        )
    
    current_token = tokens[pos]
    
    # Check if token is None
    if current_token is None:
        raise SyntaxError(
            f"Unexpected None token at position {pos}: "
            f"expected {expected_type}"
        )
    
    # Check if token type matches
    actual_type = current_token.get("type")
    if actual_type != expected_type:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise SyntaxError(
            f"Syntax error: expected {expected_type}, "
            f"got {actual_type} at line {line}, column {column}"
        )
    
    # Consume the token by incrementing position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function