# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
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
def _parse_block(parser_state: dict) -> dict:
    """解析语句块。输入：parser_state（pos 指向 LBRACE）。返回 BLOCK 类型 AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查并消费 LBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file, expected '{{'")
    current_token = tokens[pos]
    if current_token["type"] != "LBRACE":
        raise SyntaxError(f"Expected '{{', got {current_token['type']}")
    
    block_line = current_token["line"]
    block_column = current_token["column"]
    _consume_token(parser_state, "LBRACE")
    
    # 解析语句列表
    statements = []
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 遇到 RBRACE 结束块
        if current_token["type"] == "RBRACE":
            break
        
        # 根据 token 类型分发到不同解析函数
        stmt_type = current_token["type"]
        if stmt_type == "IF":
            stmt = _parse_if_stmt(parser_state)
        elif stmt_type == "WHILE":
            stmt = _parse_while_stmt(parser_state)
        elif stmt_type == "FOR":
            stmt = _parse_for_stmt(parser_state)
        elif stmt_type == "RETURN":
            stmt = _parse_return_stmt(parser_state)
        elif stmt_type == "BREAK":
            stmt = _parse_break_stmt(parser_state)
        elif stmt_type == "CONTINUE":
            stmt = _parse_continue_stmt(parser_state)
        elif stmt_type in ("VAR", "LET", "CONST"):
            stmt = _parse_var_decl(parser_state)
        else:
            stmt = _parse_expr_stmt(parser_state)
        
        statements.append(stmt)
    
    # 消费 RBRACE
    _consume_token(parser_state, "RBRACE")
    
    # 返回 BLOCK 节点
    return {
        "type": "BLOCK",
        "children": statements,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function