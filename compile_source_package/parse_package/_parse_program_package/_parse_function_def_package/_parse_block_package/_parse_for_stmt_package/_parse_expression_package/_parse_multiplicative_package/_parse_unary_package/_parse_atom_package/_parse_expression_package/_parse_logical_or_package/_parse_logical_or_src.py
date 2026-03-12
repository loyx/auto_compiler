# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_and_package._parse_logical_and_src import _parse_logical_and

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
def _parse_logical_or(parser_state: ParserState) -> AST:
    """
    解析逻辑或表达式（OR 运算符）。
    实现左结合的 OR 运算解析。
    """
    # 先解析左侧表达式（AND 层级）
    left_node = _parse_logical_and(parser_state)
    
    # 检查是否有错误
    if parser_state.get('error'):
        return left_node
    
    # 循环处理多个 OR 运算符（左结合）
    while _current_token_is_or(parser_state):
        # 记录 OR token 位置
        or_token = _consume_current_token(parser_state)
        
        # 解析右侧表达式
        right_node = _parse_logical_and(parser_state)
        
        # 检查是否有错误
        if parser_state.get('error'):
            return right_node
        
        # 构建 BINARY_OP 节点
        left_node = {
            "type": "BINARY_OP",
            "children": [left_node, right_node],
            "value": "OR",
            "line": or_token.get("line", 0),
            "column": or_token.get("column", 0)
        }
    
    return left_node

# === helper functions ===
def _current_token_is_or(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 运算符。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token.get("type") == "OR" or current_token.get("value") == "or"

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    token = tokens[pos] if pos < len(tokens) else {}
    parser_state["pos"] = pos + 1
    
    return token

# === OOP compatibility layer ===
# Not needed for parser function nodes
