# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_for_stmt_package._parse_for_stmt_src import _parse_for_stmt
from ._parse_expression_stmt_package._parse_expression_stmt_src import _parse_expression_stmt
from ._parse_while_stmt_package._parse_while_stmt_src import _parse_while_stmt
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
def _parse_block(parser_state: dict) -> dict:
    """
    解析代码块。
    输入：parser_state（pos 指向 LBRACE token）
    处理：消费 LBRACE，循环解析语句直到 RBRACE，消费 RBRACE
    副作用：修改 parser_state["pos"] 指向 RBRACE 后的下一个 token
    返回：BLOCK AST 节点
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 获取 LBRACE token
    lbrace_token = _current_token(parser_state)
    if lbrace_token["type"] != "LBRACE":
        raise SyntaxError(
            f"{filename}:{lbrace_token['line']}:{lbrace_token['column']}: 期望 LBRACE"
        )
    
    block_line = lbrace_token["line"]
    block_column = lbrace_token["column"]
    parser_state["pos"] += 1  # 消费 LBRACE
    
    statements = []
    
    # 循环解析语句直到 RBRACE
    while True:
        token = _current_token(parser_state)
        
        if token["type"] == "RBRACE":
            parser_state["pos"] += 1  # 消费 RBRACE
            break
        
        if token["type"] == "EOF":
            raise SyntaxError(
                f"{filename}:{token['line']}:{token['column']}: 未闭合的代码块"
            )
        
        # 根据 token type 分派语句解析器
        stmt_ast = _dispatch_statement(parser_state, token)
        statements.append(stmt_ast)
    
    return {
        "type": "BLOCK",
        "children": statements,
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
def _current_token(parser_state: dict) -> Token:
    """获取当前位置的 token，越界时返回 EOF token。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": -1, "column": -1}
    return tokens[pos]


def _dispatch_statement(parser_state: dict, token: Token) -> AST:
    """根据 token type 分派到相应的语句解析器。"""
    stmt_type = token["type"]
    
    if stmt_type == "IF":
        return _parse_if_stmt(parser_state)
    elif stmt_type == "FOR":
        return _parse_for_stmt(parser_state)
    elif stmt_type == "WHILE":
        return _parse_while_stmt(parser_state)
    elif stmt_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif stmt_type == "BREAK":
        return _parse_break_stmt(parser_state)
    elif stmt_type == "CONTINUE":
        return _parse_continue_stmt(parser_state)
    elif stmt_type == "LBRACE":
        # 嵌套代码块，递归调用自身
        return _parse_block(parser_state)
    else:
        # 默认作为表达式语句
        return _parse_expression_stmt(parser_state)

# === OOP compatibility layer ===
