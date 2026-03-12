# === std / third-party imports ===
import os
import sys
from typing import Any, Dict

# Get the directory of the current file for relative imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _current_dir)

# === sub function imports ===
from _parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_and_expr(parser_state: ParserState) -> AST:
    """解析 AND 表达式（&& 运算符，左结合）。"""
    left = _parse_comparison_expr(parser_state)
    
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        if current_token.get("type") != "AND":
            break
        
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        parser_state["pos"] = pos + 1
        
        right = _parse_comparison_expr(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": "&&",
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
