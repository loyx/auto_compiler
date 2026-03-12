# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
def _parse_break_stmt(parser_state: dict) -> dict:
    """
    解析 break 语句。
    
    语法格式：break ;
    输入：parser_state（pos 指向 BREAK token）
    输出：BREAK 类型 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取当前 BREAK token 的位置信息
    current_token = tokens[pos] if pos < len(tokens) else None
    line = current_token["line"] if current_token else 0
    column = current_token["column"] if current_token else 0
    
    # 消费 BREAK token
    parser_state = _consume_token(parser_state, "BREAK")
    
    # 检查是否有错误
    if parser_state.get("error"):
        return {
            "type": "ERROR",
            "children": [],
            "value": parser_state["error"],
            "line": line,
            "column": column
        }
    
    # 检查并消费分号（如果有）
    new_pos = parser_state["pos"]
    if new_pos < len(tokens) and tokens[new_pos]["type"] == "SEMICOLON":
        parser_state = _consume_token(parser_state, "SEMICOLON")
    
    # 返回 BREAK AST 节点
    return {
        "type": "BREAK",
        "children": [],
        "line": line,
        "column": column
    }

# === helper functions ===

# === OOP compatibility layer ===
