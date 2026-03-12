# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._build_binary_op_package._build_binary_op_src import _build_binary_op

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
#   "operator": str,
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
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse expression: term (('+' | '-') term)*"""
    tokens = parser_state["tokens"]
    left = _parse_term(parser_state)
    
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token["type"] not in ("PLUS", "MINUS"):
            break
        parser_state["pos"] += 1
        right = _parse_term(parser_state)
        left = _build_binary_op(token, left, right)
    
    return left

# === helper functions ===
def _parse_term(parser_state: ParserState) -> AST:
    """Parse term: factor (('*' | '/') factor)*"""
    tokens = parser_state["tokens"]
    left = _parse_factor(parser_state)
    
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token["type"] not in ("STAR", "SLASH"):
            break
        parser_state["pos"] += 1
        right = _parse_factor(parser_state)
        left = _build_binary_op(token, left, right)
    
    return left

def _parse_factor(parser_state: ParserState) -> AST:
    """Parse factor: NUMBER | IDENTIFIER | '(' expression ')'"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of expression in {parser_state.get('filename', '<unknown>')}")
    
    token = tokens[pos]
    
    if token["type"] in ("NUMBER", "IDENTIFIER"):
        parser_state["pos"] += 1
        return {
            "type": token["type"],
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    if token["type"] == "LPAREN":
        parser_state["pos"] += 1
        expr = _parse_expression(parser_state)
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Unclosed parenthesis in {parser_state.get('filename', '<unknown>')}")
        close_token = tokens[parser_state["pos"]]
        if close_token["type"] != "RPAREN":
            raise SyntaxError(
                f"Expected ')' but got '{close_token['value']}' at line {close_token['line']}, "
                f"column {close_token['column']} in {parser_state.get('filename', '<unknown>')}"
            )
        parser_state["pos"] += 1
        return expr
    
    raise SyntaxError(
        f"Unexpected token '{token['value']}' (type: {token['type']}) at line {token['line']}, "
        f"column {token['column']} in {parser_state.get('filename', '<unknown>')}"
    )

# === OOP compatibility layer ===
# Not needed