# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Using lazy import to avoid circular dependency
def _get_parse_expression():
    from ._parse_expression_package._parse_expression_src import _parse_expression
    return _parse_expression

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析初级表达式（标识符、字面量、括号表达式）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否超出 token 范围
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # 标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # 数字字面量
    elif token_type == "NUMBER":
        parser_state["pos"] += 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # 字符串字面量
    elif token_type == "STRING":
        parser_state["pos"] += 1
        return {
            "type": "STRING",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # 布尔字面量
    elif token_type == "KEYWORD" and token["value"] in ("true", "false"):
        parser_state["pos"] += 1
        return {
            "type": "BOOLEAN",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # 括号表达式
    elif token_type == "LPAREN":
        parser_state["pos"] += 1  # 消费 LPAREN
        _parse_expression = _get_parse_expression()
        expr_ast = _parse_expression(parser_state)
        
        # 检查是否有匹配的 RPAREN
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError("Expected ')'")
        
        close_token = tokens[parser_state["pos"]]
        if close_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')', got {close_token}")
        
        parser_state["pos"] += 1  # 消费 RPAREN
        return expr_ast
    
    # 无法识别的 token
    else:
        raise SyntaxError(f"Unexpected token: {token}")


# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for parser function nodes
