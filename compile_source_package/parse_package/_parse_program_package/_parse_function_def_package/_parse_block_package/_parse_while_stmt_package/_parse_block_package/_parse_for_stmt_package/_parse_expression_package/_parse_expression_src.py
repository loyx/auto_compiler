# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr
from ._parse_binop_tail_package._parse_binop_tail_src import _parse_binop_tail

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse an expression after 'in' keyword in for statements.
    Returns an AST node representing the iterable expression.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing expression"
        return {"type": "ERROR", "value": None, "line": 0, "column": 0, "children": []}
    
    expr_node = _parse_primary_expr(parser_state)
    expr_node = _parse_binop_tail(parser_state, expr_node)
    
    return expr_node

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not required - this is a parser helper function
