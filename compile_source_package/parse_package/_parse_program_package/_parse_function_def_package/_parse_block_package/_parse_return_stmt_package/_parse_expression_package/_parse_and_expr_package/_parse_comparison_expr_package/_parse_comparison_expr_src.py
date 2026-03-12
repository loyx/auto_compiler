# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
    """解析比较表达式（处理 <, >, <=, >=, ==, !=）。"""
    # 1. 解析左操作数（加法表达式）
    left = _parse_additive_expr(parser_state)
    
    # 2. 检查是否越界
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos >= len(tokens):
        return left
    
    # 3. 检查当前 token 是否为比较运算符
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    comparison_ops = {"LESS", "GREATER", "LESS_EQ", "GREATER_EQ", "EQ", "NEQ"}
    if token_type not in comparison_ops:
        return left
    
    # 4. 消费比较运算符 token
    op_symbol = current_token.get("value", "")
    op_line = current_token.get("line", 0)
    op_column = current_token.get("column", 0)
    parser_state["pos"] = pos + 1
    
    # 5. 解析右操作数（加法表达式）
    right = _parse_additive_expr(parser_state)
    
    # 6. 构建 BINARY_OP 节点
    return {
        "type": "BINARY_OP",
        "value": op_symbol,
        "children": [left, right],
        "line": op_line,
        "column": op_column
    }

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
