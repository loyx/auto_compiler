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

ForStmtAST = Dict[str, Any]
# ForStmtAST possible fields:
# {
#   "type": "FOR",
#   "variable": str,
#   "iterable": AST,
#   "body": AST,
#   "line": int,
#   "column": int
# }

# === main function ===
def _parse_for_stmt(parser_state: dict) -> dict:
    """
    解析 for 语句。
    
    语法格式：for 变量 in 表达式 语句块
    输入：parser_state（pos 指向 FOR token）
    输出：FOR 类型 AST 节点
    """
    # 消费 FOR token，记录起始位置
    for_token = _consume_token(parser_state, "FOR")
    start_line = for_token["line"]
    start_column = for_token["column"]
    
    # 解析变量名标识符
    var_token = _consume_token(parser_state, "IDENTIFIER")
    variable_name = var_token["value"]
    
    # 消费 IN token
    _consume_token(parser_state, "IN")
    
    # 解析可迭代表达式
    iterable_ast = _parse_expr_stmt(parser_state)
    
    # 解析语句块
    body_ast = _parse_block(parser_state)
    
    # 构建 FOR AST 节点
    return {
        "type": "FOR",
        "variable": variable_name,
        "iterable": iterable_ast,
        "body": body_ast,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
