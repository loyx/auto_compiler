# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """解析加法表达式（处理 +, - 运算符，左结合）。"""
    left = _parse_multiplicative_expr(parser_state)
    
    while _is_additive_operator(parser_state):
        op_token = _consume_current_token(parser_state)
        right = _parse_multiplicative_expr(parser_state)
        left = _build_binary_op_node(op_token, left, right)
    
    return left

# === helper functions ===
def _is_additive_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为加法运算符（PLUS 或 MINUS）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    current_token = tokens[pos]
    return current_token.get("type") in ("PLUS", "MINUS")

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时推进 pos 指针。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

def _build_binary_op_node(op_token: Token, left: AST, right: AST) -> AST:
    """构建二元运算符 AST 节点。"""
    return {
        "type": "BINARY_OP",
        "value": op_token.get("value"),
        "children": [left, right],
        "line": op_token.get("line"),
        "column": op_token.get("column")
    }

# === OOP compatibility layer ===
