# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
from ._parse_expr_stmt_package._parse_expr_stmt_src import _parse_expr_stmt

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_statement(parser_state: ParserState) -> AST:
    """
    解析单条语句的分发器。
    
    根据当前 token 类型路由到具体的语句解析函数。
    原地更新 parser_state["pos"] 到语句结束后的位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing statement")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # 路由到具体解析函数
    if token_type in ("LET", "VAR"):
        return _parse_var_decl(parser_state)
    elif token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "BREAK":
        return _parse_break_stmt(parser_state)
    elif token_type == "CONTINUE":
        return _parse_continue_stmt(parser_state)
    else:
        # 默认为表达式语句
        return _parse_expr_stmt(parser_state)

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a parser internal function