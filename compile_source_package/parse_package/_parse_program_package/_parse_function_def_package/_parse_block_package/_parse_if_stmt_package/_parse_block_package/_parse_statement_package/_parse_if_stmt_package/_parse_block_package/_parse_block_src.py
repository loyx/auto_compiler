# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_continue_stmt_package._parse_break_continue_stmt_src import _parse_break_continue_stmt
from ._parse_assign_stmt_package._parse_assign_stmt_src import _parse_assign_stmt
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_block(parser_state: ParserState) -> AST:
    """解析语句块。输入：parser_state（pos 指向 LBRACE token）。输出：BLOCK AST 节点。"""
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected '{{'")
    
    current_token = tokens[parser_state["pos"]]
    if current_token["type"] != "LBRACE":
        raise SyntaxError(f"{filename}:{current_token['line']}:{current_token['column']}: Expected '{{', got {current_token['type']}")
    
    block_line = current_token["line"]
    block_column = current_token["column"]
    
    _consume_token(parser_state, "LBRACE")
    
    statements = []
    
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] == "RBRACE":
            _consume_token(parser_state, "RBRACE")
            break
        
        stmt = _parse_statement(parser_state)
        statements.append(stmt)
        
        if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "SEMICOLON":
            _consume_token(parser_state, "SEMICOLON")
    else:
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{block_line}:{block_column}: Unclosed block, missing '}}'")
    
    return {
        "type": "BLOCK",
        "statements": statements,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
def _parse_statement(parser_state: ParserState) -> AST:
    """根据当前 token 类型分发到相应的语句解析函数。"""
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input in block")
    
    current_token = tokens[parser_state["pos"]]
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
        return _parse_break_continue_stmt(parser_state)
    elif token_type == "CONTINUE":
        return _parse_break_continue_stmt(parser_state)
    elif token_type == "IDENTIFIER":
        if parser_state["pos"] + 1 < len(tokens) and tokens[parser_state["pos"] + 1]["type"] == "ASSIGN":
            return _parse_assign_stmt(parser_state)
        else:
            return _parse_expr_stmt(parser_state)
    else:
        return _parse_expr_stmt(parser_state)

# === OOP compatibility layer ===
