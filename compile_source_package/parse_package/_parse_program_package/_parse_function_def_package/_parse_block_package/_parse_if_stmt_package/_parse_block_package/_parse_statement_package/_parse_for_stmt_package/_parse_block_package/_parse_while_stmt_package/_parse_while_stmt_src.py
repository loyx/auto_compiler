# === std / third-party imports ===
from typing import Any, Dict

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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """解析 WHILE 语句。
    
    WHILE 语句语法：while ( expression ) block
    输入：parser_state（pos 指向 WHILE token）
    输出：WHILE AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 获取 WHILE token 的位置信息
    while_token = tokens[pos]
    line = while_token.get("line", 0)
    column = while_token.get("column", 0)
    
    # 1. 消费 WHILE token
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 2. 消费 LPAREN
    if pos >= len(tokens) or tokens[pos].get("type") != "LPAREN":
        raise SyntaxError(f"{filename}:{line}:{column}: expected '(' after 'while'")
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 4. 消费 RPAREN
    if pos >= len(tokens) or tokens[pos].get("type") != "RPAREN":
        raise SyntaxError(f"{filename}:{line}:{column}: expected ')' after while condition")
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # 5. 解析循环体块
    body_ast = _parse_block(parser_state)
    
    # 6. 返回 WHILE AST 节点
    return {
        "type": "WHILE",
        "condition": condition_ast,
        "body": body_ast,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function