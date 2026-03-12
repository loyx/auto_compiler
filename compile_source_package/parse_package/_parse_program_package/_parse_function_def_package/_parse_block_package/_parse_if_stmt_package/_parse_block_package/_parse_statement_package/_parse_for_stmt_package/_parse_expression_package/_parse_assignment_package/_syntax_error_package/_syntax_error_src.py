# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===

# === ADT defines ===
ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _syntax_error(parser_state: ParserState, message: str) -> None:
    """
    Report a syntax error and set parser_state['error'].
    
    Optionally enhances the error message with line/column information
    from the current token if available.
    """
    error_msg = message
    
    # Try to enrich error message with position info
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    filename = parser_state.get("filename", "")
    
    if tokens and 0 <= pos < len(tokens):
        current_token = tokens[pos]
        line = current_token.get("line", "?")
        col = current_token.get("col", "?")
        error_msg = f"{filename}:{line}:{col}: {message}" if filename else f"{line}:{col}: {message}"
    elif filename:
        error_msg = f"{filename}: {message}"
    
    parser_state["error"] = error_msg
    return None

# === helper functions ===

# === OOP compatibility layer ===
