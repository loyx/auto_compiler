# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    Parse multiplicative expressions (*, /, %, //).
    Consumes multiplicative operators and builds left-associative BINARY_OP nodes.
    """
    # Parse left operand
    left = _parse_unary_expr(parser_state)
    
    # Loop to handle multiplicative operators
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        # Check if current token is a multiplicative operator
        if token["type"] != "OPERATOR" or token["value"] not in ("*", "/", "%", "//"):
            break
        
        # Consume the operator token
        parser_state["pos"] += 1
        
        # Parse right operand
        right = _parse_unary_expr(parser_state)
        
        # Build binary operation node (left-associative)
        left = {
            "type": "BINARY_OP",
            "value": token["value"],
            "children": [left, right],
            "line": token["line"],
            "column": token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
