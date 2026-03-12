# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_if_statement_package._parse_if_statement_src import _parse_if_statement
from ._parse_while_statement_package._parse_while_statement_src import _parse_while_statement
from ._parse_return_statement_package._parse_return_statement_src import _parse_return_statement
from ._parse_assign_or_expr_package._parse_assign_or_expr_src import _parse_assign_or_expr

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
def _parse_statement(parser_state: dict) -> dict:
    """解析单条语句（含结尾分号），返回语句 AST 节点。"""
    current_token = _peek_token(parser_state)
    
    if current_token is None:
        raise SyntaxError("Unexpected end of input")
    
    token_type = current_token["type"]
    line = current_token["line"]
    column = current_token["column"]
    
    if token_type == "LBRACE":
        from ._parse_block_package._parse_block_src import _parse_block
        return _parse_block(parser_state)
    elif token_type == "IF":
        _consume_token(parser_state, "IF")
        return _parse_if_statement(parser_state)
    elif token_type == "WHILE":
        _consume_token(parser_state, "WHILE")
        return _parse_while_statement(parser_state)
    elif token_type == "RETURN":
        _consume_token(parser_state, "RETURN")
        return _parse_return_statement(parser_state)
    elif token_type == "IDENT":
        _consume_token(parser_state, "IDENT")
        return _parse_assign_or_expr(parser_state)
    else:
        raise SyntaxError(f"Unexpected token '{token_type}' at line {line}, column {column}")

# === helper functions ===

# === OOP compatibility layer ===
