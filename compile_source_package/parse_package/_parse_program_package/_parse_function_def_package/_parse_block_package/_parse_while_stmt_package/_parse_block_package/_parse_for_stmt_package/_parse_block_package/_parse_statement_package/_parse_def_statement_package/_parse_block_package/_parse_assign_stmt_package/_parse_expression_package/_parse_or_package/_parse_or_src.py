# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and
from ._expect_token_package._expect_token_src import _expect_token

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": AST,
#   "args": list,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_or(parser_state: ParserState) -> AST:
    """Parse OR expression (lowest precedence) with left-associativity."""
    left_ast = _parse_and(parser_state)
    
    while _current_token_is_or(parser_state):
        or_token = _expect_token(parser_state, "OR")
        right_ast = _parse_and(parser_state)
        
        left_ast = {
            "type": "BINOP",
            "op": "or",
            "left": left_ast,
            "right": right_ast,
            "line": or_token["line"],
            "column": or_token["column"],
            "children": [left_ast, right_ast]
        }
    
    return left_ast

# === helper functions ===
def _current_token_is_or(parser_state: ParserState) -> bool:
    """Check if current token is OR without consuming it."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    return tokens[pos]["type"] == "OR"

# === OOP compatibility layer ===
# Not needed for parser function node
