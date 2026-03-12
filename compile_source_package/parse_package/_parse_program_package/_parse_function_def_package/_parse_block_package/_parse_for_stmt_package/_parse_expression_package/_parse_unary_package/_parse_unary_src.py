# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_unary(parser_state: ParserState) -> AST:
    """Parse unary expression (-, not)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we have a token to examine
    if pos >= len(tokens):
        return _parse_primary(parser_state)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # Check for unary operators
    if token_type in ("MINUS", "NOT"):
        # Record operator and consume token
        op_string = "-" if token_type == "MINUS" else "not"
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # Consume the operator token
        parser_state["pos"] = pos + 1
        
        # Recursively parse the operand (supports --x, not not x)
        operand = _parse_unary(parser_state)
        
        # Build UNARY_OP node
        return {
            "type": "UNARY_OP",
            "value": op_string,
            "children": [operand],
            "line": op_line,
            "column": op_column
        }
    else:
        # Not a unary operator, delegate to primary
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
