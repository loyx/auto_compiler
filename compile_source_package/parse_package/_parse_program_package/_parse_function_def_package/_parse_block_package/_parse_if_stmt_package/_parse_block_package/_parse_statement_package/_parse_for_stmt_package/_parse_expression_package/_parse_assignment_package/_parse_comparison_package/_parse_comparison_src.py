# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
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
def _parse_comparison(parser_state: ParserState) -> AST:
    """
    解析比较表达式（<, >, <=, >=, ==, !=）。
    支持连续比较（左结合），如 a < b < c。
    """
    # 先解析左侧加法表达式
    left = _parse_additive(parser_state)
    
    # 比较运算符集合
    comparison_ops = {"<", ">", "<=", ">=", "==", "!="}
    
    # 检查是否连续比较
    while True:
        token = _get_current_token(parser_state)
        if token is None:
            break
        
        op = token.get("value", "")
        if op not in comparison_ops:
            break
        
        # 记录运算符位置信息
        line = token.get("line", 0)
        column = token.get("column", 0)
        
        # 消耗当前 token
        _advance(parser_state)
        
        # 解析右侧加法表达式
        right = _parse_additive(parser_state)
        
        # 构建比较 AST 节点（左结合）
        left = {
            "type": "comparison",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser function nodes