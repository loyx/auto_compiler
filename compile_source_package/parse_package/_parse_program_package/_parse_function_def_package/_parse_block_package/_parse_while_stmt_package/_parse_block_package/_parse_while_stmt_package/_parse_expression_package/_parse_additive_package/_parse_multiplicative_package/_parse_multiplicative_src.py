# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_multiplicative(parser_state: ParserState) -> tuple:
    """
    解析乘法/除法表达式（*, /）。
    左结合性，返回 (AST 节点，更新后的 parser_state)。
    """
    # 解析左侧表达式
    left_ast, parser_state = _parse_primary(parser_state)
    
    # 循环处理乘除运算符
    while True:
        token = _peek_token(parser_state)
        
        if token is None:
            break
        
        if token["type"] not in ("STAR", "SLASH"):
            break
        
        # 记录运算符信息
        op_token = _consume_token(parser_state, token["type"])
        operator = "*" if token["type"] == "STAR" else "/"
        
        # 解析右侧表达式
        right_ast, parser_state = _parse_primary(parser_state)
        
        # 构建 BINARY_OP AST 节点
        left_ast = {
            "type": "BINARY_OP",
            "value": operator,
            "children": [left_ast, right_ast],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return (left_ast, parser_state)

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a parser helper function