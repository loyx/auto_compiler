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
    """解析加法/减法表达式（+ 和 - 运算符）。"""
    left = _parse_multiplicative_expr(parser_state)
    
    if parser_state.get("error"):
        return left
    
    tokens = parser_state["tokens"]
    
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        token_type = current_token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        op_token = current_token
        parser_state["pos"] += 1
        
        right = _parse_multiplicative_expr(parser_state)
        
        if parser_state.get("error"):
            return left
        
        left = {
            "type": "BINARY_OP",
            "value": op_token.get("value", ""),
            "children": [left, right],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
