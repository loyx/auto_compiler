# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._expect_token_package._expect_token_src import _expect_token
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
#   "type": str,             # WHILE_STMT
#   "children": list,        # [condition_ast, body_block_ast]
#   "value": str,            # "while"
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
def _parse_while_stmt(parser_state: dict) -> dict:
    """
    解析 while 语句。
    语法：while ( expression ) block
    """
    # 记录 WHILE token 位置信息
    while_token = parser_state["tokens"][parser_state["pos"]]
    line = while_token.get("line", 0)
    column = while_token.get("column", 0)
    
    # 1. 消耗 WHILE token
    _expect_token(parser_state, "WHILE")
    
    # 2. 消耗 LPAREN token
    _expect_token(parser_state, "LPAREN")
    
    # 3. 解析条件表达式
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消耗 RPAREN token
    _expect_token(parser_state, "RPAREN")
    
    # 5. 解析循环体代码块
    body_block_ast = _parse_block(parser_state)
    
    # 6. 构建 WHILE_STMT AST 节点
    ast_node: AST = {
        "type": "WHILE_STMT",
        "children": [condition_ast, body_block_ast],
        "value": "while",
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function