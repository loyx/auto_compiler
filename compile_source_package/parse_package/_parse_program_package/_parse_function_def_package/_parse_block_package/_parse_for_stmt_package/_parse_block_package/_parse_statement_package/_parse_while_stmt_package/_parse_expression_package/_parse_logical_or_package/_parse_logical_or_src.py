# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_and_package._parse_logical_and_src import _parse_logical_and
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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_logical_or(parser_state: ParserState) -> AST:
    """
    解析逻辑或表达式（|| 运算符）。
    这是表达式解析的最低优先级层级。
    """
    left = _parse_logical_and(parser_state)
    
    while _current_token(parser_state)["value"] == "||":
        op_token = _expect(parser_state, "OPERATOR")
        right = _parse_logical_and(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": "||",
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No additional helper functions needed

# === OOP compatibility layer ===
# Not required for parser function node
