# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """解析表达式语句：expr_stmt := expression SEMICOLON"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected expression")
    
    start_line = tokens[pos]["line"]
    start_column = tokens[pos]["column"]
    
    # 解析表达式
    expr_ast = _parse_expression(parser_state)
    
    # 消费 SEMICOLON
    _consume_token(parser_state, "SEMICOLON")
    
    return {
        "type": "EXPR_STMT",
        "line": start_line,
        "column": start_column,
        "children": [expr_ast]
    }

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
