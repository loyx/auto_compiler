# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """
    解析加法表达式（+、-）。
    调用 _parse_multiplicative_expr 获取左侧操作数，然后循环检查后续 token
    是否为加法运算符。左结合性。
    """
    # Step 1: Get left operand from multiplicative expr
    left = _parse_multiplicative_expr(parser_state)
    
    # Step 2: Loop while current token is additive operator
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        
        # Check if token is additive operator
        if token.get("type") == "OPERATOR" and token.get("value") in ["+", "-"]:
            # Consume the operator token
            parser_state["pos"] = pos + 1
            op_token = token
            
            # Parse right operand
            right = _parse_multiplicative_expr(parser_state)
            
            # Build BINARY_OP node
            left = {
                "type": "BINARY_OP",
                "value": op_token["value"],
                "children": [left, right],
                "line": op_token["line"],
                "column": op_token["column"]
            }
            
            # Update position for next iteration
            pos = parser_state["pos"]
        else:
            # Not an additive operator, exit loop
            break
    
    return left


# === helper functions ===

# === OOP compatibility layer ===
