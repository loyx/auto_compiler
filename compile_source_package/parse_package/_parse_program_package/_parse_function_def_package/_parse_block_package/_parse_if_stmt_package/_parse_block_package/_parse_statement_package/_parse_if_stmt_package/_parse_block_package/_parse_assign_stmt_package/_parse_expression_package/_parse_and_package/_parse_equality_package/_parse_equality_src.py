# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_equality(parser_state: ParserState) -> AST:
    """
    解析相等性表达式（优先级 Level 4）。
    支持 == 和 != 运算符，左结合。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 解析左侧操作数（比较表达式，更高优先级）
    left_ast = _parse_comparison(parser_state)
    
    # 循环处理相等性运算符（左结合）
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] not in ("EQ", "NE"):
            break
        
        # 消耗运算符 token
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 解析右侧操作数
        right_ast = _parse_comparison(parser_state)
        
        # 构建 BINARY AST 节点
        operator = "==" if op_token["type"] == "EQ" else "!="
        left_ast = {
            "type": "BINARY",
            "operator": operator,
            "left": left_ast,
            "right": right_ast,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
def _raise_syntax_error(filename: str, line: int, column: int, expected: str, got: str) -> None:
    """抛出语法错误异常。"""
    raise SyntaxError(f"{filename}:{line}:{column}: 预期 {expected}，但得到 '{got}'")

# === OOP compatibility layer ===
# Not required for this parser function node