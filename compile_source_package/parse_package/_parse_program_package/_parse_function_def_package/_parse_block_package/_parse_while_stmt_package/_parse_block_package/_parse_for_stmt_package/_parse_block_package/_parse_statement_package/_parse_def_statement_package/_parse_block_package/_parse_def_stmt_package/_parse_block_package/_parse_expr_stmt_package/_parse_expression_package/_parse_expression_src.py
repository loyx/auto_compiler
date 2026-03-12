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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析 expression := term ((PLUS | MINUS) term)*。
    输入 parser_state（pos 指向 term 起始），输出 expression AST 节点。
    副作用：消费所有 term 和 PLUS/MINUS token，更新 pos。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析第一个 term
    left = _parse_term(parser_state)
    
    # 循环处理后续的 PLUS/MINUS 运算符
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        
        if token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 记录运算符信息
        op_token = token
        parser_state["pos"] += 1  # 消费运算符
        
        # 解析右侧 term
        right = _parse_term(parser_state)
        
        # 构建左结合的 BINOP 节点
        left = {
            "type": "BINOP",
            "value": op_token["value"],
            "line": op_token["line"],
            "column": op_token["column"],
            "children": [left, right]
        }
    
    return left

# === helper functions ===
def _create_binop_node(op_token: Token, left: AST, right: AST) -> AST:
    """创建二元运算 AST 节点。"""
    return {
        "type": "BINOP",
        "value": op_token["value"],
        "line": op_token["line"],
        "column": op_token["column"],
        "children": [left, right]
    }

# === OOP compatibility layer ===
# Not required for this parser function node
