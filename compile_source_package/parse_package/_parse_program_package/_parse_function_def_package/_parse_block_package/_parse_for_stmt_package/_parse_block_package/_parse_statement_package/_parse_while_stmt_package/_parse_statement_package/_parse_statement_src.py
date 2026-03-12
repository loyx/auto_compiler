# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt

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
def _parse_statement(parser_state: ParserState) -> AST:
    """解析单条语句。根据当前 token 类型分发到对应的语句解析函数。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(f"{filename}:0:0: unexpected end of input")
    
    token_type = tokens[pos]["type"]
    
    if token_type == "VAR":
        return _parse_var_decl(parser_state)
    elif token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "BREAK":
        return _parse_break_stmt(parser_state)
    elif token_type == "CONTINUE":
        return _parse_continue_stmt(parser_state)
    elif token_type == "LBRACE":
        return _parse_block(parser_state)
    else:
        return _parse_expr_stmt(parser_state)

# === helper functions ===

# === OOP compatibility layer ===
