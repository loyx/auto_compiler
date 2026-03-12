# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._peek_token_package._peek_token_src import _peek_token

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
#   "error": str | None
# }

# === main function ===
def _parse_return(parser_state: ParserState) -> AST:
    """
    解析 RETURN 语句并返回 RETURN AST 节点。
    原地修改 parser_state（推进 pos）。
    """
    return_token = _consume_token(parser_state, "RETURN")
    line = return_token["line"]
    column = return_token["column"]
    
    next_token = _peek_token(parser_state)
    
    if next_token is None:
        raise SyntaxError(f"Unexpected end of file after RETURN at line {line}, column {column}")
    
    expression = None
    if next_token["type"] != "SEMICOLON":
        expression = _parse_expression_inline(parser_state)
    
    _consume_token(parser_state, "SEMICOLON")
    
    return {
        "type": "RETURN",
        "expression": expression,
        "line": line,
        "column": column
    }

# === helper functions ===
def _parse_expression_inline(parser_state: ParserState) -> AST:
    """
    内联实现：解析表达式并返回 AST 节点。
    此处为简化实现，实际应委托给 _parse_expression 子函数。
    """
    token = _peek_token(parser_state)
    if token is None:
        raise SyntaxError(f"Unexpected end of file while parsing expression")
    
    _consume_token(parser_state)
    
    return {
        "type": "EXPRESSION",
        "value": token["value"],
        "line": token["line"],
        "column": token["column"],
        "children": []
    }

# === OOP compatibility layer ===
