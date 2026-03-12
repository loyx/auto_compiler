# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl
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
def _parse_statement(parser_state: dict) -> dict:
    """解析单条语句，根据 token 类型分发到不同语句处理逻辑。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"{parser_state['filename']}:0:0: 期望语句，但已到达 token 末尾")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    if token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "BREAK":
        parser_state["pos"] += 1
        return {"type": "BREAK_STMT", "line": current_token["line"], "column": current_token["column"]}
    elif token_type == "CONTINUE":
        parser_state["pos"] += 1
        return {"type": "CONTINUE_STMT", "line": current_token["line"], "column": current_token["column"]}
    elif token_type in ("VAR", "LET"):
        return _parse_var_decl(parser_state)
    else:
        return _parse_expr_stmt(parser_state)


# === helper functions ===

# === OOP compatibility layer ===
