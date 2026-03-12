# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_assign_stmt_package._parse_assign_stmt_src import _parse_assign_stmt
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_def_stmt_package._parse_def_stmt_src import _parse_def_stmt
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
def _parse_block(parser_state: ParserState) -> AST:
    """解析函数体块，收集所有语句到 BODY AST 节点。"""
    tokens = parser_state["tokens"]
    start_pos = parser_state["pos"]
    statements = []
    
    while start_pos < len(tokens):
        token = tokens[start_pos]
        token_type = token["type"]
        
        if token_type == "SEMICOLON":
            parser_state["pos"] = start_pos
            break
        
        stmt_ast = _dispatch_statement(parser_state, token_type)
        statements.append(stmt_ast)
        start_pos = parser_state["pos"]
    
    line = statements[0]["line"] if statements else 0
    column = statements[0]["column"] if statements else 0
    
    return {
        "type": "BODY",
        "line": line,
        "column": column,
        "children": statements
    }

# === helper functions ===
def _dispatch_statement(parser_state: ParserState, token_type: str) -> AST:
    """根据 token 类型分发到对应的语句解析函数。"""
    dispatch_map = {
        "RETURN": _parse_return_stmt,
        "LET": _parse_assign_stmt,
        "IF": _parse_if_stmt,
        "WHILE": _parse_while_stmt,
        "FOR": _parse_for_stmt,
        "DEF": _parse_def_stmt,
    }
    
    if token_type in dispatch_map:
        return dispatch_map[token_type](parser_state)
    else:
        return _parse_expr_stmt(parser_state)

# === OOP compatibility layer ===
