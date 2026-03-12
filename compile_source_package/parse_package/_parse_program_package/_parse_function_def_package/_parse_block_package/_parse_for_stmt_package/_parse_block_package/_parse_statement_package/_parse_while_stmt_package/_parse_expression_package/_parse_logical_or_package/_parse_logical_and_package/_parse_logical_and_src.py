# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison
from ._current_token_package._current_token_src import _current_token
from ._expect_package._expect_src import _expect

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_logical_and(parser_state: ParserState) -> AST:
    """
    解析逻辑与表达式（&& 运算符）。
    优先级高于 ||，低于比较运算符。
    左结合：a && b && c 解析为 ((a && b) && c)
    """
    left: AST = _parse_comparison(parser_state)
    
    while True:
        token: Optional[Token] = _current_token(parser_state)
        if token is None or token["value"] != "&&":
            break
        
        _expect(parser_state, "OPERATOR", "&&")
        right = _parse_comparison(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": "&&",
            "children": [left, right],
            "line": token["line"],
            "column": token["column"]
        }
    
    return left

# === helper functions ===


# === OOP compatibility layer ===
