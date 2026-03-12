# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._advance_package._advance_src import _advance

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
def _parse_multiplicative(parser_state: dict) -> dict:
    """解析乘法表达式（*、/、% 运算符），支持左结合连续乘法。"""
    # 1. 解析左侧一元表达式
    left = _parse_unary(parser_state)
    
    # 2. 检查并处理连续的乘法运算符
    while True:
        token = _get_current_token(parser_state)
        
        # 3. 检查是否为乘法运算符
        if token is None or token.get("type") not in ("OPERATOR",):
            break
        if token.get("value") not in ("*", "/", "%"):
            break
        
        # 4. 记录运算符信息并消耗 token
        op = token.get("value")
        line = token.get("line")
        column = token.get("column")
        _advance(parser_state)
        
        # 5. 解析右侧一元表达式
        right = _parse_unary(parser_state)
        
        # 6. 构建乘法 AST 节点（左结合）
        left = {
            "type": "multiplicative",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
# No helper functions needed; all logic is in main function.

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function.
