# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality

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
def _parse_and(parser_state: ParserState) -> AST:
    """解析 AND 表达式（优先级 Level 5）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（更高优先级的相等性表达式）
    left_ast = _parse_equality(parser_state)
    
    # 循环处理多个 AND（左结合）
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token["type"] != "AND":
            break
        
        # 消耗 AND token
        and_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 解析右侧操作数
        right_ast = _parse_equality(parser_state)
        
        # 构建 BINARY AST 节点
        left_ast = {
            "type": "BINARY",
            "operator": "AND",
            "left": left_ast,
            "right": right_ast,
            "line": and_token.get("line", 0),
            "column": and_token.get("column", 0)
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not required for parser function nodes
