# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
#   "value": Any,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
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
def _parse_additive_expr(parser_state: dict) -> dict:
    """Parse additive expressions (+, - operators) with left associativity."""
    # Parse left operand (next priority level)
    left_node = _parse_multiplicative_expr(parser_state)
    
    # Loop for additive operators
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        # Check if current token is + or - operator
        if token["type"] == "OPERATOR" and token["value"] in ["+", "-"]:
            op_token = token
            parser_state["pos"] += 1  # consume operator
            
            # Parse right operand
            right_node = _parse_multiplicative_expr(parser_state)
            
            # Build binary op node
            left_node = {
                "type": "BINARY_OP",
                "operator": op_token["value"],
                "left": left_node,
                "right": right_node,
                "line": op_token["line"],
                "column": op_token["column"]
            }
        else:
            break
    
    return left_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
