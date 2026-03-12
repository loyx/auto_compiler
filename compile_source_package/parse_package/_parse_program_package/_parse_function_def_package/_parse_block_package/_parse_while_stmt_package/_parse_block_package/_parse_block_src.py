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
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
from ._consume_token_package._consume_token_src import _consume_token
from ._peek_token_package._peek_token_src import _peek_token

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
def _parse_block(parser_state: dict) -> dict:
    """解析语句块，返回 BLOCK 类型 AST 节点。"""
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError("Unexpected end of input while parsing block")
    
    line = token.get("line", 0)
    column = token.get("column", 0)
    statements = []
    
    # 检查是否是花括号块
    if token.get("type") == "LBRACE":
        parser_state = _consume_token(parser_state, "LBRACE")
        
        # 解析块内语句直到 RBRACE
        while True:
            token = _peek_token(parser_state)
            if token is None:
                raise SyntaxError("Unexpected end of input, expected '}'")
            
            if token.get("type") == "RBRACE":
                parser_state = _consume_token(parser_state, "RBRACE")
                break
            
            stmt = _parse_statement(parser_state)
            statements.append(stmt)
    else:
        # 单个语句作为块
        stmt = _parse_statement(parser_state)
        statements.append(stmt)
    
    return {
        "type": "BLOCK",
        "children": statements,
        "line": line,
        "column": column
    }

# === helper functions ===
def _parse_statement(parser_state: dict) -> dict:
    """根据当前 token 类型解析对应的语句。"""
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError("Unexpected end of input while parsing statement")
    
    token_type = token.get("type")
    
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
    else:
        # 默认为表达式语句
        return _parse_expr_stmt(parser_state)

# === OOP compatibility layer ===
