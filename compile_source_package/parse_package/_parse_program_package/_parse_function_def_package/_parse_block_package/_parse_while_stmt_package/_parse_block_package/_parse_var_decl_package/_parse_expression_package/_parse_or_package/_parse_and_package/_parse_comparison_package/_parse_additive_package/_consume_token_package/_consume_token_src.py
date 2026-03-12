# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none)

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
def _consume_token(parser_state: ParserState, token_type: str) -> ParserState:
    """
    Consume a token of the expected type from the parser state.
    
    If current token type matches, advance pos by 1 and return updated state.
    If mismatch or EOF, raise SyntaxError with detailed location info.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if pos is out of bounds (EOF)
    if pos >= len(tokens):
        raise SyntaxError(f"Syntax error at {filename}: expected {token_type}, got EOF")
    
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches
    if actual_type != token_type:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        raise SyntaxError(f"Syntax error at {filename}:{line}:{column}: expected {token_type}, got {actual_type}")
    
    # Token matches, advance position
    new_state = parser_state.copy()
    new_state["pos"] = pos + 1
    return new_state

# === helper functions ===
# (none)

# === OOP compatibility layer ===
# (none - this is a helper function, not a framework entry point)
