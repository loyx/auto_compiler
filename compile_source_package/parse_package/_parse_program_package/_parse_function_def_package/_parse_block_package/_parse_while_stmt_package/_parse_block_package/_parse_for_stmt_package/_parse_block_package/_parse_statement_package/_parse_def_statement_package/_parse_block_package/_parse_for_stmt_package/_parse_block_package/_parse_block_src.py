# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_assign_stmt_package._parse_assign_stmt_src import _parse_assign_stmt
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt

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
def _parse_block(parser_state: ParserState) -> AST:
    """解析语句块。输入 pos 指向 COLON token，输出 BLOCK AST 节点。"""
    tokens = parser_state["tokens"]
    
    # 1. 消费 COLON token（块起始标记）
    colon_token = _consume_token(parser_state, "COLON")
    block_line = colon_token["line"]
    block_column = colon_token["column"]
    
    # 2. 循环解析语句，直到遇到 SEMICOLON
    statements = []
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        current_type = current_token["type"]
        
        # 3. 检查是否遇到块结束标记
        if current_type == "SEMICOLON":
            break
        
        # 4. 根据语句类型调用相应的解析函数
        if current_type == "FOR":
            stmt_ast = _parse_for_stmt(parser_state)
        elif current_type == "IF":
            stmt_ast = _parse_if_stmt(parser_state)
        elif current_type == "WHILE":
            stmt_ast = _parse_while_stmt(parser_state)
        elif current_type == "IDENTIFIER":
            stmt_ast = _parse_assign_stmt(parser_state)
        elif current_type in ("RETURN",):
            stmt_ast = _parse_return_stmt(parser_state)
        elif current_type in ("BREAK",):
            stmt_ast = _parse_break_stmt(parser_state)
        elif current_type in ("CONTINUE",):
            stmt_ast = _parse_continue_stmt(parser_state)
        else:
            # 默认为表达式语句
            stmt_ast = _parse_expr_stmt(parser_state)
        
        statements.append(stmt_ast)
    
    # 5. 消费 SEMICOLON（块结束标记）
    if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected SEMICOLON at end of block in {parser_state.get('filename', 'unknown')}")
    _consume_token(parser_state, "SEMICOLON")
    
    # 6. 构建 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "line": block_line,
        "column": block_column,
        "children": statements
    }

# === helper functions ===

# === OOP compatibility layer ===
