# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._consume_token_package._consume_token_src import _consume_token
from ._current_token_type_package._current_token_type_src import _current_token_type

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
#   "op": str,
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
def _parse_and(parser_state: ParserState) -> AST:
    """解析逻辑与表达式（较高优先级，低于一元表达式）。"""
    left = _parse_unary(parser_state)
    
    while _current_token_type(parser_state) == "AND":
        _consume_token(parser_state, "AND")
        right = _parse_unary(parser_state)
        left = {
            "type": "BINOP",
            "op": "&&",
            "left": left,
            "right": right,
            "line": left.get("line", 0),
            "column": left.get("column", 0)
        }
    
    return left

# === helper functions ===
# No helper functions needed; all logic delegated to child functions.

# === OOP compatibility layer ===
# Not needed for parser function nodes.
