# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_arithmetic_package._parse_arithmetic_src import _parse_arithmetic

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
def _parse_comparison(parser_state: dict) -> dict:
    """解析比较表达式（==、!=、<、>、<=、>=），左结合。"""
    # 先解析左操作数
    left_ast = _parse_arithmetic(parser_state)
    if parser_state.get("error"):
        return left_ast

    tokens = parser_state["tokens"]
    comparison_ops = ["==", "!=", "<", "<=", ">", ">="]

    # 循环检查比较运算符
    while True:
        pos = parser_state["pos"]
        if pos >= len(tokens):
            break

        current_token = tokens[pos]
        op_value = current_token.get("value")

        if op_value not in comparison_ops:
            break

        # 消耗运算符 token
        parser_state["pos"] += 1
        line_num = current_token.get("line", 0)
        col_num = current_token.get("column", 0)

        # 解析右操作数
        right_ast = _parse_arithmetic(parser_state)
        if parser_state.get("error"):
            return right_ast

        # 构建比较 AST 节点（左结合：之前的结果作为左操作数）
        left_ast = {
            "type": "COMPARE",
            "operator": op_value,
            "left": left_ast,
            "right": right_ast,
            "line": line_num,
            "column": col_num
        }

    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
