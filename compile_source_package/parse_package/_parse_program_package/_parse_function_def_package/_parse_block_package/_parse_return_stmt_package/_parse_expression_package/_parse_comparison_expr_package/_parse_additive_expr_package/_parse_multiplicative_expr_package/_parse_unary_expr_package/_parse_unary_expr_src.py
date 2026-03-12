# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

UNARY_OPERATORS = ["PLUS", "MINUS", "NOT"]

# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """Parse unary expression (handles unary operators like +, -, !)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if current token is a unary operator
    if pos < len(tokens) and tokens[pos]["type"] in UNARY_OPERATORS:
        op_token = tokens[pos]
        parser_state["pos"] = pos + 1
        
        # Parse operand recursively
        operand = _parse_unary_expr(parser_state)
        
        # Check if operand parsing succeeded
        if parser_state.get("error"):
            return {
                "type": "ERROR",
                "value": parser_state["error"],
                "children": [],
                "line": 0,
                "column": 0
            }
        
        return {
            "type": "UNARY_OP",
            "value": op_token["value"],
            "children": [operand],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    else:
        # Not a unary operator, parse primary expression
        return _parse_primary_expr(parser_state)

# === helper functions ===

# === OOP compatibility layer ===
