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
#   "operator": str,
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
    解析 expression 层级语法：term ((PLUS | MINUS) term)*
    返回表达式 AST 节点，更新 parser_state['pos'] 到表达式结束位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    
    # 解析左侧 term
    left = _parse_term(parser_state)
    
    # 处理连续的 PLUS/MINUS 二元运算
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        token_type = current_token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        # 消费运算符
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 解析右侧 term
        right = _parse_term(parser_state)
        
        # 构建二元运算 AST 节点
        left = {
            "type": "BINOP",
            "operator": op_token["value"],
            "children": [left, right],
            "line": op_token.get("line", left.get("line", 0)),
            "column": op_token.get("column", left.get("column", 0))
        }
    
    return left


# === helper functions ===
# No helper functions needed in this file


# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
