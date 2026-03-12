# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expr_package._parse_expr_src import _parse_expr
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
def _parse_expr_stmt(parser_state: dict) -> dict:
    """解析表达式语句。
    
    语法格式：表达式 ;
    返回 EXPR_STMT 类型 AST 节点。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取起始位置信息
    start_line = tokens[pos]["line"] if pos < len(tokens) else 0
    start_column = tokens[pos]["column"] if pos < len(tokens) else 0
    
    # 解析表达式
    expr_ast = _parse_expr(parser_state)
    
    # 检查解析是否失败
    if parser_state.get("error"):
        return {
            "type": "EXPR_STMT",
            "children": [],
            "line": start_line,
            "column": start_column
        }
    
    # 消费分号（如果有）
    _consume_token(parser_state, ";")
    
    # 返回 EXPR_STMT 节点
    return {
        "type": "EXPR_STMT",
        "children": [expr_ast],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===
