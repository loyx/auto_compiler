# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and

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
def _parse_or(parser_state: ParserState) -> AST:
    """
    解析 OR 表达式（优先级最低，Level 6）。
    支持左结合的多个 OR 操作。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（AND 表达式）
    left_ast = _parse_and(parser_state)
    
    # 循环处理多个 OR（左结合）
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token.get("type") != "OR":
            break
        
        # 记录 OR 运算符位置
        or_line = current_token.get("line", 0)
        or_column = current_token.get("column", 0)
        
        # 消耗 OR token
        parser_state["pos"] += 1
        
        # 解析右侧操作数（AND 表达式）
        right_ast = _parse_and(parser_state)
        
        # 构建 BINARY AST 节点
        left_ast = {
            "type": "BINARY",
            "operator": "OR",
            "left": left_ast,
            "right": right_ast,
            "line": or_line,
            "column": or_column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes