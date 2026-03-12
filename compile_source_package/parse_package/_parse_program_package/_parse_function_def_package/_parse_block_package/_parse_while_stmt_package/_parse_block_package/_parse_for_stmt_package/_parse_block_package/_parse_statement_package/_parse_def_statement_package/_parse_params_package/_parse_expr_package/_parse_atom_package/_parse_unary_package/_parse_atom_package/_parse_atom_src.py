# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
    解析原子表达式（最基本的不可再分的表达式单元）。
    
    支持的原子类型：
    1. NUMBER: 数字字面量，返回 NUM AST 节点
    2. STRING: 字符串字面量，返回 STR AST 节点
    3. IDENT: 标识符（变量名），返回 IDENT AST 节点
    4. TRUE/FALSE: 布尔字面量，返回 BOOL AST 节点
    5. LPAREN: 左括号，解析括号内的完整表达式
    
    副作用：更新 parser_state["pos"] 跳过已解析的 token。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise ValueError("Unexpected end of input while parsing atom")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "NUM",
            "value": int(token_value) if "." not in token_value else float(token_value),
            "line": line,
            "column": column
        }
    
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {
            "type": "STR",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "IDENT":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENT",
            "name": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {
            "type": "BOOL",
            "value": True,
            "line": line,
            "column": column
        }
    
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {
            "type": "BOOL",
            "value": False,
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        if parser_state["pos"] >= len(tokens):
            raise ValueError("Unexpected end of input, expected ')'")
        rparen_token = tokens[parser_state["pos"]]
        if rparen_token["type"] != "RPAREN":
            raise ValueError(f"Expected ')' but got {rparen_token['type']}")
        parser_state["pos"] += 1
        return expr_ast
    
    else:
        raise ValueError(f"Unexpected token type '{token_type}' at line {line}, column {column}")

# === helper functions ===

# === OOP compatibility layer ===
