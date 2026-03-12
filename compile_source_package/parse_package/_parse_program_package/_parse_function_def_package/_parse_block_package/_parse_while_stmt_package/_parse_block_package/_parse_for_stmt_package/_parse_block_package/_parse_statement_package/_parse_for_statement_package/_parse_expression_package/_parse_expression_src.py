# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "operator": str,
#   "left": dict,
#   "right": dict,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析表达式。输入：parser_state（pos 指向表达式起始 token）。
    输出：表达式 AST 节点。
    副作用：消费表达式全部 token，更新 pos。
    错误：表达式语法错误时抛 SyntaxError。
    """
    # 先解析 primary（标识符、字面量、括号、函数调用等）
    left = _parse_primary(parser_state)
    
    # 处理二元运算符（带优先级）
    result = _parse_binary_op(parser_state, 0, left)
    
    return result

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，若越界返回 None。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos < len(tokens):
        return tokens[pos]
    return None

# === OOP compatibility layer ===
