# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_assignment_package._parse_assignment_src import _parse_assignment

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (uppercase string)
#   "value": str,            # token value
#   "line": int,             # line number
#   "column": int            # column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # node type (BINARY_OP, UNARY_OP, ASSIGNMENT, etc.)
#   "children": list,        # child nodes (for GROUPING)
#   "value": Any,            # node value (for literals, identifiers)
#   "op": str,               # operator (for BINARY_OP, UNARY_OP)
#   "left": AST,             # left operand (for BINARY_OP)
#   "right": AST,            # right operand (for BINARY_OP)
#   "operand": AST,          # operand (for UNARY_OP)
#   "name": str,             # variable name (for ASSIGNMENT)
#   "line": int,             # line number
#   "column": int            # column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position
#   "filename": str,         # source filename
#   "error": str             # error message (optional)
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """Parse a full expression (entry point).
    
    Delegates to _parse_assignment which is the lowest precedence level.
    Input: parser_state with pos at expression start.
    Output: AST node for the expression.
    Updates parser_state['pos'] past the expression.
    May set parser_state['error'] on failure.
    """
    return _parse_assignment(parser_state)

# === helper functions ===
# (Helpers are delegated to child functions that need them)

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
