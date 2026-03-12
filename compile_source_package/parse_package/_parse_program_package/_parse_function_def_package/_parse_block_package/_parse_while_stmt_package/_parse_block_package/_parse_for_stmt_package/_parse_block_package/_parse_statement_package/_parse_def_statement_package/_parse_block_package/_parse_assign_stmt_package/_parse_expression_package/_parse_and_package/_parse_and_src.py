# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison
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
def _parse_and(parser_state: ParserState) -> AST:
    """解析 AND 表达式，构建左结合的 BINOP AST 节点。"""
    # 解析左操作数
    left_ast = _parse_comparison(parser_state)
    
    # 循环处理多个 AND（左结合）
    while _is_current_token(parser_state, "AND"):
        # 记录 AND token 位置
        and_token = _expect_token(parser_state, "AND")
        line = and_token.get("line", 0)
        column = and_token.get("column", 0)
        
        # 解析右操作数
        right_ast = _parse_comparison(parser_state)
        
        # 构建 BINOP 节点
        left_ast = {
            "type": "BINOP",
            "op": "and",
            "left": left_ast,
            "right": right_ast,
            "line": line,
            "column": column,
            "children": [left_ast, right_ast]
        }
    
    return left_ast

# === helper functions ===
def _is_current_token(parser_state: ParserState, token_type: str) -> bool:
    """检查当前 token 是否为指定类型，不消费 token。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    return tokens[pos].get("type") == token_type

# === OOP compatibility layer ===
