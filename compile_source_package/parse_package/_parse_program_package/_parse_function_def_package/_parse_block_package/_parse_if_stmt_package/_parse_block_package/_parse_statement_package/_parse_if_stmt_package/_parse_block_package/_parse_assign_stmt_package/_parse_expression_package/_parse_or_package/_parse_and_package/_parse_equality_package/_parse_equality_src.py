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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_equality(parser_state: ParserState) -> AST:
    """解析相等性表达式（优先级 Level 4）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（比较表达式）
    left_ast = _parse_comparison(parser_state)
    
    # 循环处理相等性运算符（左结合）
    while pos < len(tokens):
        token = tokens[pos]
        token_type = token.get("type", "")
        
        if token_type not in ("EQ", "NE"):
            break
        
        # 消耗运算符 token
        operator = token.get("value", "==")
        line = token.get("line", 0)
        column = token.get("column", 0)
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # 解析右侧操作数
        right_ast = _parse_comparison(parser_state)
        
        # 构建 BINARY AST 节点
        left_ast = {
            "type": "BINARY",
            "operator": operator,
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column
        }
        
        pos = parser_state["pos"]
    
    return left_ast

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function