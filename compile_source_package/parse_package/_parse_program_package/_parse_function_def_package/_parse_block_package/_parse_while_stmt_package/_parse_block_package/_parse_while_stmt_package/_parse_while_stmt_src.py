# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_while_stmt(parser_state: dict) -> dict:
    """解析 while 语句，返回 WHILE_STMT 类型 AST 节点。"""
    # 1. 记录 WHILE 关键字位置
    token = _peek_token(parser_state)
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # 2. 消费 WHILE 关键字
    parser_state = _consume_token(parser_state, "WHILE")
    
    # 3. 消费 '('
    parser_state = _consume_token(parser_state, "LPAREN")
    
    # 4. 解析条件表达式
    condition = _parse_expression(parser_state)
    
    # 5. 消费 ')'
    parser_state = _consume_token(parser_state, "RPAREN")
    
    # 6. 解析循环体（语句块）
    body = _parse_block(parser_state)
    
    # 7. 返回 AST 节点
    return {
        "type": "WHILE_STMT",
        "children": [condition, body],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed; all logic delegated to child functions.

# === OOP compatibility layer ===
# No OOP wrapper needed; this is a parser function node.