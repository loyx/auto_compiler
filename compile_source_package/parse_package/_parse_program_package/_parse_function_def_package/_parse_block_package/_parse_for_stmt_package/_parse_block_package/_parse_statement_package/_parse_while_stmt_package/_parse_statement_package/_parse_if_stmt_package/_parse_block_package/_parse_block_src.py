# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_if_stmt_package._parse_if_stmt_src import _parse_if_stmt
from ._parse_assign_stmt_package._parse_assign_stmt_src import _parse_assign_stmt
from ._parse_return_stmt_package._parse_return_stmt_src import _parse_return_stmt
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
#   "pos": int,
#   "filename": str,
#   "error": str
# }


# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """解析语句块。输入 parser_state（pos 指向 LBRACE），返回 BLOCK AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")

    # 检查当前 token 是否为 LBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望语句块起始 '{{'，但到达文件末尾")
    if tokens[pos]["type"] != "LBRACE":
        raise SyntaxError(
            f"{filename}:{tokens[pos]['line']}:{tokens[pos]['column']}: "
            f"期望语句块起始 '{{'，但得到 '{tokens[pos]['value']}'"
        )

    # 记录 LBRACE 位置并消耗该 token
    block_line = tokens[pos]["line"]
    block_column = tokens[pos]["column"]
    pos += 1

    statements = []

    # 循环解析语句直到 RBRACE 或文件末尾
    while pos < len(tokens) and tokens[pos]["type"] != "RBRACE":
        parser_state["pos"] = pos
        stmt_ast = _parse_statement(parser_state)
        pos = parser_state["pos"]
        statements.append(stmt_ast)

    # 检查是否遇到 RBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{block_line}:{block_column}: 语句块未闭合，缺少 '}}'")

    # 消耗 RBRACE
    pos += 1
    parser_state["pos"] = pos

    return {
        "type": "BLOCK",
        "children": statements,
        "value": None,
        "line": block_line,
        "column": block_column
    }


# === helper functions ===
def _parse_statement(parser_state: ParserState) -> AST:
    """根据当前 token 类型选择并调用相应的语句解析函数。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")

    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: 期望语句，但到达文件末尾")

    token_type = tokens[pos]["type"]

    if token_type == "IF":
        return _parse_if_stmt(parser_state)
    elif token_type == "RETURN":
        return _parse_return_stmt(parser_state)
    elif token_type == "IDENTIFIER":
        # 检查下一个 token 是否为 ASSIGN，判断是否为赋值语句
        if pos + 1 < len(tokens) and tokens[pos + 1]["type"] == "ASSIGN":
            return _parse_assign_stmt(parser_state)
        else:
            return _parse_expr_stmt(parser_state)
    else:
        # 默认作为表达式语句处理
        return _parse_expr_stmt(parser_state)


# === OOP compatibility layer ===
