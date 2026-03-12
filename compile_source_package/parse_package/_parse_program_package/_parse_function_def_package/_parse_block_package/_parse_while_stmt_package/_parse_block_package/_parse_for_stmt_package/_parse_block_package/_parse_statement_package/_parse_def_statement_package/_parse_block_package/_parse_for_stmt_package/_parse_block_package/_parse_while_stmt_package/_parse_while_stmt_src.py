# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
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
    """解析 while 语句。输入 pos 指向 WHILE token，输出 WHILE_STMT AST 节点。"""
    tokens = parser_state["tokens"]
    
    # 1. 消费 WHILE token
    while_token = _consume_token(parser_state, "WHILE")
    stmt_line = while_token["line"]
    stmt_column = while_token["column"]
    
    # 2. 解析条件表达式
    condition_ast = _parse_expr_stmt(parser_state)
    
    # 3. 验证并消费 COLON token
    if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] != "COLON":
        raise SyntaxError(f"Expected COLON after while condition at line {stmt_line}")
    _consume_token(parser_state, "COLON")
    
    # 4. 解析循环体
    body_ast = _parse_block(parser_state)
    
    # 5. 构建 WHILE_STMT AST 节点
    return {
        "type": "WHILE_STMT",
        "line": stmt_line,
        "column": stmt_column,
        "children": [condition_ast, body_ast]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
