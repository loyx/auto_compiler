# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """
    解析比较表达式（优先级 Level 3：LT, GT, LE, GE）。
    支持左结合，循环处理多个比较运算符。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 1. 先解析左侧操作数（调用 _parse_term）
    left_ast = _parse_term(parser_state)
    
    # 2. 循环检查并处理比较运算符
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        
        if token["type"] not in ("LT", "GT", "LE", "GE"):
            break
        
        # 3. 消耗运算符 token
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 4. 解析右侧操作数
        right_ast = _parse_term(parser_state)
        
        # 5. 构建 BINARY AST 节点
        left_ast = {
            "type": "BINARY",
            "operator": op_token["value"],
            "left": left_ast,
            "right": right_ast,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function