# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume a token of the expected type from the parser state.
    
    If the current token matches expected_type, increment pos and return the token.
    If pos is out of range or type mismatches, raise SyntaxError with location info.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        if tokens:
            last_token = tokens[-1]
            line = last_token.get("line", 1)
            column = last_token.get("column", 1)
        else:
            line = 1
            column = 1
        raise SyntaxError(f"{filename}:{line}:{column}: 期望 {expected_type}，但已到达文件末尾")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches
    if actual_type != expected_type:
        line = current_token.get("line", 1)
        column = current_token.get("column", 1)
        raise SyntaxError(f"{filename}:{line}:{column}: 期望 {expected_type}，但得到 {actual_type}")
    
    # Consume the token
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function