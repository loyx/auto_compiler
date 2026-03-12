# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

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
#   "value": Any,
#   "operator": str,
#   "left": AST,
#   "right": AST,
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
def _parse_term(parser_state: ParserState) -> AST:
    """
    解析 term 层级表达式，处理加减运算符。
    语法：term := factor ( ( "+" | "-" ) factor )*
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)

    # 先解析左侧 factor
    left_ast = _parse_factor(parser_state)

    # 检查是否有错误
    if parser_state.get("error"):
        return left_ast

    # 循环处理加减运算符
    while pos < len(tokens):
        token = tokens[pos]
        token_value = token.get("value", "")

        if token_value not in ("+", "-"):
            break

        # 记录运算符和位置
        operator = token_value
        line = token.get("line", 0)
        column = token.get("column", 0)

        # 前进 pos
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]

        # 解析右侧 factor
        right_ast = _parse_factor(parser_state)

        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast

        # 构建 Binary AST 节点
        left_ast = {
            "type": "Binary",
            "operator": operator,
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column
        }

        # 更新 pos 继续循环
        pos = parser_state.get("pos", 0)

    return left_ast


# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，若越界则返回空 token。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": 0, "column": 0}


# === OOP compatibility layer ===
# 本模块为函数依赖树节点，不需要 OOP wrapper
