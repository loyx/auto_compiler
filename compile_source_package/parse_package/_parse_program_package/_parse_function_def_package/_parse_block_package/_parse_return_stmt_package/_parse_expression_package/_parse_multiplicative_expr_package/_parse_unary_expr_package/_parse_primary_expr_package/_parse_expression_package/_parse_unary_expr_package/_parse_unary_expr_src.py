# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: _parse_primary_expr is imported inside the function to avoid circular dependency

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

# === main function ===
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """Parse unary expressions (-, not)."""
    # Import here to avoid circular dependency
    from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing unary expression")
    
    current_token = tokens[pos]
    
    # Check if current token is a unary operator
    is_unary_op = (
        (current_token.get("type") == "OPERATOR" and current_token.get("value") == "-") or
        (current_token.get("type") == "KEYWORD" and current_token.get("value") == "not")
    )
    
    if is_unary_op:
        # Consume the operator token
        op_token = current_token
        parser_state["pos"] = pos + 1
        
        # Recursively parse the operand
        operand = _parse_unary_expr(parser_state)
        
        # Build UNARY_OP node
        return {
            "type": "UNARY_OP",
            "operator": op_token["value"],
            "children": [operand],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    else:
        # Not a unary operator, parse as primary expression
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function