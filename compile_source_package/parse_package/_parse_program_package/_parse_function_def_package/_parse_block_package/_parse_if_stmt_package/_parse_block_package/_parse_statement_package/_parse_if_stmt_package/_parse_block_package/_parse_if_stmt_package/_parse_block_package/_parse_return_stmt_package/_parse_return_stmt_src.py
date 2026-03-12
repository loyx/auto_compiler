# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """
    解析 RETURN 语句。
    语法：'return' expression? ';'
    输入：parser_state（pos 指向 RETURN token）
    返回：RETURN AST 节点
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 检查是否有 RETURN token
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望 RETURN token，但已到达文件末尾")
    
    # 记录 RETURN token 的位置
    return_token = tokens[parser_state["pos"]]
    line = return_token["line"]
    column = return_token["column"]
    
    # 消费 RETURN token
    _consume_token(parser_state, "RETURN")
    
    # 检查是否有返回值表达式
    value = None
    if parser_state["pos"] < len(tokens):
        next_token = tokens[parser_state["pos"]]
        # 如果下一个 token 不是 SEMICOLON 或 RBRACE，则解析表达式
        if next_token["type"] not in ("SEMICOLON", "RBRACE"):
            value = _parse_expression(parser_state)
    
    # 消费可选的分号
    if parser_state["pos"] < len(tokens):
        if tokens[parser_state["pos"]]["type"] == "SEMICOLON":
            parser_state["pos"] += 1
    
    return {
        "type": "RETURN",
        "value": value,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
