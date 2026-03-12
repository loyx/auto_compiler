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
    """
    解析加法表达式（支持 + 和 - 运算符）。
    
    算法：
    1. 调用 _parse_multiplicative_expr 解析左侧操作数
    2. 检查当前 token 是否为加法运算符（ADD, SUB）
    3. 如果是：消费运算符 token，解析右侧操作数，构建 BINARY_OP 节点
    4. 如果不是加法运算符，直接返回左侧操作数的 AST
    """
    left = _parse_multiplicative_expr(parser_state)
    
    if parser_state.get("error"):
        return left
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        current_token = tokens[pos]
        
        if current_token["type"] not in ("ADD", "SUB"):
            break
        
        op_token = current_token
        parser_state["pos"] = pos + 1
        
        right = _parse_multiplicative_expr(parser_state)
        
        if parser_state.get("error"):
            return left
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
        
        pos = parser_state["pos"]
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
