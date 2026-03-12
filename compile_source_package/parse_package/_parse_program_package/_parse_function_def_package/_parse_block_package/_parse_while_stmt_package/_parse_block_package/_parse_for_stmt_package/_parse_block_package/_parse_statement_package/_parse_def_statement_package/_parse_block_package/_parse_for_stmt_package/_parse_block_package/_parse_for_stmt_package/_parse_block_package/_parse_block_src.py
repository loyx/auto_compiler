# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_assign_package._parse_assign_src import _parse_assign
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt
from ._get_indent_level_package._get_indent_level_src import _get_indent_level
from ._is_in_block_package._is_in_block_src import _is_in_block

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int,
#   "indent": int
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
    """解析代码块。代码块由缩进相同的多个语句组成。"""
    tokens = parser_state["tokens"]
    start_pos = parser_state["pos"]
    
    if start_pos >= len(tokens):
        return {"type": "BLOCK", "line": 0, "column": 0, "children": []}
    
    # 获取块的缩进级别
    block_indent = _get_indent_level(parser_state, start_pos)
    start_line = tokens[start_pos]["line"]
    start_column = tokens[start_pos]["column"]
    
    children = []
    
    # 循环解析语句，直到遇到缩进小于块缩进的 token 或文件结束
    while parser_state["pos"] < len(tokens):
        if not _is_in_block(parser_state, parser_state["pos"], block_indent):
            break
        
        # 获取当前 token 类型，分发到相应的解析函数
        current_token = tokens[parser_state["pos"]]
        token_type = current_token["type"]
        token_value = current_token["value"]
        
        stmt_ast = None
        
        if token_type == "KEYWORD" and token_value == "for":
            stmt_ast = _parse_for_stmt(parser_state)
        elif token_type == "KEYWORD" and token_value == "if":
            stmt_ast = _parse_if_stmt(parser_state)
        elif token_type == "IDENTIFIER":
            # 检查是否是赋值（下一个 token 是 ASSIGN）
            if parser_state["pos"] + 1 < len(tokens):
                next_token = tokens[parser_state["pos"] + 1]
                if next_token["type"] == "ASSIGN":
                    stmt_ast = _parse_assign(parser_state)
                else:
                    stmt_ast = _parse_expr_stmt(parser_state)
            else:
                stmt_ast = _parse_expr_stmt(parser_state)
        else:
            # 默认作为表达式语句处理
            stmt_ast = _parse_expr_stmt(parser_state)
        
        if stmt_ast:
            children.append(stmt_ast)
    
    return {
        "type": "BLOCK",
        "line": start_line,
        "column": start_column,
        "children": children
    }

# === helper functions ===
# Helper functions are delegated to sub-function modules

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
