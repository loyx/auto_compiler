# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
#   "type": str,             # 表达式类型（如 BINARY_EXPR, IDENTIFIER, LITERAL 等）
#   "children": list,        # 子节点列表
#   "value": str,            # token 值
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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析表达式并返回 AST 节点。
    使用递归下降解析，支持运算符优先级。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of expression")
    
    # 解析左侧操作数
    left = _parse_primary(parser_state)
    
    # 处理二元运算符（按优先级顺序）
    while pos < len(tokens):
        token = tokens[pos]
        if token["type"] in ["PLUS", "MINUS", "STAR", "SLASH", "PERCENT"]:
            parser_state["pos"] += 1
            right = _parse_primary(parser_state)
            left = {
                "type": "BINARY_EXPR",
                "children": [left, right],
                "operator": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        else:
            break
    
    return left

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for this parser function node
