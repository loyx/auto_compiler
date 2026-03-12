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
#   "operator": str,         # 运算符 (仅 BINARY_OP/UNARY_OP)
#   "left": AST,             # 左操作数 (仅 BINARY_OP)
#   "right": AST,            # 右操作数 (仅 BINARY_OP)
#   "operand": AST,          # 操作数 (仅 UNARY_OP)
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
    """解析一元表达式（如负号、逻辑非）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we have a token to examine
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at line {parser_state.get('filename', 'unknown')}")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # Check if current token is a unary operator
    if token_type in ("MINUS", "NOT"):
        # Consume the operator token
        parser_state["pos"] += 1
        operator = "-" if token_type == "MINUS" else "!"
        line = current_token["line"]
        column = current_token["column"]
        
        # Recursively parse the operand (supports chained unary ops like --x)
        operand = _parse_unary_expr(parser_state)
        
        # Build UNARY_OP AST node
        return {
            "type": "UNARY_OP",
            "operator": operator,
            "operand": operand,
            "line": line,
            "column": column
        }
    else:
        # Not a unary operator, parse primary expression
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
