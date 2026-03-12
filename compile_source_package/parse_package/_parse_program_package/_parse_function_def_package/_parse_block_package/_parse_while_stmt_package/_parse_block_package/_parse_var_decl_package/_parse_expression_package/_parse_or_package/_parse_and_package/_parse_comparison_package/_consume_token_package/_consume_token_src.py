# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No subfunctions needed

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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Tuple[Token, ParserState]:
    """
    Consume a token of the expected type from the parser state.
    
    Args:
        parser_state: Current parser state containing tokens, position, filename
        expected_type: The expected token type to consume
    
    Returns:
        Tuple of (consumed_token, updated_parser_state)
    
    Raises:
        SyntaxError: If token doesn't match expected type or EOF is reached
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        raise SyntaxError(f"Syntax error at {filename}:0:0: expected {expected_type}, got EOF")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches
    if actual_type != expected_type:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        raise SyntaxError(f"Syntax error at {filename}:{line}:{column}: expected {expected_type}, got {actual_type}")
    
    # Create updated parser state with incremented position
    updated_state = parser_state.copy()
    updated_state["pos"] = pos + 1
    
    return (current_token, updated_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
