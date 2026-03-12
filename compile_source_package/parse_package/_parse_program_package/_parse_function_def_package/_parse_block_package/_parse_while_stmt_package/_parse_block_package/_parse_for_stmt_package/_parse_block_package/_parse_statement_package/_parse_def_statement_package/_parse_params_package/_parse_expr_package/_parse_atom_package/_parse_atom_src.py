# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_literal_package._parse_literal_src import _parse_literal

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
def _parse_atom(parser_state: ParserState) -> AST:
    """
    解析原子表达式：字面量或标识符或一元运算。
    输入：parser_state（pos 指向原子起始 token）
    输出：原子 AST 节点
    副作用：更新 parser_state["pos"] 到原子后位置
    错误：未知 token 类型时抛 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Incomplete expression")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # 字面量
    if token_type in ("NUMBER", "STRING", "TRUE", "FALSE", "NONE"):
        return _parse_literal(parser_state, token)
    
    # 标识符
    elif token_type == "IDENT":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENT",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # 一元运算
    elif token_type in ("MINUS", "NOT"):
        from ._parse_unary_package._parse_unary_src import _parse_unary
        return _parse_unary(parser_state, token)
    
    else:
        raise SyntaxError(f"Unexpected token in expression: {token_type}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function