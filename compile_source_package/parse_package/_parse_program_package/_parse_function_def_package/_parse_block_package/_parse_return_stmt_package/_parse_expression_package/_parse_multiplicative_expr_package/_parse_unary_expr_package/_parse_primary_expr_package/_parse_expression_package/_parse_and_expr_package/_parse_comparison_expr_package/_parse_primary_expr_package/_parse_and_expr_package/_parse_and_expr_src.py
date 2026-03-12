# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """Parse AND expression: primary_expr ('&&' primary_expr)*"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Parse first primary expression
    left_ast = _parse_primary_expr(parser_state)
    
    # Check for && operators
    children = [left_ast]
    
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token.get("type") == "OPERATOR" and token.get("value") == "&&":
            # Consume && token
            parser_state["pos"] += 1
            # Parse next primary expression
            right_ast = _parse_primary_expr(parser_state)
            children.append(right_ast)
        else:
            break
    
    # Build AST node
    if len(children) == 1:
        return children[0]
    else:
        return {
            "type": "AND_EXPR",
            "children": children,
            "line": left_ast.get("line", 0),
            "column": left_ast.get("column", 0)
        }

# === helper functions ===

# === OOP compatibility layer ===
