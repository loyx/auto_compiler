# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple error-raising utility

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
def _raise_error(parser_state: ParserState, message: str) -> None:
    """
    Raise a SyntaxError exception with location information.
    
    Extracts position data from parser_state and constructs an error message
    containing filename, line, column, and the original message.
    """
    # Extract position information
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    filename = parser_state.get("filename", "")
    
    # Try to get location from current token
    line = None
    column = None
    if tokens and 0 <= pos < len(tokens):
        current_token = tokens[pos]
        line = current_token.get("line")
        column = current_token.get("column")
    
    # Build error message
    if filename and line is not None and column is not None:
        error_msg = f"{filename}:{line}:{column}: {message}"
    elif filename and line is not None:
        error_msg = f"{filename}:{line}: {message}"
    elif filename:
        error_msg = f"{filename}: {message}"
    else:
        error_msg = message
    
    # Raise the exception
    raise SyntaxError(error_msg)

# === helper functions ===
# No helper functions needed - logic is simple and self-contained

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a utility function, not a framework entry point
