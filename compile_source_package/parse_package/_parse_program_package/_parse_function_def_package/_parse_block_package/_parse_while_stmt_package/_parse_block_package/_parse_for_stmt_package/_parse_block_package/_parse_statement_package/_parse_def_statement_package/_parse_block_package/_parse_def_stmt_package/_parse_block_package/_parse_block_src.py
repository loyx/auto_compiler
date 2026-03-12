# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_def_stmt_package._parse_def_stmt_src import _parse_def_stmt
from ._parse_assign_stmt_package._parse_assign_stmt_src import _parse_assign_stmt
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt

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
    """解析函数体块（COLON 到 SEMICOLON 之间的语句）。"""
    tokens = parser_state["tokens"]
    start_pos = parser_state["pos"]
    
    if start_pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file in block at {parser_state.get('filename', 'unknown')}")
    
    start_line = tokens[start_pos].get("line", 0)
    start_column = tokens[start_pos].get("column", 0)
    
    statements = []
    
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查是否到达块结束
        if current_token["type"] == "SEMICOLON":
            parser_state["pos"] += 1
            break
        
        # 根据 token 类型分发到不同的语句解析器
        stmt_ast = _parse_statement_by_type(parser_state, current_token)
        statements.append(stmt_ast)
    
    # 验证是否找到 SEMICOLON
    if parser_state["pos"] <= start_pos or (parser_state["pos"] < len(tokens) and 
                                            tokens[parser_state["pos"] - 1]["type"] != "SEMICOLON"):
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Missing SEMICOLON to close block at {parser_state.get('filename', 'unknown')}")
    
    return {
        "type": "BLOCK",
        "line": start_line,
        "column": start_column,
        "children": statements
    }

# === helper functions ===
def _parse_statement_by_type(parser_state: ParserState, token: Token) -> AST:
    """根据 token 类型分发到相应的语句解析函数。"""
    token_type = token["type"]
    
    if token_type == "DEF":
        return _parse_def_stmt(parser_state)
    elif token_type == "IDENTIFIER":
        # 可能是赋值语句或表达式语句，需要查看下一个 token
        next_pos = parser_state["pos"] + 1
        if next_pos < len(parser_state["tokens"]):
            next_token = parser_state["tokens"][next_pos]
            if next_token["type"] == "ASSIGN":
                return _parse_assign_stmt(parser_state)
        return _parse_expr_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "IF":
        return _parse_if_stmt(parser_state)
    else:
        # 默认作为表达式语句处理
        return _parse_expr_stmt(parser_state)

# === OOP compatibility layer ===
