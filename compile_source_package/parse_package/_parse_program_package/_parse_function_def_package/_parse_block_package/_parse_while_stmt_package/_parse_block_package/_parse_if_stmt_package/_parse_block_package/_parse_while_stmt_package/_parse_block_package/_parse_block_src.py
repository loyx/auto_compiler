# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 获取起始位置信息
    start_line = tokens[pos]["line"] if pos < len(tokens) else 0
    start_column = tokens[pos]["column"] if pos < len(tokens) else 0
    
    # 可选：消费 LBRACE
    _consume_token(parser_state, "LBRACE")
    
    # 收集语句
    statements = []
    
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # 检查块结束条件
        if current_token["type"] == "RBRACE":
            break
        
        # 解析当前语句
        stmt_ast = _parse_statement(parser_state)
        if stmt_ast:
            statements.append(stmt_ast)
        
        # 防止无限循环：如果 pos 没有前进，则退出
        if parser_state["pos"] == pos:
            break
        pos = parser_state["pos"]
    
    # 可选：消费 RBRACE
    _consume_token(parser_state, "RBRACE")
    
    # 构建 BLOCK AST 节点
    block_ast = {
        "type": "BLOCK",
        "children": statements,
        "line": start_line,
        "column": start_column
    }
    
    return block_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
