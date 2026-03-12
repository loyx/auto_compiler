# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._get_precedence_package._get_precedence_src import _get_precedence
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_expression(parser_state: dict) -> dict:
    """
    解析表达式，使用 precedence climbing 算法处理运算符优先级。
    输入：parser_state（当前位置指向表达式起始 token）
    输出：表达式 AST 节点
    """
    return _parse_binary(parser_state, 0)

# === helper functions ===
def _parse_binary(parser_state: dict, min_precedence: int) -> dict:
    """
    使用 precedence climbing 解析二元表达式。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of expression")
    
    # 解析左侧操作数（先解析一元表达式）
    left = _parse_unary(parser_state)
    
    while True:
        pos = parser_state["pos"]
        if pos >= len(tokens):
            break
        
        token = tokens[pos]
        precedence = _get_precedence(token["type"], token["value"])
        
        if precedence < min_precedence:
            break
        
        # 左结合运算符
        next_precedence = precedence + 1
        
        # 消费运算符
        op_token = _consume_token(parser_state)
        
        # 解析右侧操作数
        right = _parse_binary(parser_state, next_precedence)
        
        # 构建二元运算节点
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === OOP compatibility layer ===
