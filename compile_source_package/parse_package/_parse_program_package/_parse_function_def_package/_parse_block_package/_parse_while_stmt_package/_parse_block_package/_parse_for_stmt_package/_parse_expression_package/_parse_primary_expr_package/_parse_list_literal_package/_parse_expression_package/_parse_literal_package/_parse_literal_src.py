# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions required for this leaf node

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
def _parse_literal(parser_state: ParserState) -> AST:
    """
    解析字面量值（数字、字符串、布尔值、None）。
    
    输入：parser_state（当前位置指向字面量 token）
    输出：LITERAL AST 节点，包含转换后的 value
    副作用：更新 parser_state["pos"] += 1（修改传入的 parser_state 字典）
    
    Resource IO:
    - 读：parser_state["tokens"], parser_state["pos"]
    - 写：parser_state["pos"]（直接修改传入的字典对象）
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    token = tokens[pos]
    
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    # Convert token value to appropriate Python type
    if token_type == "NUMBER":
        # Try int first, then float
        if "." in token_value:
            value = float(token_value)
        else:
            value = int(token_value)
    elif token_type == "STRING":
        # Remove quotes
        value = token_value[1:-1]
    elif token_type == "BOOLEAN":
        value = token_value == "true"
    elif token_type == "NONE":
        value = None
    else:
        # Should not happen per contract (caller ensures correct type)
        value = token_value
    
    # Create AST node
    ast_node: AST = {
        "type": "LITERAL",
        "value": value,
        "children": [],
        "line": line,
        "column": column
    }
    
    # Side effect: advance position
    parser_state["pos"] = pos + 1
    
    return ast_node

# === helper functions ===
# No helper functions needed for this simple leaf node

# === OOP compatibility layer ===
# Not required for this parser function node
