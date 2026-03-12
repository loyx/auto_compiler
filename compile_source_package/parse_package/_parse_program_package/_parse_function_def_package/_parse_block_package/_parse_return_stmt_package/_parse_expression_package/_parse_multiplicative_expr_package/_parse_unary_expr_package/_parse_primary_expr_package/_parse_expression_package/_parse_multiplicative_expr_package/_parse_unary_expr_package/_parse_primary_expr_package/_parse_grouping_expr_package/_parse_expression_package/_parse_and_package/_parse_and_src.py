# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality

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
#   "operator": str,
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
    """Parse logical AND (&&) expressions."""
    tokens = parser_state["tokens"]
    
    # Parse left operand at equality precedence
    left_ast = _parse_equality(parser_state)
    
    # Loop to chain && operators (left-associative)
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # Check if current token is && operator
        if current_token.get("type") != "OPERATOR" or current_token.get("value") != "&&":
            break
        
        # Record operator position before consuming
        op_line = current_token["line"]
        op_column = current_token["column"]
        parser_state["pos"] += 1
        
        # Parse right operand at equality precedence
        right_ast = _parse_equality(parser_state)
        
        # Build binary AST node for && operation
        left_ast = {
            "type": "BINARY",
            "operator": "&&",
            "left": left_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed; logic is straightforward

# === OOP compatibility layer ===
# Not needed for parser subfunction