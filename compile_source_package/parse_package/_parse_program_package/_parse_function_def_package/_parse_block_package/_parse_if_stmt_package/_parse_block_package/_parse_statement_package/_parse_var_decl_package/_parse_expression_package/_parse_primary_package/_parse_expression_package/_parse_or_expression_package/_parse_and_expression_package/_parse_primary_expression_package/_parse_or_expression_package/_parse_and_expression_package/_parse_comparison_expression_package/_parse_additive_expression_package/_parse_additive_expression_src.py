# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expression_package._parse_multiplicative_expression_src import _parse_multiplicative_expression

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
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
def _parse_additive_expression(parser_state: ParserState) -> AST:
    """
    解析加法表达式（较低优先级）。
    处理 +, - 运算符，构建左结合的 binary_op AST 节点。
    """
    left = _parse_multiplicative_expression(parser_state)
    
    if parser_state.get("error"):
        return left
    
    while (
        parser_state["pos"] < len(parser_state["tokens"]) and
        parser_state["tokens"][parser_state["pos"]]["type"] == "OPERATOR" and
        parser_state["tokens"][parser_state["pos"]]["value"] in ("+", "-")
    ):
        op_token = parser_state["tokens"][parser_state["pos"]]
        parser_state["pos"] += 1
        
        right = _parse_multiplicative_expression(parser_state)
        
        if parser_state.get("error"):
            return left
        
        operator = "add" if op_token["value"] == "+" else "sub"
        left = {
            "type": "binary_op",
            "operator": operator,
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
