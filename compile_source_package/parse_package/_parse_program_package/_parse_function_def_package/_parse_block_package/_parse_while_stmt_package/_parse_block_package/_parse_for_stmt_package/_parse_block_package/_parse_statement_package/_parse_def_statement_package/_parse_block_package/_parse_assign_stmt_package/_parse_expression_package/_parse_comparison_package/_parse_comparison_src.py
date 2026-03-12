# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
from ._expect_token_package._expect_token_src import _expect_token
from ._current_token_package._current_token_src import _current_token

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": AST,
#   "args": list,
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
    解析比较表达式（==, !=, <, >, <=, >=）。
    
    输入：mutable parser_state
    输出：AST 节点（BINOP 或左操作数）
    处理逻辑：
    1. 调用 _parse_additive 解析左操作数
    2. 检查当前 token 是否为比较运算符
    3. 若是，消费运算符并解析右操作数，构建 BINOP 节点
    4. 若否，直接返回左操作数
    """
    left = _parse_additive(parser_state)
    current = _current_token(parser_state)
    
    comparison_types = ("EQ", "NE", "LT", "GT", "LE", "GE")
    
    if current["type"] in comparison_types:
        op_token = _expect_token(parser_state, current["type"])
        right = _parse_additive(parser_state)
        return {
            "type": "BINOP",
            "op": op_token["value"],
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"],
            "children": [left, right]
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
