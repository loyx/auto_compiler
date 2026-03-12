# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
#   "left": Any,
#   "right": Any,
#   "operator": str,
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
def _parse_arithmetic(parser_state: ParserState) -> AST:
    """
    解析算术表达式（+、- 运算符），左结合。
    调用 _parse_term 获取操作数（_parse_term 处理更高优先级的 *、/、%）。
    原地更新 parser_state['pos'] 到表达式结束位置。
    若解析失败，设置 parser_state['error']。
    """
    # 先解析左操作数（调用 _parse_term 处理更高优先级的 * / %）
    left_ast = _parse_term(parser_state)
    if parser_state.get("error"):
        return left_ast

    tokens = parser_state["tokens"]
    arithmetic_ops = ["+", "-"]

    # 循环检查算术运算符
    while True:
        pos = parser_state["pos"]
        if pos >= len(tokens):
            break

        current_token = tokens[pos]
        op_value = current_token.get("value")

        if op_value not in arithmetic_ops:
            break

        # 消耗运算符 token
        parser_state["pos"] += 1
        line_num = current_token.get("line", 0)
        col_num = current_token.get("column", 0)

        # 解析右操作数
        right_ast = _parse_term(parser_state)
        if parser_state.get("error"):
            return right_ast

        # 构建算术 AST 节点（左结合）
        left_ast = {
            "type": "ARITHMETIC",
            "operator": op_value,
            "left": left_ast,
            "right": right_ast,
            "line": line_num,
            "column": col_num
        }

    return left_ast

# === helper functions ===
# No helper functions needed.

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function.
