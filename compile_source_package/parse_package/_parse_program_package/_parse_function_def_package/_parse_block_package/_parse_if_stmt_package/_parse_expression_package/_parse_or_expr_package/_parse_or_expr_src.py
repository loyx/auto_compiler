# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
#   "value": Any,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """
    处理 || 逻辑或操作符（最低优先级）。
    左结合：a || b || c 解析为 ((a || b) || c)
    """
    left_node = _parse_and_expr(parser_state)
    
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        if current_token.get("type") != "OPERATOR" or current_token.get("value") != "||":
            break
        
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        parser_state["pos"] = pos + 1
        
        right_node = _parse_and_expr(parser_state)
        
        left_node = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": left_node,
            "right": right_node,
            "line": line,
            "column": column
        }
    
    return left_node

# === helper functions ===

# === OOP compatibility layer ===
