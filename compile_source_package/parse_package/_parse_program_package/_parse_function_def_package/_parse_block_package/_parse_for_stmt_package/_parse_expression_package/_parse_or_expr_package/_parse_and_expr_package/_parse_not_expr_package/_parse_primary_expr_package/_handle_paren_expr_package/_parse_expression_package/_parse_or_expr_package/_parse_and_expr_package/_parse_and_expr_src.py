# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
from ._parse_not_expr_package._parse_not_expr_src import _parse_not_expr

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """解析 and 表达式（比 or 更高优先级的二元运算符）。"""
    # 1. 首先获取左侧操作数（调用下一优先级层次）
    left = _parse_not_expr(parser_state)
    
    # 如果左侧已经是错误节点，直接透传
    if left.get("type") == "ERROR":
        return left
    
    # 2. 循环检查是否有 "and" 运算符（左结合）
    while True:
        token = _current_token(parser_state)
        if token is None:
            break
        
        # 检查是否为 KEYWORD 且 value 为 "and"
        if token.get("type") == "KEYWORD" and token.get("value") == "and":
            # 3. 消费 "and" token
            _consume_token(parser_state)
            
            # 4. 获取右侧操作数
            right = _parse_not_expr(parser_state)
            
            # 如果右侧是错误节点，直接透传
            if right.get("type") == "ERROR":
                return right
            
            # 5. 构建 BINARY_OP 节点
            left = {
                "type": "BINARY_OP",
                "left": left,
                "operator": "and",
                "right": right,
                "line": token.get("line", 0),
                "column": token.get("column", 0)
            }
        else:
            # 不是 "and" 运算符，结束循环
            break
    
    # 6. 返回最终 AST 节点
    return left


# === helper functions ===
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """获取当前位置的 token，如果已到末尾则返回 None。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return None
    return tokens[pos]


def _is_at_end(parser_state: ParserState) -> bool:
    """检查是否到达 token 列表末尾。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    return pos >= len(tokens)


def _consume_token(parser_state: ParserState) -> None:
    """消费当前 token 并更新 pos。"""
    parser_state["pos"] = parser_state.get("pos", 0) + 1


# === OOP compatibility layer ===
# Not needed for parser utility functions
