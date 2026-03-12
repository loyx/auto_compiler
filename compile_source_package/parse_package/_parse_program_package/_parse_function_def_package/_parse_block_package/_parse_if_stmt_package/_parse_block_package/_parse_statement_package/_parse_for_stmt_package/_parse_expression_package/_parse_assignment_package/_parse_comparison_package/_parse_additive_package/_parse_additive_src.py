# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
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
def _parse_additive(parser_state: ParserState) -> AST:
    """
    解析加法表达式（+ 和 - 运算符）。
    支持左结合连续加法，如 a + b - c。
    """
    # 1. 先解析左侧的乘法表达式
    left = _parse_multiplicative(parser_state)
    
    # 2. 检查并处理连续的加法运算符
    while True:
        current_token = _get_current_token(parser_state)
        
        # 3. 判断是否为加法运算符
        if current_token is None or current_token.get("type") not in ("PLUS", "MINUS"):
            break
        
        # 4. 记录运算符信息
        op = current_token.get("value")
        line = current_token.get("line")
        column = current_token.get("column")
        
        # 5. 消耗当前 token
        _advance(parser_state)
        
        # 6. 解析右侧的乘法表达式
        right = _parse_multiplicative(parser_state)
        
        # 7. 构建加法 AST 节点（左结合：将之前的结果作为新的 left）
        left = {
            "type": "additive",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    # 8. 返回最终结果（可能是纯乘法节点，也可能是加法节点）
    return left

# === helper functions ===
# No helper functions needed - logic is delegated to child functions

# === OOP compatibility layer ===
# Not needed for parser function nodes