# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this utility function

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
    Consume a token of expected type from parser state.
    
    Advances parser_state["pos"] on success, raises SyntaxError on mismatch.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if there are tokens remaining
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望 '{expected_type}'，但得到 'EOF'")
    
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches expected
    if actual_type != expected_type:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        raise SyntaxError(f"{filename}:{line}:{column}: 期望 '{expected_type}'，但得到 '{actual_type}'")
    
    # Token matches: advance position and return
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function