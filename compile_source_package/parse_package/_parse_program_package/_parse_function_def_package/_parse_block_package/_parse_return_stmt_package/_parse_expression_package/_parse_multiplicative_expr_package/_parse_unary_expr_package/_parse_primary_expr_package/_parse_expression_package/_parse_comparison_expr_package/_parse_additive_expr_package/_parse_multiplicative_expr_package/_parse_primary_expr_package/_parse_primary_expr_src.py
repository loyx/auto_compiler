# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
    """解析初级表达式（数字、标识符、括号表达式等）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input in {parser_state.get('filename', '<unknown>')} "
            f"at line {tokens[-1]['line'] if tokens else 'N/A'}, "
            f"column {tokens[-1]['column'] if tokens else 'N/A'}"
        )
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "LPAREN":
        parser_state["pos"] += 1  # consume LPAREN
        expr_ast = _parse_additive_expr(parser_state)
        
        # consume RPAREN
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Expected ')' but found end of input in {parser_state.get('filename', '<unknown>')} "
                f"at line {token['line']}, column {token['column']}"
            )
        
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] != "RPAREN":
            raise SyntaxError(
                f"Expected ')' but found '{current_token['value']}' in {parser_state.get('filename', '<unknown>')} "
                f"at line {current_token['line']}, column {current_token['column']}"
            )
        
        parser_state["pos"] += 1  # consume RPAREN
        return expr_ast
    
    else:
        raise SyntaxError(
            f"Unexpected token '{token['value']}' of type {token_type} in {parser_state.get('filename', '<unknown>')} "
            f"at line {token['line']}, column {token['column']}"
        )

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function