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
def _parse_expr(parser_state: ParserState) -> AST:
    """
    Parse expression using recursive descent with operator precedence.
    Entry point: starts from lowest precedence (OR) and works down to atomic.
    """
    return _parse_or(parser_state)

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed - this is a pure function node
