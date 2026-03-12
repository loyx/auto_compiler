# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_and_expr(parser_state: ParserState) -> AST:
    """
    解析 AND 表达式（&& 运算符）。
    返回左结合的 BINARY_OP AST 节点。
    """
    # 解析左侧操作数
    left_ast = _parse_comparison_expr(parser_state)

    # 检查是否有错误
    if parser_state.get("error"):
        return left_ast

    # 循环解析 && 连接的操作数
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]

        # 检查是否还有 token
        if pos >= len(tokens):
            break

        current_token = tokens[pos]

        # 检查是否为 AND token
        if current_token.get("type") != "AND":
            break

        # 获取 AND token 的位置信息
        and_line = current_token.get("line", 0)
        and_column = current_token.get("column", 0)

        # 消费 AND token
        parser_state["pos"] = pos + 1

        # 解析右侧操作数
        right_ast = _parse_comparison_expr(parser_state)

        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast

        # 构建 BINARY_OP 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": "&&",
            "children": [left_ast, right_ast],
            "line": and_line,
            "column": and_column
        }

    return left_ast


# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
