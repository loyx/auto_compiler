# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed for this literal parser

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
def _parse_literal(parser_state: ParserState, token: Token) -> AST:
    """
    解析字面量 token 并返回对应 AST 节点。
    
    支持的字面量类型：NUMBER, STRING, TRUE, FALSE, NONE
    副作用：更新 parser_state["pos"] += 1
    """
    token_type = token["type"]
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # Parse value based on token type
    if token_type == "NUMBER":
        value_str = token["value"]
        if "." in value_str:
            value = float(value_str)
        else:
            value = int(value_str)
        ast_type = "NUMBER"
    elif token_type == "STRING":
        value = token["value"]
        ast_type = "STRING"
    elif token_type == "TRUE":
        value = True
        ast_type = "TRUE"
    elif token_type == "FALSE":
        value = False
        ast_type = "FALSE"
    elif token_type == "NONE":
        value = None
        ast_type = "NONE"
    else:
        raise ValueError(f"Unknown literal token type: {token_type}")
    
    # Update parser state position
    parser_state["pos"] = parser_state["pos"] + 1
    
    # Build and return AST node
    ast_node: AST = {
        "type": ast_type,
        "value": value,
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function