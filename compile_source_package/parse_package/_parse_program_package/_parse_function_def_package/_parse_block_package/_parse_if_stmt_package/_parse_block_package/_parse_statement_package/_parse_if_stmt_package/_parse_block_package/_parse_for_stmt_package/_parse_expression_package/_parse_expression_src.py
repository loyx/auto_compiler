# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_assignment_package._parse_assignment_src import _parse_assignment

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
def _parse_expression(parser_state: dict) -> dict:
    """Parse C-style expression with proper operator precedence."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        _raise_error(parser_state, "Unexpected end of expression")
    
    # Parse expression starting with assignment (lowest precedence)
    result = _parse_assignment(parser_state)
    return result

# === helper functions ===
def _raise_error(parser_state: dict, message: str) -> None:
    """Raise SyntaxError with location information."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 0)
        column = token.get("column", 0)
    else:
        line = 0
        column = 0
    
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

def _get_current_token(parser_state: dict) -> dict:
    """Get current token at parser_state['pos']."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": 0, "column": 0}

# === OOP compatibility layer ===
