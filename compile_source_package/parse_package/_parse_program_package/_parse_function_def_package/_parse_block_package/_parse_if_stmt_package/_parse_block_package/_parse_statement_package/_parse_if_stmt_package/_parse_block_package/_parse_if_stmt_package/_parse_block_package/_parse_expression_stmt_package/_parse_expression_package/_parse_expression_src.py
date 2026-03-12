# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
#   "left": AST,
#   "right": AST,
#   "operator": str,
#   "name": str
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
def _parse_expression(parser_state: dict) -> dict:
    """解析表达式，支持字面量、标识符、二元运算、括号表达式。"""
    if parser_state.get("error"):
        return {}
    
    left = _parse_primary(parser_state)
    if parser_state.get("error"):
        return {}
    
    return _parse_binary_expr(parser_state, left, 0)

# === helper functions ===
def _get_operator_precedence(op_type: str) -> int:
    """获取运算符优先级。"""
    precedence_map = {
        "OR": 1,
        "AND": 2,
        "EQ": 3, "NE": 3,
        "LT": 4, "LE": 4, "GT": 4, "GE": 4,
        "PLUS": 5, "MINUS": 5,
        "MUL": 6, "DIV": 6, "MOD": 6,
    }
    return precedence_map.get(op_type, 0)

def _parse_binary_expr(parser_state: dict, left: dict, min_prec: int) -> dict:
    """处理二元运算符（考虑优先级）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        op_type = token.get("type")
        
        if op_type not in ["OR", "AND", "EQ", "NE", "LT", "LE", "GT", "GE", "PLUS", "MINUS", "MUL", "DIV", "MOD"]:
            break
        
        prec = _get_operator_precedence(op_type)
        if prec < min_prec:
            break
        
        parser_state["pos"] = pos + 1
        right = _parse_primary(parser_state)
        if parser_state.get("error"):
            return {}
        
        while parser_state["pos"] < len(tokens):
            next_token = tokens[parser_state["pos"]]
            next_op = next_token.get("type")
            next_prec = _get_operator_precedence(next_op)
            
            if next_prec <= prec:
                break
            
            right = _parse_binary_expr(parser_state, right, next_prec)
            if parser_state.get("error"):
                return {}
        
        left = {
            "type": "BINARY_EXPR",
            "left": left,
            "operator": token.get("value", op_type),
            "right": right,
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
        
        pos = parser_state["pos"]
    
    return left

# === OOP compatibility layer ===
