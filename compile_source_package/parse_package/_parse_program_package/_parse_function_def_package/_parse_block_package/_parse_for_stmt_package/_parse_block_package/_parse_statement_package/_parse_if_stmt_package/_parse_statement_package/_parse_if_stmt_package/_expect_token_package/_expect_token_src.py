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
def _expect_token(parser_state: ParserState, expected_type: str) -> None:
    """
    Validate and consume the expected token.
    
    Resource IO: Reads and modifies parser_state['pos'] (GLOBAL_STATE)
    
    If current token type matches expected_type: consume it (pos += 1)
    If not matching: raise SyntaxError without modifying parser_state['error']
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we have a token at current position
    if pos >= len(tokens):
        raise SyntaxError(f"Expected '{expected_type}' but found end of input")
    
    current_token = tokens[pos]
    
    # Check if token type matches
    if current_token["type"] != expected_type:
        raise SyntaxError(
            f"Expected '{expected_type}' but found '{current_token['value']}' "
            f"at line {current_token['line']}, column {current_token['column']}"
        )
    
    # Consume the token (modifies parser_state['pos'])
    parser_state["pos"] = pos + 1


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this utility function
