# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions - this is an atomic parser module

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
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_atom_expr(parser_state: ParserState) -> AST:
    """解析原子表达式（标识符、字面量、括号表达式）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "EMPTY", "children": [], "value": None, "line": 0, "column": 0}
    
    token = tokens[pos]
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "children": [], "value": token_value, "line": line, "column": column}
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        val = float(token_value) if "." in token_value else int(token_value)
        return {"type": "LITERAL", "children": [], "value": val, "line": line, "column": column}
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        val = token_value[1:-1] if len(token_value) >= 2 else token_value
        return {"type": "LITERAL", "children": [], "value": val, "line": line, "column": column}
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "children": [], "value": True, "line": line, "column": column}
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "children": [], "value": False, "line": line, "column": column}
    elif token_type == "LPAREN":
        return _handle_paren(parser_state, pos, line, column)
    else:
        parser_state["error"] = f"Unexpected token '{token_value}'"
        return {"type": "EMPTY", "children": [], "value": None, "line": 0, "column": 0}

# === helper functions ===
def _handle_paren(parser_state: ParserState, pos: int, line: int, column: int) -> AST:
    """处理括号表达式，返回 PAREN_EXPR 节点。"""
    parser_state["pos"] = pos + 1
    tokens = parser_state.get("tokens", [])
    depth, start = 1, parser_state.get("pos", 0)
    p = start
    while p < len(tokens) and depth > 0:
        t = tokens[p].get("type", "")
        if t == "LPAREN": depth += 1
        elif t == "RPAREN": depth -= 1
        if depth > 0: p += 1
    if depth != 0:
        parser_state["error"] = "Unmatched parenthesis"
        return {"type": "EMPTY", "children": [], "value": None, "line": 0, "column": 0}
    parser_state["pos"] = p + 1
    return {"type": "PAREN_EXPR", "children": [], "value": {"start": start, "end": p}, "line": line, "column": column}

# === OOP compatibility layer ===
# Not needed for parser helper
