# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Using lazy import to avoid circular dependency
_parse_additive_expr = None

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
def _parse_comparison_expr(parser_state: ParserState) -> AST:
    """
    解析比较表达式（<, >, <=, >=, ==, !=）。
    调用 _parse_additive_expr 获取左右操作数，构建 BINARY_OP AST 节点。
    不支持链式比较，遇到一个比较运算符后即返回。
    """
    # 获取左操作数
    left = _parse_additive_expr(parser_state)
    
    # 如果左操作数解析出错，直接返回
    if parser_state.get("error") is not None:
        return left
    
    # 检查当前 token 是否为比较运算符
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return left
    
    current_token = tokens[pos]
    comparison_types = {"LT", "GT", "LE", "GE", "EQ", "NE"}
    
    if current_token.get("type") not in comparison_types:
        return left
    
    # 消费比较运算符 token
    op_symbol = current_token.get("value", "")
    op_line = current_token.get("line", 0)
    op_column = current_token.get("column", 0)
    parser_state["pos"] = pos + 1
    
    # 获取右操作数
    right = _parse_additive_expr(parser_state)
    
    # 如果右操作数解析出错，直接返回
    if parser_state.get("error") is not None:
        return right
    
    # 构建 BINARY_OP 节点
    return {
        "type": "BINARY_OP",
        "value": op_symbol,
        "children": [left, right],
        "line": op_line,
        "column": op_column
    }

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
