# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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
def _parse_for_stmt(parser_state: ParserState) -> AST:
    """
    解析 for 语句，语法：for (var in iterable) { ... }
    输入 parser_state（pos 指向 FOR token），输出 FOR_STMT AST 节点。
    原地更新 parser_state["pos"] 到语句结束位置之后。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 步骤 1: 消耗 FOR token
    if pos >= len(tokens) or tokens[pos]["type"] != "FOR":
        _raise_syntax_error(filename, tokens, pos, "期望 'for' 关键字")
    for_token = tokens[pos]
    pos += 1
    
    # 步骤 2: 期望并消耗 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        _raise_syntax_error(filename, tokens, pos, "期望 '('")
    pos += 1
    
    # 步骤 3: 期望 IDENT token 作为迭代变量名
    if pos >= len(tokens) or tokens[pos]["type"] != "IDENT":
        _raise_syntax_error(filename, tokens, pos, "期望循环变量名")
    var_name = tokens[pos]["value"]
    pos += 1
    
    # 步骤 4: 期望 IN token
    if pos >= len(tokens) or tokens[pos]["type"] != "IN":
        _raise_syntax_error(filename, tokens, pos, "期望 'in' 关键字")
    pos += 1
    
    # 步骤 5: 解析可迭代对象表达式
    parser_state["pos"] = pos
    iterable_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 6: 期望并消耗 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        _raise_syntax_error(filename, tokens, pos, "期望 ')'")
    pos += 1
    
    # 步骤 7: 解析循环体块
    parser_state["pos"] = pos
    body_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 步骤 8: 返回 FOR_STMT AST 节点
    result = {
        "type": "FOR_STMT",
        "var_name": var_name,
        "iterable": iterable_ast,
        "body": body_ast,
        "line": for_token["line"],
        "column": for_token["column"]
    }
    
    parser_state["pos"] = pos
    return result

# === helper functions ===
def _raise_syntax_error(filename: str, tokens: list, pos: int, message: str) -> None:
    """抛出语法错误异常。"""
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 1)
        column = token.get("column", 1)
    else:
        line = 1
        column = 1
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

# === OOP compatibility layer ===
# Not needed for this parser function
