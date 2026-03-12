# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions required

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
def _consume_token(parser_state: ParserState, expected_type: str) -> None:
    """
    Consume a token if it matches the expected type.
    
    Modifies parser_state in place:
    - If current token matches expected_type: increment pos
    - If mismatch or end of input: set error message
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check boundary condition
    if pos >= len(tokens):
        parser_state["error"] = f"Expected {expected_type} at end of input"
        return
    
    current_token = tokens[pos]
    
    # Check token type match
    if current_token["type"] == expected_type:
        parser_state["pos"] += 1
    else:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        parser_state["error"] = f"Expected {expected_type} at line {line}, column {column}"

# === helper functions ===
# No helper functions required

# === OOP compatibility layer ===
# No OOP wrapper required for this utility function
