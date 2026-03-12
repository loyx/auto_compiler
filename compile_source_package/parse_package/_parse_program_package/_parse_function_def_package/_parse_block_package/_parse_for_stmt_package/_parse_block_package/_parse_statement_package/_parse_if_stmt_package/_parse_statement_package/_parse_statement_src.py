# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_break_stmt_package._parse_break_stmt_src import _parse_break_stmt
from ._parse_continue_stmt_package._parse_continue_stmt_src import _parse_continue_stmt
from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl
from ._parse_block_package._parse_block_src import _parse_block
from ._parse_expr_or_assign_stmt_package._parse_expr_or_assign_stmt_src import _parse_expr_or_assign_stmt

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
#   "type": str,             # 节点类型 (PROGRAM, FUNCTION_DEF, PARAM, VAR_DECL, IF_STMT, WHILE_STMT, FOR_STMT, RETURN_STMT, BREAK_STMT, CONTINUE_STMT, EXPR_STMT, ASSIGN_STMT, EMPTY_STMT, BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, BLOCK)
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
def _parse_statement(parser_state: dict) -> dict:
    """
    解析语句。根据当前 token 类型分发到具体语句解析函数。
    
    输入：parser_state（pos 指向语句起始 token）
    输出：语句 AST 节点（IF_STMT、WHILE_STMT、RETURN_STMT、EXPR_STMT 等）
    副作用：更新 parser_state['pos'] 到语句结束位置
    异常：遇到语法错误抛出 SyntaxError
    """
    current_pos = parser_state["pos"]
    
    if current_pos >= len(parser_state["tokens"]):
        raise SyntaxError("Unexpected end of input while parsing statement")
    
    token_type = parser_state["tokens"][current_pos]["type"]
    token = parser_state["tokens"][current_pos]
    
    if token_type == "IF":
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
    elif token_type == "VAR":
        return _parse_var_decl(parser_state)
    elif token_type == "LBRACE":
        return _parse_block(parser_state)
    elif token_type == "IDENTIFIER":
        return _parse_expr_or_assign_stmt(parser_state)
    elif token_type == "SEMICOLON":
        parser_state["pos"] += 1
        return {
            "type": "EMPTY_STMT",
            "children": [],
            "value": None,
            "line": token["line"],
            "column": token["column"]
        }
    else:
        raise SyntaxError(
            f"Unexpected token '{token['value']}' (type: {token_type}) at line {token['line']}, "
            f"column {token['column']}. Expected a statement."
        )

# === helper functions ===
# No helper functions in this file; _parse_expr_or_assign_stmt is delegated

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node