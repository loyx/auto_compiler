# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
def _parse_expr(parser_state: ParserState) -> AST:
    """
    解析表达式：expr := term ((PLUS | MINUS) term)*
    构建左结合的 AST 树。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of expression in {parser_state.get('filename', '<unknown>')}")
    
    # 解析第一个 term
    left = _parse_term(parser_state)
    
    # 循环处理 PLUS/MINUS 运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        token_type = current_token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        op_token = current_token
        parser_state["pos"] += 1
        
        # 解析右侧 term
        right = _parse_term(parser_state)
        
        # 构建左结合的二元操作节点
        left = {
            "type": "BINOP",
            "op": op_token["type"],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0),
            "children": [left, right]
        }
    
    return left

# === helper functions ===
# No helper functions needed in this file

# === OOP compatibility layer ===
# Not needed for parser function nodes
