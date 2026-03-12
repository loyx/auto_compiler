# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_relational_package._parse_relational_src import _parse_relational

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
def _parse_equality(parser_state: ParserState) -> AST:
    """Parse equality expressions (== and != operators)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Parse left operand (relational expression)
    left = _parse_relational(parser_state)
    
    # Loop for == and != operators (left-associative)
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        
        if token.get("type") != "OPERATOR" or token.get("value") not in ("==", "!="):
            break
        
        # Consume operator token
        op_token = token
        parser_state["pos"] += 1
        
        # Parse right operand
        right = _parse_relational(parser_state)
        
        # Build BINARY_OP node
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token["value"],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function nodes
