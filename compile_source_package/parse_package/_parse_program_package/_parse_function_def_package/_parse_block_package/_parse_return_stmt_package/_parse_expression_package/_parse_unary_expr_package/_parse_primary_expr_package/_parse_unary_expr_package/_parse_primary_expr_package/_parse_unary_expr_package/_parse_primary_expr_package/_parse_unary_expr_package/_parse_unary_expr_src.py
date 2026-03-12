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
    """Parse unary expressions including unary operators and primary expressions."""
    # Check if we have tokens remaining
    if parser_state["pos"] >= len(parser_state["tokens"]):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "children": [], "value": None, "line": -1, "column": -1}
    
    token = parser_state["tokens"][parser_state["pos"]]
    
    # Define unary operator types
    unary_operators = {"MINUS", "PLUS", "NOT", "TILDE"}
    
    if token["type"] in unary_operators:
        # Consume the unary operator token
        operator_token = token
        parser_state["pos"] += 1
        
        # Recursively parse the operand (allows chained unary operators like ---x)
        operand = _parse_unary_expr(parser_state)
        
        # Return UNARY_OP AST node
        return {
            "type": "UNARY_OP",
            "children": [operand],
            "value": operator_token["value"],
            "line": operator_token["line"],
            "column": operator_token["column"]
        }
    else:
        # Not a unary operator, delegate to primary expression parser
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not needed for parser functions - this is a pure function node
