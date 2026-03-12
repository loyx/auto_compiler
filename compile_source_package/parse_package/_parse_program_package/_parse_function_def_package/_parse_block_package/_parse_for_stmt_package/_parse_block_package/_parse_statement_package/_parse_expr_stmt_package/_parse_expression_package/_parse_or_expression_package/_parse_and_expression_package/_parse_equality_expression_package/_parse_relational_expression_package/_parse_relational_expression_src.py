# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expression_package._parse_additive_expression_src import _parse_additive_expression

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
def _parse_relational_expression(parser_state: ParserState) -> AST:
    """Parse relational expression (<, >, <=, >=) with left-recursive elimination."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Parse left operand using additive expression
    left = _parse_additive_expression(parser_state)
    
    # Loop for relational operators
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token["value"] not in ("<", ">", "<=", ">="):
            break
        
        op = token["value"]
        line = token["line"]
        column = token["column"]
        parser_state["pos"] += 1
        
        # Parse right operand
        right = _parse_additive_expression(parser_state)
        
        # Build binary op node
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
