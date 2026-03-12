# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._get_precedence_package._get_precedence_src import _get_precedence
from ._is_right_associative_package._is_right_associative_src import _is_right_associative

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_binary_op(parser_state: dict, left: dict, min_precedence: int) -> dict:
    """Parse binary operation expression using precedence climbing algorithm."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        if token["type"] not in _BINARY_OPERATORS:
            break
        
        op_type = token["type"]
        op_prec = _get_precedence(op_type)
        
        if op_prec < min_precedence:
            break
        
        parser_state["pos"] = pos + 1
        right = _parse_primary(parser_state)
        
        if right is None:
            filename = parser_state.get("filename", "unknown")
            line = token.get("line", 1)
            column = token.get("column", 1)
            raise SyntaxError(f"{filename}:{line}:{column}: Expected expression after operator")
        
        next_prec = _get_precedence(tokens[parser_state["pos"]]["type"]) if parser_state["pos"] < len(tokens) else 0
        next_min = op_prec if _is_right_associative(op_type) else op_prec + 1
        
        if next_prec > op_prec:
            right = _parse_binary_op(parser_state, right, next_min)
        
        left = {
            "type": "BINARY_OP",
            "operator": op_type,
            "left": left,
            "right": right,
            "line": left.get("line", token.get("line", 1)),
            "column": left.get("column", token.get("column", 1))
        }
        pos = parser_state["pos"]
    
    return left

# === helper functions ===
_BINARY_OPERATORS = {"OR", "AND", "EQ", "NEQ", "LT", "LTE", "GT", "GTE", "PLUS", "MINUS", "MUL", "DIV", "MOD", "POWER"}

# === OOP compatibility layer ===
# Not required for this parser function node
