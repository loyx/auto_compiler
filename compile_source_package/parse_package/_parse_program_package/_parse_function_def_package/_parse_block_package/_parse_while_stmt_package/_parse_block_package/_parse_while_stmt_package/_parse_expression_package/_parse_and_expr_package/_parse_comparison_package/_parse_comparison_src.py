# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._peek_token_package._peek_token_src import _peek_token
from .._consume_token_package._consume_token_src import _consume_token
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
def _parse_comparison(parser_state: ParserState) -> tuple[AST, ParserState]:
    """解析 comparison 表达式（比较运算符：EQ, NE, LT, LE, GT, GE）。"""
    comparison_ops = {"EQ", "NE", "LT", "LE", "GT", "GE"}
    
    left_ast, parser_state = _parse_additive_expr(parser_state)
    
    while True:
        token = _peek_token(parser_state)
        if token is None or token["type"] not in comparison_ops:
            break
        
        op_token = _consume_token(parser_state)
        right_ast, parser_state = _parse_additive_expr(parser_state)
        
        left_ast = {
            "type": "BINARY_OP",
            "operator": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast, parser_state

# === helper functions ===
# No additional helper functions needed; logic is in main function.

# === OOP compatibility layer ===
# Not needed for parser function nodes.
