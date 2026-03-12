# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_statement(parser_state: dict) -> dict:
    """Parse a single statement and return corresponding AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    if token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "BREAK":
        parser_state["pos"] = pos + 1
        return {
            "type": "BREAK_STMT",
            "line": current_token["line"],
            "column": current_token["column"]
        }
    elif token_type == "CONTINUE":
        parser_state["pos"] = pos + 1
        return {
            "type": "CONTINUE_STMT",
            "line": current_token["line"],
            "column": current_token["column"]
        }
    else:
        # Expression statement: parse expression then consume SEMICOLON
        expr_ast = _parse_expression(parser_state)
        pos = parser_state["pos"]
        
        if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
            raise SyntaxError(
                f"{filename}:{current_token['line']}:{current_token['column']}: "
                "Expected ';' after expression"
            )
        
        parser_state["pos"] = pos + 1
        
        return {
            "type": "EXPR_STMT",
            "children": [expr_ast],
            "line": current_token["line"],
            "column": current_token["column"]
        }

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this parser function node
