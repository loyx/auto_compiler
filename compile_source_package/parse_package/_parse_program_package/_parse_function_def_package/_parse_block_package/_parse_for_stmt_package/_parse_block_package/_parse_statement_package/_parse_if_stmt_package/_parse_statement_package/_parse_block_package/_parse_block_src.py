# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._expect_token_package._expect_token_src import _expect_token
from ._parse_statement_package._parse_statement_src import _parse_statement

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
#   "type": str,             # BLOCK
#   "children": list,        # [statement_ast, ...] 语句列表
#   "value": str,            # "{"
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
    """解析代码块 { statement* }。
    
    输入 parser_state（pos 指向 LBRACE token），返回 BLOCK AST 节点。
    副作用：更新 pos 到代码块结束（RBRACE 之后）。
    异常：语法错误抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    lbrace_token = _expect_token(parser_state, "LBRACE")
    
    children = []
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "RBRACE":
            break
        stmt_ast = _parse_statement(parser_state)
        children.append(stmt_ast)
    
    _expect_token(parser_state, "RBRACE")
    
    return {
        "type": "BLOCK",
        "children": children,
        "value": None,
        "line": lbrace_token["line"],
        "column": lbrace_token["column"]
    }

# === helper functions ===

# === OOP compatibility layer ===
