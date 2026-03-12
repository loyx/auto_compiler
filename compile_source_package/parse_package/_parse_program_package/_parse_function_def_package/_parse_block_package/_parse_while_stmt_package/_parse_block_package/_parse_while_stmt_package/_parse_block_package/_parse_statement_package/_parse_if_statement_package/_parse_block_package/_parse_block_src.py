# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._peek_token_package._peek_token_src import _peek_token
from ._parse_statement_package._parse_statement_src import _parse_statement

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
#   "statements": list,  # for BLOCK nodes
#   "children": list,    # for other nodes
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
#   "error": str | None
# }

# === main function ===
def _parse_block(parser_state: dict) -> dict:
    """
    解析语句块并返回 BLOCK AST 节点。
    
    行为：
    1. 如果当前 token 是 LBRACE，消费它，解析多个语句直到 RBRACE
    2. 如果不是 LBRACE，解析单个语句作为块
    3. 原地修改 parser_state（推进 pos）
    4. 返回 BLOCK AST 节点
    5. 遇到 RBRACE 时消费它并结束
    6. 遇到语法错误时抛出 SyntaxError 异常
    """
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError(f"Unexpected EOF while parsing block at line {parser_state.get('filename', 'unknown')}")
    
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    statements = []
    
    if token.get("type") == "LBRACE":
        _consume_token(parser_state, "LBRACE")
        
        while True:
            token = _peek_token(parser_state)
            
            if token is None:
                raise SyntaxError(f"Expected RBRACE but got EOF at line {parser_state.get('filename', 'unknown')}")
            
            if token.get("type") == "RBRACE":
                _consume_token(parser_state, "RBRACE")
                break
            
            stmt = _parse_statement(parser_state)
            statements.append(stmt)
    else:
        stmt = _parse_statement(parser_state)
        statements.append(stmt)
    
    return {
        "type": "BLOCK",
        "statements": statements,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed; logic delegated to child functions.

# === OOP compatibility layer ===
# Not required for this parser function node.
