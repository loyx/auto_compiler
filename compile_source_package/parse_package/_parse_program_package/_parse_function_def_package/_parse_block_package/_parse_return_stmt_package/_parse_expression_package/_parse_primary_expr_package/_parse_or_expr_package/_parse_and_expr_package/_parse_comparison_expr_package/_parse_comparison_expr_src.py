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
    """
    解析比较表达式（如 a > b, x == y, foo <= bar 等）。
    
    算法：
    1. 调用 _parse_additive_expr 解析左侧操作数
    2. 检查当前 token 是否为比较运算符（GT, LT, GE, LE, EQ, NE）
    3. 如果是：消费运算符 token，调用 _parse_additive_expr 解析右侧操作数
    4. 构建 BINARY_OP 节点并返回
    5. 如果不是比较运算符，直接返回左侧操作数的 AST
    """
    # 比较运算符集合
    COMPARISON_OPS = {"GT", "LT", "GE", "LE", "EQ", "NE"}
    
    # 1. 解析左侧操作数
    left_ast = _parse_additive_expr(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return left_ast
    
    # 2. 检查当前 token 是否为比较运算符
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return left_ast
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # 3. 如果是比较运算符
    if token_type in COMPARISON_OPS:
        # 消费运算符 token
        parser_state["pos"] = pos + 1
        
        # 解析右侧操作数
        right_ast = _parse_additive_expr(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return left_ast
        
        # 4. 构建 BINARY_OP 节点
        operator_value = current_token.get("value", "")
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        return {
            "type": "BINARY_OP",
            "children": [left_ast, right_ast],
            "value": operator_value,
            "line": line,
            "column": column
        }
    
    # 5. 不是比较运算符，直接返回左侧操作数
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function