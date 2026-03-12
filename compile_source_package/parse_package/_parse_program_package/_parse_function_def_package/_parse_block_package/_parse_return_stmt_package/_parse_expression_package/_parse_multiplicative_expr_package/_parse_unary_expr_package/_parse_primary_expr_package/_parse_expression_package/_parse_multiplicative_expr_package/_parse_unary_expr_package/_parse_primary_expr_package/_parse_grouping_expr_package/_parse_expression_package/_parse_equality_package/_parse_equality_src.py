# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_equality(parser_state: ParserState) -> AST:
    """Parse equality (==, !=) expressions."""
    tokens = parser_state["tokens"]
    
    left_ast = _parse_comparison(parser_state)
    
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token["value"] not in ("==", "!="):
            break
        
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Unexpected end of file after '{op_token['value']}' "
                f"in {parser_state.get('filename', 'unknown')}"
            )
        
        right_ast = _parse_comparison(parser_state)
        
        left_ast = {
            "type": "BINARY",
            "operator": op_token["value"],
            "left": left_ast,
            "right": right_ast,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function node