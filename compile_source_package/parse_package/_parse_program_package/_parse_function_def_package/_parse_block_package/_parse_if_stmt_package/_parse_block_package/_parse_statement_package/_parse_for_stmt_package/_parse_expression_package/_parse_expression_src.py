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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """Parse expression with operator precedence (entry point)."""
    return _parse_assignment(parser_state)

# === helper functions ===
# No additional helpers - all delegated to sub-functions

# === OOP compatibility layer ===
# Not required for parser function node
