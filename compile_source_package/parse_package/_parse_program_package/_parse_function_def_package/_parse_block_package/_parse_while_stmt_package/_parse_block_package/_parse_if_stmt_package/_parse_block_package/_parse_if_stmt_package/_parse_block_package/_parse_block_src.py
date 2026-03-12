# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_var_stmt_package._parse_var_stmt_src import _parse_var_stmt
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt

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
def _parse_block(parser_state: ParserState) -> AST:
    """解析语句块并返回 BLOCK AST 节点。"""
    # 1. 消费 LBRACE
    lbrace_token = _consume_token(parser_state, "LBRACE")
    block_line = lbrace_token["line"]
    block_column = lbrace_token["column"]
    
    # 2. 循环解析语句直到 RBRACE
    statements = []
    while True:
        # 检查是否到达 RBRACE
        current_pos = parser_state["pos"]
        tokens = parser_state["tokens"]
        
        if current_pos >= len(tokens):
            raise SyntaxError("Unexpected end of input, expected '}'")
        
        current_token = tokens[current_pos]
        if current_token["type"] == "RBRACE":
            break
        
        # 3. 根据 token 类型分发到不同语句解析器
        stmt_type = current_token["type"]
        if stmt_type == "IF":
            stmt_ast = _parse_if_stmt(parser_state)
        elif stmt_type == "WHILE":
            stmt_ast = _parse_while_stmt(parser_state)
        elif stmt_type == "RETURN":
            stmt_ast = _parse_return_stmt(parser_state)
        elif stmt_type == "VAR":
            stmt_ast = _parse_var_stmt(parser_state)
        else:
            # 默认为表达式语句
            stmt_ast = _parse_expr_stmt(parser_state)
        
        statements.append(stmt_ast)
    
    # 4. 消费 RBRACE
    _consume_token(parser_state, "RBRACE")
    
    # 5. 返回 BLOCK 节点
    return {
        "type": "BLOCK",
        "children": statements,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a parser helper function
