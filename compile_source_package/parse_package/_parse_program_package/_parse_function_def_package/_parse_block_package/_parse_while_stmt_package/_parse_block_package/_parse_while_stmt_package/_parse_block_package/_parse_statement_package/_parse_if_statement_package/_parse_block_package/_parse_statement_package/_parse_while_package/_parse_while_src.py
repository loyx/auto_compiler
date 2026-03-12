# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_until_colon_package._parse_expression_until_colon_src import _parse_expression_until_colon
from ._parse_inline_block_package._parse_inline_block_src import _parse_inline_block

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
def _parse_while(parser_state: dict) -> dict:
    """解析 WHILE 语句并返回 WHILE AST 节点。"""
    # 1. 消费 WHILE token
    while_token = _consume_token(parser_state, "WHILE")
    line = while_token["line"]
    column = while_token["column"]
    
    # 2. 解析条件表达式（直到遇到 COLON）
    condition = _parse_expression_until_colon(parser_state)
    
    # 3. 消费 COLON token
    colon_token = _peek_token(parser_state)
    if colon_token["type"] != "COLON":
        raise SyntaxError(f"Expected ':' after WHILE condition at line {line}, column {column}")
    _consume_token(parser_state, "COLON")
    
    # 4. 解析循环体（body）
    body = _parse_inline_block(parser_state)
    
    # 5. 返回 WHILE AST 节点
    return {
        "type": "WHILE",
        "condition": condition,
        "body": body,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions - all logic delegated to child nodes

# === OOP compatibility layer ===
# No wrapper needed for this parser function node
