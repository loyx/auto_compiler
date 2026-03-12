# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expression_package._parse_and_expression_src import _parse_and_expression

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
#   "line": int,
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
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
def _parse_or_expression(parser_state: ParserState) -> AST:
    """
    解析 OR 表达式（最低优先级）。
    递归下降解析入口，处理括号内的完整表达式。
    """
    # 解析左侧 and_expression
    left_ast = _parse_and_expression(parser_state)
    
    # 若已有错误，直接返回
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理 OR 运算符（左结合）
    while _is_current_token_or(parser_state):
        or_token = _consume_current_token(parser_state)
        line = or_token.get("line", 0)
        column = or_token.get("column", 0)
        
        # 解析右侧 and_expression
        right_ast = _parse_and_expression(parser_state)
        
        # 若已有错误，直接返回
        if parser_state.get("error"):
            return left_ast
        
        # 构建二元运算 AST 节点
        left_ast = {
            "type": "binary_op",
            "operator": "or",
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column
        }
    
    return left_ast

# === helper functions ===
def _is_current_token_or(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 运算符。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "OR" or token.get("value", "").upper() == "OR"

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并推进位置。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    token = tokens[pos] if pos < len(tokens) else {}
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function