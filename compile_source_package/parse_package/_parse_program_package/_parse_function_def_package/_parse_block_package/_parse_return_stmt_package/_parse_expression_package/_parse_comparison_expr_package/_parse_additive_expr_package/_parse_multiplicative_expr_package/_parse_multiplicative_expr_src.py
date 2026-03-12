# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """Parse multiplicative expression (handling *, / operators, left-associative)."""
    # Step 1: Get left operand
    left = _parse_unary_expr(parser_state)
    
    # Step 2-5: Loop for left-associative multiplicative operators
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        # Check if current token is multiplication operator
        if token["type"] not in ("MULTIPLY", "DIVIDE"):
            break
        
        # Step 3: Consume operator token
        operator_str = token["value"]
        line = token["line"]
        column = token["column"]
        parser_state["pos"] += 1
        
        # Get right operand
        right = _parse_unary_expr(parser_state)
        
        # Step 4: Build BINARY_OP node
        left = {
            "type": "BINARY_OP",
            "value": operator_str,
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    # Step 6: Return AST node
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function
