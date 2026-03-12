# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_unary(parser_state: dict) -> dict:
    """
    解析一元表达式。
    
    输入：parser_state（当前位置指向可能的一元运算符或基本单元）
    输出：AST 节点（UNARY_OP 或基本单元）
    副作用：原地修改 parser_state["pos"]
    支持的一元运算符：-（负号）、!（逻辑非）
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查是否到达 token 末尾
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of expression at {filename}")
    
    token = tokens[pos]
    
    # 检查是否为一元运算符
    if token["type"] == "OPERATOR" and token["value"] in ("-", "!"):
        op_token = _consume_token(parser_state)
        # 一元运算符右结合，递归解析右侧表达式
        operand = _parse_unary(parser_state)
        
        return {
            "type": "UNARY_OP",
            "children": [operand],
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    else:
        # 不是 unary operator，解析基本单元
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
