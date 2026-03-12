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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# Binary operator set
BINARY_OPERATORS = {
    '+', '-', '*', '/', '//', '%',
    '==', '!=', '<', '>', '<=', '>=',
    '&&', '||', '&', '|', '^',
    '<<', '>>', '**'
}

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse complete expression with binary operators."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    # Parse left side (primary expression)
    left_ast = _parse_primary(parser_state)
    
    # Check for binary operators
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] != "OPERATOR" or current_token["value"] not in BINARY_OPERATORS:
            break
        
        op_token = current_token
        parser_state["pos"] += 1
        
        # Parse right side
        right_ast = _parse_primary(parser_state)
        
        # Create binary operation node
        left_ast = {
            "type": "BINOP",
            "children": [left_ast, right_ast],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
# No additional helper functions needed

# === OOP compatibility layer ===
# Not required for this parser function
