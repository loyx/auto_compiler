# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（支持 *、/、% 运算符）。
    
    算法：
    1. 调用 _parse_unary_expr 解析左侧操作数
    2. 检查当前 token 是否为乘法运算符（MUL, DIV, MOD）
    3. 如果是：消费运算符 token，解析右侧操作数
    4. 构建 BINARY_OP 节点并返回
    5. 如果不是乘法运算符，直接返回左侧操作数的 AST
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧操作数（一元表达式）
    left = _parse_unary_expr(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left
    
    # 检查当前 token 是否为乘法运算符
    while pos < len(tokens):
        current_token = tokens[pos]
        token_type = current_token.get("type", "")
        
        if token_type not in ("MUL", "DIV", "MOD"):
            break
        
        # 消费运算符 token
        operator = current_token["value"]
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # 解析右侧操作数
        right = _parse_unary_expr(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": operator,
            "line": current_token.get("line", 0),
            "column": current_token.get("column", 0)
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
