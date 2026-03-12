# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or

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
def _parse_expression(parser_state: dict) -> dict:
    """
    Parse an expression starting at the current position.
    Delegates to _parse_or as the entry point for precedence parsing.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for empty input
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input in expression")
    
    # Start parsing from the lowest precedence level
    result = _parse_or(parser_state)
    
    return result

# === helper functions ===
# No helper functions needed - all logic delegated to precedence-level parsers

# === OOP compatibility layer ===
# Not needed for this function node
