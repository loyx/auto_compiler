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
def _parse_additive_expression(parser_state: ParserState) -> AST:
    """
    解析加法表达式（+、-）。使用左递归消除后的循环结构。
    """
    # 先解析左操作数（乘法表达式）
    left = _parse_multiplicative_expression(parser_state)
    
    # 循环处理 + 和 - 运算符
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        if token["type"] != "OPERATOR" or token["value"] not in ("+", "-"):
            break
        
        # 记录运算符信息
        op = token["value"]
        line = token["line"]
        column = token["column"]
        
        # pos 前进
        parser_state["pos"] += 1
        
        # 解析右操作数（乘法表达式）
        right = _parse_multiplicative_expression(parser_state)
        
        # 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function
