# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """解析加法表达式（处理 + 和 - 运算符，左结合）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧操作数
    left_ast = _parse_unary_expr(parser_state)
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理 + 和 - 运算符
    while pos < len(tokens):
        token = tokens[pos]
        if token["type"] != "OPERATOR" or token["value"] not in ("+", "-"):
            break
        
        operator = token["value"]
        line = token["line"]
        column = token["column"]
        
        # 消费运算符 token
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # 解析右侧操作数
        right_ast = _parse_unary_expr(parser_state)
        if parser_state.get("error"):
            return right_ast
        
        # 构建 BINARY_OP AST 节点（左结合）
        left_ast = {
            "type": "BINARY_OP",
            "children": [left_ast, right_ast],
            "value": operator,
            "line": line,
            "column": column
        }
        
        pos = parser_state["pos"]
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function