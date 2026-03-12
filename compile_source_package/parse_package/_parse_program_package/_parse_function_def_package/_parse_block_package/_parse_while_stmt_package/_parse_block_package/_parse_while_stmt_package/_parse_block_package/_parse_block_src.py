# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_block(parser_state: dict) -> dict:
    """解析语句块，返回 BLOCK 类型 AST 节点。"""
    # 获取 LBRACE token 位置信息
    current_token = _peek_token(parser_state)
    block_line = current_token["line"]
    block_column = current_token["column"]
    
    # 消费左大括号
    parser_state = _consume_token(parser_state, "LBRACE")
    
    # 收集语句
    children = []
    
    # 循环解析语句直到遇到 RBRACE
    while True:
        current_token = _peek_token(parser_state)
        
        # 检查是否遇到右大括号
        if current_token is None or current_token["type"] == "RBRACE":
            break
        
        # 解析一条语句
        statement_ast = _parse_statement(parser_state)
        children.append(statement_ast)
    
    # 消费右大括号
    parser_state = _consume_token(parser_state, "RBRACE")
    
    # 返回 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "children": children,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
# No additional helper functions needed; logic is delegated to sub-functions.

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.
