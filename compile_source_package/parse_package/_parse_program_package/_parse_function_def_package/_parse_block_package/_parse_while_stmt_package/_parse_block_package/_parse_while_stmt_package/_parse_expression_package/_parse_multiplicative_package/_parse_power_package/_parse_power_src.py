# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
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
def _parse_power(parser_state: ParserState) -> tuple:
    """
    解析幂运算表达式（^）。
    右结合：a ^ b ^ c 解析为 a ^ (b ^ c)
    """
    # 解析左侧表达式（一元表达式）
    left_ast, parser_state = _parse_unary(parser_state)
    
    # 循环处理幂运算符（右结合通过递归实现）
    while True:
        token = _peek_token(parser_state)
        
        # 检查是否为幂运算符
        if token is None or token.get("type") not in ("POWER", "^"):
            break
        
        # 消费幂运算符 token
        op_token, parser_state = _consume_token(parser_state)
        
        # 递归解析右侧表达式（右结合）
        right_ast, parser_state = _parse_power(parser_state)
        
        # 构建二元运算 AST 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": "^",
            "left": left_ast,
            "right": right_ast,
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return (left_ast, parser_state)

# === helper functions ===
# No helper functions needed - all logic in main

# === OOP compatibility layer ===
# Not needed for parser function nodes
