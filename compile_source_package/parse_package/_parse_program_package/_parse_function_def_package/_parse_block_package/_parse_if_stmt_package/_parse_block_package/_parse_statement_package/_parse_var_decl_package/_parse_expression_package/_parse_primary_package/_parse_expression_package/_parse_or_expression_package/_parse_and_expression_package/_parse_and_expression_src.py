# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expression_package._parse_primary_expression_src import _parse_primary_expression
from ._consume_token_package._consume_token_src import _consume_token
from ._make_binary_op_package._make_binary_op_src import _make_binary_op

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
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
def _parse_and_expression(parser_state: ParserState) -> AST:
    """
    解析 AND 表达式（中等优先级）。
    这是递归下降解析的第二层，处理左结合的连续 AND 运算符。
    """
    # 1. 解析左侧 primary 表达式
    left = _parse_primary_expression(parser_state)
    if parser_state.get("error"):
        return left

    # 2. 循环处理 AND 运算符
    tokens = parser_state.get("tokens", [])
    while True:
        pos = parser_state.get("pos", 0)
        if pos >= len(tokens):
            break

        current_token = tokens[pos]
        if current_token.get("type") != "AND":
            break

        # 3. 记录 AND token 位置用于 AST
        and_line = current_token.get("line", 0)
        and_column = current_token.get("column", 0)

        # 4. 消费 AND token
        _consume_token(parser_state, "AND")
        if parser_state.get("error"):
            return left

        # 5. 解析右侧 primary 表达式
        right = _parse_primary_expression(parser_state)
        if parser_state.get("error"):
            return left

        # 6. 构建 binary_op AST 节点（左结合）
        left = _make_binary_op("and", left, right, and_line, and_column)

    return left


# === helper functions ===
# No helper functions needed; all logic is in main function.

# === OOP compatibility layer ===
# Not needed for this parser function.
