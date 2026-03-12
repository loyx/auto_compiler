# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_var_decl_package._parse_var_decl_src import _parse_var_decl
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
from ._parse_block_package._parse_block_src import _parse_block
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
#   "type": str,             # e.g., VAR_DECL, IF_STMT, FOR_STMT, etc.
#   "children": list,        # child AST nodes
#   "value": str,            # token value
#   "line": int,             # source line number
#   "column": int            # source column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position in tokens
#   "filename": str,         # source filename
#   "error": str             # error message (if any)
# }

# === main function ===
def _parse_statement(parser_state: ParserState) -> AST:
    """
    解析一条语句。根据当前 token 类型分发到不同的语句解析逻辑。
    
    Args:
        parser_state: 解析器状态，pos 指向语句起始 token。
    
    Returns:
        语句 AST 节点（type 为具体语句类型）。
    
    Side effects:
        更新 parser_state["pos"] 到语句结束位置。
    
    Raises:
        SyntaxError: 语法错误时抛出。
    """
    current = _current_token(parser_state)
    token_type = current["type"]
    
    if token_type in ("VAR", "LET", "CONST"):
        return _parse_var_decl(parser_state)
    elif token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif token_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "LBRACE":
        return _parse_block(parser_state)
    else:
        return _parse_expr_stmt(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token，若到达文件末尾则抛出 SyntaxError。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(f"Unexpected end of file at {filename}")
    return tokens[pos]

def _advance(parser_state: ParserState) -> None:
    """向前移动 pos 一个位置。"""
    parser_state["pos"] += 1

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node.
