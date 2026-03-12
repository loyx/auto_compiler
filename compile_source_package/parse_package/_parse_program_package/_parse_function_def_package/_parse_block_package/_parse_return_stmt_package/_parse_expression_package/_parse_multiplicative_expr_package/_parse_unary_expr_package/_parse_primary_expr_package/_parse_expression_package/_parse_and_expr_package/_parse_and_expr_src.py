# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr

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
    """Parse AND expression with left-associative binding."""
    left = _parse_comparison_expr(parser_state)
    
    while _is_and_keyword(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_comparison_expr(parser_state)
        left = _build_binary_op("AND", left, right, op_token)
    
    return left

# === helper functions ===
def _is_and_keyword(parser_state: ParserState) -> bool:
    """Check if current token is AND keyword."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token["type"] == "KEYWORD" and token["value"] == "AND"

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state['filename']}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

def _build_binary_op(operator: str, left: AST, right: AST, op_token: Token) -> AST:
    """Build BINARY_OP AST node."""
    return {
        "type": "BINARY_OP",
        "operator": operator,
        "children": [left, right],
        "line": op_token["line"],
        "column": op_token["column"]
    }

# === OOP compatibility layer ===
# Not needed for parser function
