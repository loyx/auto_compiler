# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._expect_token_package._expect_token_src import _expect_token
from ._parse_identifier_package._parse_identifier_src import _parse_identifier
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
def _parse_for_stmt(parser_state: dict) -> dict:
    """解析 for 语句，返回 FOR_STMT 类型 AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file in for statement")
    
    for_token = tokens[pos]
    stmt_line = for_token.get("line", 0)
    stmt_column = for_token.get("column", 0)
    
    # 1. 消费 FOR 关键字
    _expect_token(parser_state, "KEYWORD", "for")
    
    # 2. 解析迭代器标识符
    iterator_node = _parse_identifier(parser_state)
    
    # 3. 消费 IN 关键字
    _expect_token(parser_state, "KEYWORD", "in")
    
    # 4. 解析可迭代表达式
    iterable_node = _parse_expression(parser_state)
    
    # 5. 解析循环体块
    body_node = _parse_block(parser_state)
    
    # 构建 FOR_STMT AST 节点
    for_stmt_node = {
        "type": "FOR_STMT",
        "children": [iterator_node, iterable_node, body_node],
        "line": stmt_line,
        "column": stmt_column
    }
    
    return for_stmt_node

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for parser function nodes
