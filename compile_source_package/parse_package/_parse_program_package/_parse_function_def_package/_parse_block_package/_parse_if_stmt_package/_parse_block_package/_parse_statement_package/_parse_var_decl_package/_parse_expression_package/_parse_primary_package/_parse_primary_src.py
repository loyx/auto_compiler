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
def _parse_primary(parser_state: ParserState) -> AST:
    """解析基础单元（字面量、标识符、括号表达式）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "number_literal",
            "value": float(token_value) if "." in token_value else int(token_value),
            "line": line,
            "column": column
        }
    
    elif token_type == "STRING_LITERAL":
        parser_state["pos"] = pos + 1
        # 去掉引号（支持单引号和双引号）
        if token_value.startswith('"') and token_value.endswith('"'):
            value = token_value[1:-1]
        elif token_value.startswith("'") and token_value.endswith("'"):
            value = token_value[1:-1]
        else:
            value = token_value
        return {
            "type": "string_literal",
            "value": value,
            "line": line,
            "column": column
        }
    
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {
            "type": "boolean_literal",
            "value": True,
            "line": line,
            "column": column
        }
    
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {
            "type": "boolean_literal",
            "value": False,
            "line": line,
            "column": column
        }
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "identifier",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')' but found end of input")
        
        parser_state["pos"] = new_pos + 1
        return expr_ast
    
    else:
        raise SyntaxError(f"{filename}:{line}:{column}: Unexpected token '{token_value}' of type {token_type}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
