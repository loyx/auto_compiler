# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_logical(parser_state: ParserState) -> AST:
    """
    解析逻辑运算符表达式（AND, OR）。这是表达式解析的顶层入口函数。
    支持左结合性，运算符优先级最低。
    """
    # 1. 解析左侧操作数（比较表达式）
    left_ast = _parse_comparison(parser_state)
    
    # 2. 检查并处理逻辑运算符（左结合）
    while _has_logical_operator(parser_state):
        op_token = _consume_logical_operator(parser_state)
        right_ast = _parse_comparison(parser_state)
        
        # 构建 BinaryOp AST 节点
        left_ast = {
            "type": "BinaryOp",
            "op": op_token["value"].upper(),
            "left": left_ast,
            "right": right_ast,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
def _has_logical_operator(parser_state: ParserState) -> bool:
    """检查当前位置是否为逻辑运算符（AND/OR）。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    if pos >= len(tokens):
        return False
    
    token = tokens[pos]
    return token["type"] == "KEYWORD" and token["value"].upper() in ("AND", "OR")

def _consume_logical_operator(parser_state: ParserState) -> Token:
    """消费并返回逻辑运算符 token。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of expression")
    
    token = tokens[pos]
    if token["type"] != "KEYWORD" or token["value"].upper() not in ("AND", "OR"):
        raise SyntaxError(
            f"{filename}:{token['line']}:{token['column']}: "
            f"Expected AND or OR, got {token['value']}"
        )
    
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
