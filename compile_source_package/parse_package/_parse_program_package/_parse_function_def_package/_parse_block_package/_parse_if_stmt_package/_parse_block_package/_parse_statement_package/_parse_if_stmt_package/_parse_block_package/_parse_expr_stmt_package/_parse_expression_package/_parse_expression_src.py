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
#   "name": str,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "arguments": list,
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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse an expression starting at parser_state["pos"].
    Entry point for expression parsing with full operator precedence.
    Uses recursive descent parsing through precedence levels.
    """
    return _parse_or(parser_state)

# === helper functions ===
# No helper functions in this file; all logic delegated to precedence-level functions

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
