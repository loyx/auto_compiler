# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_assignment(parser_state: ParserState) -> AST:
    """
    解析赋值语句。语法：ident '=' expression ';'
    输入：parser_state（pos 指向 IDENT token）。
    返回：ASSIGNMENT AST 节点。
    副作用：修改 parser_state["pos"] 到赋值语句结束位置。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 记录 IDENT token 的行号列号
    ident_token = tokens[pos]
    line = ident_token["line"]
    column = ident_token["column"]
    
    # 2. 消费 IDENT token，构建目标 AST
    target_token = _consume_token(parser_state, "IDENT")
    target_ast = {
        "type": "IDENTIFIER",
        "value": target_token["value"],
        "line": target_token["line"],
        "column": target_token["column"]
    }
    
    # 3. 消费 ASSIGN token ('=')
    _consume_token(parser_state, "ASSIGN")
    
    # 4. 解析右侧表达式
    value_ast = _parse_expression(parser_state)
    
    # 5. 消费可选的 SEMICOLON
    if parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "SEMICOLON":
            _consume_token(parser_state, "SEMICOLON")
    
    # 6. 返回 ASSIGNMENT AST 节点
    return {
        "type": "ASSIGNMENT",
        "target": target_ast,
        "value": value_ast,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node