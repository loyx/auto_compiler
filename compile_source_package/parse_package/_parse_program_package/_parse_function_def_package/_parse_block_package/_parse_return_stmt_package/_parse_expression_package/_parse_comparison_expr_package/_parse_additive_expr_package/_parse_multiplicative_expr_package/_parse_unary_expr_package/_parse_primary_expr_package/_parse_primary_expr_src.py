# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
#   "type": str,             # 节点类型
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
#   "error": str             # 错误信息
# }


# === main function ===
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析基本表达式（标识符、字面量、括号表达式等）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of file"
        return {"type": "ERROR", "value": "Unexpected end of file", "children": [], "line": 0, "column": 0}
    
    token = tokens[pos]
    ttype = token["type"]
    tval = token["value"]
    tline = token["line"]
    tcol = token["column"]
    
    if ttype == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "value": tval, "children": [], "line": tline, "column": tcol}
    elif ttype in ("NUMBER", "STRING", "TRUE", "FALSE", "NULL"):
        parser_state["pos"] = pos + 1
        if ttype == "STRING":
            if len(tval) >= 2 and tval[0] in ('"', "'") and tval[-1] == tval[0]:
                tval = tval[1:-1]
        elif ttype == "TRUE":
            tval = True
        elif ttype == "FALSE":
            tval = False
        elif ttype == "NULL":
            tval = None
        return {"type": "LITERAL", "value": tval, "children": [], "line": tline, "column": tcol}
    elif ttype == "LPAREN":
        return _parse_paren_expr(parser_state, pos, tline)
    else:
        err = f"Unexpected token '{ttype}' at line {tline}"
        parser_state["error"] = err
        return {"type": "ERROR", "value": err, "children": [], "line": 0, "column": 0}


# === helper functions ===
def _parse_paren_expr(parser_state: ParserState, pos: int, lparen_line: int) -> AST:
    """解析括号表达式：消费 LPAREN，解析内部，消费 RPAREN。"""
    parser_state["pos"] = pos + 1
    inner = _parse_unary_expr(parser_state)
    if inner.get("type") == "ERROR":
        return inner
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        actual = "end of file" if pos >= len(tokens) else tokens[pos]["type"]
        err = f"Expected ')' at line {lparen_line}, got {actual}"
        parser_state["error"] = err
        return {"type": "ERROR", "value": err, "children": [], "line": 0, "column": 0}
    parser_state["pos"] = pos + 1
    return inner

# === OOP compatibility layer ===
# No OOP wrapper needed
