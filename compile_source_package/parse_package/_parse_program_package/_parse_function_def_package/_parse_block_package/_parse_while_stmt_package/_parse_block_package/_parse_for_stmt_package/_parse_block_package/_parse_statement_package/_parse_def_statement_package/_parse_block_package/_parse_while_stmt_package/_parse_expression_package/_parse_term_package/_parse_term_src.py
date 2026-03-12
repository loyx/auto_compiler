# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

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
#   "column": int,
#   "op": str,
#   "left": AST,
#   "right": AST
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
def _parse_term(parser_state: ParserState) -> AST:
    """
    解析 term 层级：term := factor ((MUL | DIV) factor)*
    
    输入：parser_state（pos 指向 term 起始 token）
    输出：term AST 节点
    副作用：更新 parser_state["pos"] 到 term 之后的位置
    """
    # 解析左侧 factor
    left = _parse_factor(parser_state)
    
    # 处理连续的 MUL/DIV 运算符
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        if token["type"] not in ("MUL", "DIV"):
            break
        
        op_token = token
        parser_state["pos"] += 1
        
        # 解析右侧 factor
        right = _parse_factor(parser_state)
        
        # 构建二元操作节点
        left = {
            "type": "BINOP",
            "op": op_token["type"],
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left


# === helper functions ===


# === OOP compatibility layer ===
