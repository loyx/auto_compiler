# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 延迟导入以避免循环依赖问题，导入在函数内部进行

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
def _parse_statement(parser_state: dict) -> dict:
    """解析单条语句，根据 token 类型分发到对应的解析子函数。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"{parser_state['filename']}:0:0: Unexpected end of input, expected statement"
        )
    
    token = tokens[pos]
    token_type = token["type"]
    
    # 根据 token 类型分发到对应的解析逻辑
    if token_type in ("VAR", "LET"):
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
        # 其他情况：标识符、字面量等 -> 表达式语句
        return _parse_expr_stmt(parser_state)

# === helper functions ===
# 无 helper 函数，所有逻辑已委派给子函数

# === OOP compatibility layer ===
# 本节点为普通函数节点，无需 OOP wrapper
