# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_assign_stmt(parser_state: ParserState) -> AST:
    """解析赋值语句：LET IDENTIFIER EQUALS expression SEMICOLON."""
    # 1. 消费 LET 关键字
    let_token = _expect_token(parser_state, "LET")
    
    # 2. 消费标识符
    ident_token = _expect_token(parser_state, "IDENTIFIER")
    ident_ast = {
        "type": "IDENTIFIER",
        "value": ident_token["value"],
        "line": ident_token["line"],
        "column": ident_token["column"],
        "children": []
    }
    
    # 3. 消费 EQUALS 运算符
    _expect_token(parser_state, "EQUALS")
    
    # 4. 解析右侧表达式（委托给子函数）
    expr_ast = _parse_expression(parser_state)
    
    # 5. 消费 SEMICOLON 结束标记
    _expect_token(parser_state, "SEMICOLON")
    
    # 6. 构建 ASSIGN AST 节点
    return {
        "type": "ASSIGN",
        "line": let_token["line"],
        "column": let_token["column"],
        "children": [ident_ast, expr_ast]
    }

# === helper functions ===
def _expect_token(parser_state: ParserState, expected_type: str) -> Token:
    """消费期望类型的 token，否则抛出 SyntaxError。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    
    token = tokens[pos]
    if token["type"] != expected_type:
        raise SyntaxError(
            f"Expected {expected_type}, got {token['type']} "
            f"at line {token['line']}, column {token['column']}"
        )
    
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
