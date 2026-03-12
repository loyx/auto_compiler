# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """
    Parse OR expression (lowest precedence).
    Consumes OR tokens and builds left-associative BINARY_OP nodes.
    """
    left = _parse_and_expr(parser_state)
    
    while _is_or_keyword(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_and_expr(parser_state)
        left = {
            "type": "BINARY_OP",
            "operator": "OR",
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left


# === helper functions ===
def _is_or_keyword(parser_state: ParserState) -> bool:
    """Check if current token is OR keyword."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token["type"] == "KEYWORD" and token["value"] == "OR"


def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state['filename']}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token
