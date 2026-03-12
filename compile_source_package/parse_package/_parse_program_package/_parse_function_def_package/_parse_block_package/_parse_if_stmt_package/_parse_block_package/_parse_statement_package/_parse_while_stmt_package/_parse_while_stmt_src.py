# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
#   "tokens": List[Token],
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """
    解析 while 循环语句。
    语法：while ( condition ) { statement* }
    输入：parser_state（pos 指向 WHILE 关键字）
    输出：WHILE_STMT AST 节点
    """
    tokens: List[Token] = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查 token 是否耗尽
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input while parsing while statement")
    
    # 1. 记录 WHILE 关键字的位置并消费
    while_token = tokens[pos]
    while_line = while_token["line"]
    while_column = while_token["column"]
    parser_state["pos"] = pos + 1
    
    # 2. 消费 LPAREN
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{while_line}:{while_column}: Expected '(' after 'while'")
    lparen_token = tokens[pos]
    if lparen_token["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:{lparen_token['line']}:{lparen_token['column']}: Expected '(' after 'while', got '{lparen_token['value']}'")
    parser_state["pos"] = pos + 1
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消费 RPAREN
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{while_line}:{while_column}: Expected ')' after condition expression")
    rparen_token = tokens[pos]
    if rparen_token["type"] != "RPAREN":
        raise SyntaxError(f"{filename}:{rparen_token['line']}:{rparen_token['column']}: Expected ')' after condition, got '{rparen_token['value']}'")
    parser_state["pos"] = pos + 1
    
    # 5. 解析循环体块
    body_ast = _parse_block(parser_state)
    
    # 6. 构建 WHILE_STMT AST 节点
    return {
        "type": "WHILE_STMT",
        "condition": condition_ast,
        "body": body_ast,
        "line": while_line,
        "column": while_column
    }

# === helper functions ===

# === OOP compatibility layer ===
