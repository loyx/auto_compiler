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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, PAREN_EXPR, ERROR, etc.)
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


# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """Parse unary expressions (MINUS, NOT operators)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if position is out of range
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing unary expression"
        return {"type": "ERROR", "children": [], "value": None, "line": -1, "column": -1}
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_line = current_token.get("line", -1)
    token_column = current_token.get("column", -1)
    
    # Handle unary minus operator
    if token_type == "MINUS":
        parser_state["pos"] = pos + 1
        operand_ast = _parse_unary_expr(parser_state)
        if parser_state.get("error"):
            return operand_ast
        return {
            "type": "UNARY_OP",
            "children": [operand_ast],
            "value": "-",
            "line": token_line,
            "column": token_column
        }
    
    # Handle logical NOT operator
    elif token_type == "NOT":
        parser_state["pos"] = pos + 1
        operand_ast = _parse_unary_expr(parser_state)
        if parser_state.get("error"):
            return operand_ast
        return {
            "type": "UNARY_OP",
            "children": [operand_ast],
            "value": "!",
            "line": token_line,
            "column": token_column
        }
    
    # Handle other tokens by delegating to primary expression parser
    else:
        return _parse_primary_expr(parser_state)


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed - this is an internal parser function, not a framework entry point
