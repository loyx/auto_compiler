# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
from ._expect_token_package._expect_token_src import _expect_token

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
    """解析比较表达式，构建 BINOP AST 节点。"""
    left_ast = _parse_additive(parser_state)
    
    if not _is_current_token_comparison_op(parser_state):
        return left_ast
    
    op_token = _expect_token(
        parser_state,
        parser_state["tokens"][parser_state["pos"]]["type"]
    )
    line = op_token.get("line", 0)
    column = op_token.get("column", 0)
    op_type = op_token.get("type")
    
    op_map = {
        "EQ": "eq", "NE": "ne", "LT": "lt",
        "GT": "gt", "LE": "le", "GE": "ge"
    }
    op_value = op_map[op_type]
    
    right_ast = _parse_additive(parser_state)
    
    return {
        "type": "BINOP",
        "op": op_value,
        "left": left_ast,
        "right": right_ast,
        "line": line,
        "column": column,
        "children": [left_ast, right_ast]
    }

# === helper functions ===
def _is_current_token_comparison_op(parser_state: ParserState) -> bool:
    """检查当前 token 是否为比较运算符类型。"""
    COMPARISON_OPS = {"EQ", "NE", "LT", "GT", "LE", "GE"}
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    return tokens[pos].get("type") in COMPARISON_OPS

# === OOP compatibility layer ===
