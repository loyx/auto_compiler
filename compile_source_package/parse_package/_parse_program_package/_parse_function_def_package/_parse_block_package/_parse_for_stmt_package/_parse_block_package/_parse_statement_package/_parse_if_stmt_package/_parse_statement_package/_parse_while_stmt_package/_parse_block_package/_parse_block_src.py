# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_statement_package._parse_statement_src import _parse_statement

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,           # 必填，大写字母串如 "LBRACE", "RBRACE", "WHILE"
#   "value": str,          # 可选，原始字符值如 "{", "}", "while"
#   "line": int,           # 必填，行号从 1 开始
#   "column": int          # 必填，列号从 1 开始
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,           # 节点类型如 "BLOCK", "WHILE_STMT"
#   "children": list,      # 子 AST 节点列表
#   "value": str,          # 可选，原始值如 "{"
#   "line": int,           # 必填，起始 token 行号
#   "column": int          # 必填，起始 token 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,        # Token 列表
#   "pos": int,            # 当前解析位置索引
#   "filename": str,       # 源文件名
#   "error": str           # 不使用，错误通过异常抛出
# }

# === main function ===
def _parse_block(parser_state: ParserState) -> AST:
    """
    解析代码块。
    语法：block := "{" statement* "}"
    输入：parser_state（pos 指向 LBRACE token）
    输出：BLOCK AST 节点，包含所有语句子节点
    副作用：更新 parser_state['pos'] 到块结束（RBRACE 之后）
    异常：语法错误抛出 SyntaxError
    """
    # 1. 消耗 LBRACE token
    lbrace_token = _expect_token(parser_state, "LBRACE")
    
    # 2. 记录 LBRACE 位置用于 BLOCK AST
    block_line = lbrace_token["line"]
    block_column = lbrace_token["column"]
    
    # 3. 循环解析语句
    children = []
    while True:
        current_token = _peek_token(parser_state)
        if current_token is None:
            raise SyntaxError(
                f"Unexpected end of file, expected '}}', at line {block_line}, column {block_column}"
            )
        if current_token["type"] == "RBRACE":
            break
        # 解析语句（委托给子函数）
        stmt_ast = _parse_statement(parser_state)
        children.append(stmt_ast)
    
    # 4. 消耗 RBRACE token
    _expect_token(parser_state, "RBRACE")
    
    # 5. 构建并返回 BLOCK AST 节点
    return {
        "type": "BLOCK",
        "children": children,
        "value": "{",
        "line": block_line,
        "column": block_column
    }

# === helper functions ===
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    期望当前 token 为指定类型，若是则消耗并返回该 token。
    异常：若不是期望类型，抛出 SyntaxError
    """
    token = _peek_token(parser_state)
    if token is None:
        raise SyntaxError(
            f"Unexpected end of file, expected '{token_type}'"
        )
    if token["type"] != token_type:
        raise SyntaxError(
            f"Unexpected token '{token['type']}', expected '{token_type}', "
            f"at line {token['line']}, column {token['column']}"
        )
    # 消耗 token
    parser_state["pos"] += 1
    return token

def _peek_token(parser_state: ParserState) -> Token:
    """
    查看当前 token 但不消耗。
    返回：当前 Token 或 None（若已到达末尾）
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return None
    return tokens[pos]

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
