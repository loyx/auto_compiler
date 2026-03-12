# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr
from ._make_error_node_package._make_error_node_src import _make_error_node
from ._convert_literal_value_package._convert_literal_value_src import _convert_literal_value

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
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """解析一元表达式（最高优先级的表达式单元）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return _make_error_node("Unexpected end of input", parser_state)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    if token_type == "OPERATOR" and token_value in ("+", "-"):
        parser_state["pos"] += 1
        operand_ast = _parse_unary_expr(parser_state)
        if parser_state.get("error"):
            return operand_ast
        return {
            "type": "UNARY_OP",
            "children": [operand_ast],
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] += 1
        expr_ast = _parse_additive_expr(parser_state)
        if parser_state.get("error"):
            return expr_ast
        
        pos = parser_state["pos"]
        if pos >= len(tokens) or tokens[pos].get("type") != "RPAREN":
            parser_state["error"] = "Expected closing parenthesis"
            return _make_error_node("Expected closing parenthesis", parser_state)
        
        parser_state["pos"] += 1
        return expr_ast
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "children": [],
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "children": [],
            "value": _convert_literal_value(token_value, token_type),
            "line": line,
            "column": column
        }
    
    else:
        parser_state["error"] = f"Unexpected token: {token_value}"
        return _make_error_node(f"Unexpected token: {token_value}", parser_state)

# === helper functions ===
# All helpers delegated to child functions

# === OOP compatibility layer ===
# Not needed
