# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
#   "tokens": list[Token],
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_binary_expression(parser_state: ParserState, min_precedence: int = 0) -> AST:
    """Parse binary expressions using Pratt Parsing with operator precedence."""
    left = _parse_primary(parser_state)
    
    while True:
        if parser_state["pos"] >= len(parser_state["tokens"]):
            break
        
        token = parser_state["tokens"][parser_state["pos"]]
        op = token.get("value", "")
        precedence = _get_operator_precedence(op)
        
        if precedence < min_precedence:
            break
        
        parser_state["pos"] += 1
        right = _parse_binary_expression(parser_state, precedence + 1)
        
        left = {
            "type": "BINARY_OP",
            "op": op,
            "left": left,
            "right": right,
            "line": token.get("line"),
            "column": token.get("column")
        }
    
    return left

# === helper functions ===
def _get_operator_precedence(op: str) -> int:
    """Return precedence level for binary operator (0 if not recognized)."""
    precedence_map = {
        "||": 1, "or": 1,
        "&&": 2, "and": 2,
        "==": 3, "!=": 3,
        "<": 4, ">": 4, "<=": 4, ">=": 4,
        "+": 5, "-": 5,
        "*": 6, "/": 6, "%": 6,
        "^": 7, "**": 7,
    }
    return precedence_map.get(op, 0)

# === OOP compatibility layer ===
