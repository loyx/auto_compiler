# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none - this is a leaf function in the dependency tree)

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
def _consume_token(parser_state: ParserState) -> Token:
    """
    Consume token at current position and advance pos.
    
    Input: parser_state with pos pointing to token to consume
    Output: consumed token dict (type, value, line, column)
    Side effect: mutates parser_state['pos'] += 1
    Exception: SyntaxError if pos exceeds tokens range
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(f"Unexpected end of input at {filename}")
    
    token = tokens[pos].copy()
    parser_state["pos"] = pos + 1
    return token

# === helper functions ===
# (none needed - function is atomic)

# === OOP compatibility layer ===
# (none needed - this is a helper function, not a framework entry point)
