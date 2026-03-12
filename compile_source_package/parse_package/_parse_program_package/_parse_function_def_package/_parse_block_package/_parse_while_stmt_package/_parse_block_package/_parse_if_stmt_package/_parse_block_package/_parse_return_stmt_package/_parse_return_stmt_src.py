# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expr_package._parse_expr_src import _parse_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,          # 大写 token 类型，如 "RETURN", "SEMICOLON"
#   "value": str,         # token 原始文本
#   "line": int,          # 行号
#   "column": int         # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,          # 节点类型，如 "RETURN", "BINARY_OP"
#   "children": list,     # 子节点列表
#   "value": Any,         # 节点值（可选）
#   "line": int,          # 行号
#   "column": int         # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,       # Token 列表
#   "pos": int,           # 当前位置索引
#   "filename": str       # 源文件名
# }


# === main function ===
def _parse_return_stmt(parser_state: dict) -> dict:
    """
    解析 return 语句。
    
    语法：RETURN [表达式] SEMICOLON
    
    输入：parser_state（pos 指向 RETURN token）
    输出：RETURN 类型 AST 节点
    """
    # 确认当前 token 是 RETURN
    current_token = parser_state["tokens"][parser_state["pos"]]
    if current_token["type"] != "RETURN":
        raise SyntaxError(f"Expected RETURN token, got {current_token['type']}")
    
    # 记录 RETURN token 的位置
    line = current_token["line"]
    column = current_token["column"]
    
    # 消费 RETURN token
    _consume_token(parser_state, "RETURN")
    
    # 检查下一 token 是否为分号（无返回值情况）
    next_token = parser_state["tokens"][parser_state["pos"]]
    
    if next_token["type"] == "SEMICOLON":
        # return; 无返回值
        children = [None]
        _consume_token(parser_state, "SEMICOLON")
    else:
        # return expr; 有返回值
        expr_ast = _parse_expr(parser_state)
        children = [expr_ast]
        # 消费分号
        _consume_token(parser_state, "SEMICOLON")
    
    # 构建 RETURN AST 节点
    return {
        "type": "RETURN",
        "children": children,
        "line": line,
        "column": column
    }


# === helper functions ===
# No helper functions needed for this simple parsing logic


# === OOP compatibility layer ===
# Not needed for parser internal functions
