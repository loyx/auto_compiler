# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions delegated

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL)
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
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """解析表达式，返回 AST 节点。"""
    return _parse_or(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    if parser_state["pos"] >= len(parser_state["tokens"]):
        return {"type": "EOF", "value": None, "line": 0, "column": 0}
    return parser_state["tokens"][parser_state["pos"]]

def _consume(parser_state: ParserState, expected_type: str) -> Token:
    token = _current_token(parser_state)
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token['type']}")
    parser_state["pos"] += 1
    return token

def _parse_or(parser_state: ParserState) -> AST:
    left = _parse_and(parser_state)
    while _current_token(parser_state)["type"] == "OR":
        op_token = _consume(parser_state, "OR")
        right = _parse_and(parser_state)
        left = {"type": "BINARY_OP", "value": "||", "children": [left, right], "line": op_token["line"], "column": op_token["column"]}
    return left

def _parse_and(parser_state: ParserState) -> AST:
    left = _parse_equality(parser_state)
    while _current_token(parser_state)["type"] == "AND":
        op_token = _consume(parser_state, "AND")
        right = _parse_equality(parser_state)
        left = {"type": "BINARY_OP", "value": "&&", "children": [left, right], "line": op_token["line"], "column": op_token["column"]}
    return left

def _parse_equality(parser_state: ParserState) -> AST:
    left = _parse_comparison(parser_state)
    while _current_token(parser_state)["type"] in ("EQ", "NEQ"):
        op_token = _consume(parser_state, _current_token(parser_state)["type"])
        op_str = "==" if op_token["type"] == "EQ" else "!="
        right = _parse_comparison(parser_state)
        left = {"type": "BINARY_OP", "value": op_str, "children": [left, right], "line": op_token["line"], "column": op_token["column"]}
    return left

def _parse_comparison(parser_state: ParserState) -> AST:
    left = _parse_additive(parser_state)
    while _current_token(parser_state)["type"] in ("LT", "GT", "LTE", "GTE"):
        op_token = _consume(parser_state, _current_token(parser_state)["type"])
        op_map = {"LT": "<", "GT": ">", "LTE": "<=", "GTE": ">="}
        right = _parse_additive(parser_state)
        left = {"type": "BINARY_OP", "value": op_map[op_token["type"]], "children": [left, right], "line": op_token["line"], "column": op_token["column"]}
    return left

def _parse_additive(parser_state: ParserState) -> AST:
    left = _parse_multiplicative(parser_state)
    while _current_token(parser_state)["type"] in ("PLUS", "MINUS"):
        op_token = _consume(parser_state, _current_token(parser_state)["type"])
        op_str = "+" if op_token["type"] == "PLUS" else "-"
        right = _parse_multiplicative(parser_state)
        left = {"type": "BINARY_OP", "value": op_str, "children": [left, right], "line": op_token["line"], "column": op_token["column"]}
    return left

def _parse_multiplicative(parser_state: ParserState) -> AST:
    left = _parse_unary(parser_state)
    while _current_token(parser_state)["type"] in ("STAR", "SLASH", "PERCENT"):
        op_token = _consume(parser_state, _current_token(parser_state)["type"])
        op_map = {"STAR": "*", "SLASH": "/", "PERCENT": "%"}
        right = _parse_unary(parser_state)
        left = {"type": "BINARY_OP", "value": op_map[op_token["type"]], "children": [left, right], "line": op_token["line"], "column": op_token["column"]}
    return left

def _parse_unary(parser_state: ParserState) -> AST:
    if _current_token(parser_state)["type"] in ("MINUS", "NOT", "TILDE"):
        op_token = _consume(parser_state, _current_token(parser_state)["type"])
        op_map = {"MINUS": "-", "NOT": "!", "TILDE": "~"}
        operand = _parse_unary(parser_state)
        return {"type": "UNARY_OP", "value": op_map[op_token["type"]], "children": [operand], "line": op_token["line"], "column": op_token["column"]}
    return _parse_primary(parser_state)

def _parse_primary(parser_state: ParserState) -> AST:
    token = _current_token(parser_state)
    if token["type"] == "EOF":
        raise SyntaxError("Unexpected end of input")
    if token["type"] == "IDENTIFIER":
        parser_state["pos"] += 1
        return {"type": "IDENTIFIER", "value": token["value"], "children": [], "line": token["line"], "column": token["column"]}
    if token["type"] in ("INTEGER", "FLOAT", "STRING", "BOOLEAN"):
        parser_state["pos"] += 1
        value = token["value"]
        return {"type": "LITERAL", "value": value, "children": [], "line": token["line"], "column": token["column"]}
    if token["type"] == "LPAREN":
        _consume(parser_state, "LPAREN")
        expr = _parse_or(parser_state)
        _consume(parser_state, "RPAREN")
        return expr
    raise SyntaxError(f"Unexpected token: {token['type']}")

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node