# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """Parse primary expression (number, identifier, or parenthesized expression)."""
    if parser_state["pos"] >= len(parser_state["tokens"]):
        raise SyntaxError("Unexpected end of input")
    
    token = parser_state["tokens"][parser_state["pos"]]
    
    if token["type"] == "NUMBER":
        parser_state["pos"] += 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token["type"] == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token["type"] == "LPAREN":
        parser_state["pos"] += 1
        expr = _parse_expression(parser_state)
        
        if parser_state["pos"] >= len(parser_state["tokens"]):
            raise SyntaxError("Expected RPAREN but got end of input")
        
        rparen_token = parser_state["tokens"][parser_state["pos"]]
        if rparen_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected RPAREN but got {rparen_token['type']}")
        
        parser_state["pos"] += 1
        return expr
    
    else:
        raise SyntaxError(f"Unexpected token: {token['type']}")

# === helper functions ===

# === OOP compatibility layer ===
