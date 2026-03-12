# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_expression_with_precedence_package._parse_expression_with_precedence_src import (
    _parse_expression_with_precedence,
)
from ._current_token_package._current_token_src import _current_token
from ._consume_token_package._consume_token_src import _consume_token

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

# Binary operator precedence (higher = tighter binding)
_BINARY_PRECEDENCE: Dict[str, int] = {
    "||": 1,
    "&&": 2,
    "|": 3,
    "^": 3,
    "&": 3,
    "==": 4,
    "!=": 4,
    "<": 4,
    ">": 4,
    "<=": 4,
    ">=": 4,
    "+": 5,
    "-": 5,
    "*": 6,
    "/": 6,
    "%": 6,
}

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse an expression using Pratt Parsing algorithm.
    Input: parser_state with pos pointing to expression start token.
    Output: AST node for the expression.
    Side effect: Updates parser_state["pos"] to after the expression.
    """
    left = _parse_primary(parser_state)

    while True:
        token = _current_token(parser_state)
        if token is None:
            break

        op = token["value"]
        prec = _BINARY_PRECEDENCE.get(op)
        if prec is None:
            break

        _consume_token(parser_state)
        right = _parse_expression_with_precedence(parser_state, prec)
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": token["line"],
            "column": token["column"],
        }

    return left


# === helper functions ===
# No helper functions in this file; all delegated to child nodes

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
