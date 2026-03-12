# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expr_package._parse_expr_src import _parse_expr
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
    """
    解析 while 语句。
    
    语法格式：while (表达式) 语句块
    输入：parser_state（pos 指向 WHILE token）
    输出：WHILE 类型 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取 WHILE token 的位置信息
    while_token = tokens[pos]
    line = while_token.get("line", 0)
    column = while_token.get("column", 0)
    
    # 1. 消费 WHILE token
    _consume_token(parser_state, "WHILE")
    
    # 2. 消费 LPAREN（左圆括号）
    _consume_token(parser_state, "LPAREN")
    
    # 3. 解析条件表达式
    condition_ast = _parse_expr(parser_state)
    
    # 4. 消费 RPAREN（右圆括号）
    _consume_token(parser_state, "RPAREN")
    
    # 5. 解析语句块
    body_block_ast = _parse_block(parser_state)
    
    # 6. 返回 WHILE 节点
    return {
        "type": "WHILE",
        "children": [condition_ast, body_block_ast],
        "line": line,
        "column": column
    }

# === helper functions ===

# === OOP compatibility layer ===
