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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse complete expression with operator precedence.
    Entry point that delegates to lowest precedence parser (_parse_or).
    """
    return _parse_or(parser_state)

# === helper functions ===
# No helper functions in this file - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser function nodes
