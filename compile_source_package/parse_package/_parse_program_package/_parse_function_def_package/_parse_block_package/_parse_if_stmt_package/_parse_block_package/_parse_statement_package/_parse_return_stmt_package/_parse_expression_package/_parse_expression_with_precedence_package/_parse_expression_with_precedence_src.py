# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
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

# === main function ===
def _parse_expression_with_precedence(parser_state: ParserState, min_prec: int) -> AST:
    """
    Parse expression using Pratt Parsing algorithm with minimum precedence constraint.
    """
    # Binary operator precedence table
    _BINARY_PRECEDENCE = {
        "||": 1, "&&": 2, "|": 3, "^": 3, "&": 3,
        "==": 4, "!=": 4, "<": 4, ">": 4, "<=": 4, ">=": 4,
        "+": 5, "-": 5, "*": 6, "/": 6, "%": 6,
    }
    
    # Parse left operand (atomic expression)
    left = _parse_primary(parser_state)
    
    while True:
        token = _current_token(parser_state)
        
        # Exit if no token or not a binary operator
        if token is None:
            break
        
        op = token.get("value")
        if op not in _BINARY_PRECEDENCE:
            break
        
        prec = _BINARY_PRECEDENCE[op]
        
        # Exit if precedence is below minimum threshold
        if prec < min_prec:
            break
        
        # Consume the operator token
        _consume_token(parser_state)
        
        # Parse right operand with higher precedence (left-associative: prec + 1)
        right = _parse_expression_with_precedence(parser_state, prec + 1)
        
        # Build BINARY_OP AST node
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    return left

# === helper functions ===
# (No helper functions needed - all logic is in main function)

# === OOP compatibility layer ===
# (Not needed - this is a parser helper function, not a framework entry point)
