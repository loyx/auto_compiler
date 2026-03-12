# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (NUMBER, STRING, IDENTIFIER, KEYWORD, OPERATOR, etc.)
#   "value": str,            # token 值 (原始字符串)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, LITERAL, IDENTIFIER, ERROR, etc.)
#   "left": AST,             # 左操作数 (BINARY_OP)
#   "right": AST,            # 右操作数 (BINARY_OP)
#   "operator": str,         # 运算符字符串
#   "message": str,          # 错误消息 (ERROR)
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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """
    解析 or 表达式（最低优先级二元运算符）。
    
    使用循环处理左结合的 or 运算符，构建嵌套 BINARY_OP AST 节点。
    如果下层解析出错，直接透传 ERROR 节点。
    """
    left = _parse_and_expr(parser_state)
    
    # 如果下层已经出错，直接透传
    if left.get("type") == "ERROR":
        return left
    
    # 循环处理左结合的 or 运算符
    while True:
        if _is_at_end(parser_state):
            break
        
        token = _current_token(parser_state)
        if token["type"] == "KEYWORD" and token["value"] == "or":
            op_token = _consume_token(parser_state)
            right = _parse_and_expr(parser_state)
            
            # 如果右操作数出错，透传错误
            if right.get("type") == "ERROR":
                return right
            
            # 构建 BINARY_OP 节点（左结合）
            left = {
                "type": "BINARY_OP",
                "operator": "or",
                "left": left,
                "right": right,
                "line": op_token["line"],
                "column": op_token["column"]
            }
        else:
            break
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token。"""
    return parser_state["tokens"][parser_state["pos"]]

def _is_at_end(parser_state: ParserState) -> bool:
    """检查是否已到达 token 列表末尾。"""
    return parser_state["pos"] >= len(parser_state["tokens"])

def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时更新 pos。"""
    token = _current_token(parser_state)
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是纯函数式解析器节点
