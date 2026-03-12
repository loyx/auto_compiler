# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
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
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """
    解析 while 语句。
    语法：while ( condition ) { statement_list }
    输入：parser_state（pos 指向 WHILE token）
    输出：WHILE_STMT AST 节点
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 1. 消费 WHILE token
    while_token = _expect_token(parser_state, "WHILE", filename)
    start_line = while_token["line"]
    start_column = while_token["column"]
    
    # 2. 消费 LPAREN
    _expect_token(parser_state, "LPAREN", filename)
    
    # 3. 解析条件表达式
    condition = _parse_expression(parser_state)
    
    # 4. 消费 RPAREN
    _expect_token(parser_state, "RPAREN", filename)
    
    # 5. 消费 LBRACE
    _expect_token(parser_state, "LBRACE", filename)
    
    # 6. 解析语句列表，直到 RBRACE
    statements: List[AST] = []
    while _current_token(parser_state)["type"] != "RBRACE":
        stmt = _parse_statement(parser_state)
        statements.append(stmt)
    
    # 7. 消费 RBRACE
    _expect_token(parser_state, "RBRACE", filename)
    
    # 构建 BLOCK 节点作为 body
    body: AST = {
        "type": "BLOCK",
        "children": statements,
        "line": start_line,
        "column": start_column
    }
    
    # 构建 WHILE_STMT 节点
    return {
        "type": "WHILE_STMT",
        "children": [condition, body],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token（不消费）。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        # 返回 EOF token
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    return tokens[pos]

def _expect_token(parser_state: ParserState, expected_type: str, filename: str) -> Token:
    """
    期望当前 token 为指定类型，是则消费并返回，否则抛出 SyntaxError。
    """
    token = _current_token(parser_state)
    if token["type"] != expected_type:
        line = token.get("line", 0)
        column = token.get("column", 0)
        message = f"Expected {expected_type}, got {token['type']}"
        raise SyntaxError(f"{filename}:{line}:{column}: {message}")
    
    # 消费 token
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
# Not required for this parser function node.
