# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expr_package._parse_expr_src import _parse_expr

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
    解析赋值语句。
    
    语法：assignment := IDENT ASSIGN expr SEMICOLON
    
    输入：parser_state，pos 指向 IDENT token
    输出：ASSIGNMENT AST 节点
    副作用：更新 parser_state["pos"] 到赋值语句结束后的位置
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 1. 消费 IDENT token（变量名）
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected IDENT")
    
    ident_token = tokens[pos]
    if ident_token["type"] != "IDENT":
        raise SyntaxError(f"Expected IDENT, got {ident_token['type']} at line {ident_token['line']}")
    
    ident_line = ident_token["line"]
    ident_column = ident_token["column"]
    pos += 1
    
    # 2. 消费 ASSIGN token
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected ASSIGN")
    
    assign_token = tokens[pos]
    if assign_token["type"] != "ASSIGN":
        raise SyntaxError(f"Expected ASSIGN, got {assign_token['type']} at line {assign_token['line']}")
    
    pos += 1
    
    # 3. 解析右侧表达式（调用 _parse_expr）
    expr_ast = _parse_expr(parser_state)
    
    # 4. 消费 SEMICOLON token
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected SEMICOLON")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected SEMICOLON, got {semicolon_token['type']} at line {semicolon_token['line']}")
    
    pos += 1
    
    # 更新 parser_state 位置
    parser_state["pos"] = pos
    
    # 5. 构建 ASSIGNMENT AST 节点
    identifier_ast = {
        "type": "IDENTIFIER",
        "value": ident_token["value"],
        "line": ident_line,
        "column": ident_column,
        "children": []
    }
    
    assignment_ast = {
        "type": "ASSIGNMENT",
        "line": ident_line,
        "column": ident_column,
        "children": [identifier_ast, expr_ast]
    }
    
    return assignment_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function nodes