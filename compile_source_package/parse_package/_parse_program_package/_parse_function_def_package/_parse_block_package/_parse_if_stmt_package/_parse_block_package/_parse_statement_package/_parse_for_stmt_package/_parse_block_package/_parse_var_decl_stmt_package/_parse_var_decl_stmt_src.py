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
def _parse_var_decl_stmt(parser_state: dict) -> dict:
    """解析 VAR 变量声明语句：var identifier = expression ;"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 消费 VAR token
    var_token = _expect_token(tokens, pos, "VAR", filename)
    pos += 1
    
    # 消费标识符
    if pos >= len(tokens):
        _raise_error(filename, var_token["line"], var_token["column"], "expected identifier after 'var'")
    ident_token = tokens[pos]
    if ident_token["type"] != "IDENTIFIER":
        _raise_error(filename, ident_token["line"], ident_token["column"], f"expected identifier, got '{ident_token['value']}'")
    var_name = ident_token["value"]
    pos += 1
    
    # 消费 ASSIGN
    if pos >= len(tokens):
        _raise_error(filename, var_token["line"], var_token["column"], "expected '=' after variable name")
    assign_token = tokens[pos]
    if assign_token["type"] != "ASSIGN":
        _raise_error(filename, assign_token["line"], assign_token["column"], f"expected '=', got '{assign_token['value']}'")
    pos += 1
    
    # 解析初始化表达式
    parser_state["pos"] = pos
    initializer_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 消费 SEMICOLON
    if pos >= len(tokens):
        _raise_error(filename, var_token["line"], var_token["column"], "expected ';' after expression")
    semi_token = tokens[pos]
    if semi_token["type"] != "SEMICOLON":
        _raise_error(filename, semi_token["line"], semi_token["column"], f"expected ';', got '{semi_token['value']}'")
    pos += 1
    
    # 更新位置
    parser_state["pos"] = pos
    
    # 返回 VAR_DECL AST 节点
    return {
        "type": "VAR_DECL",
        "name": var_name,
        "initializer": initializer_ast,
        "line": var_token["line"],
        "column": var_token["column"]
    }

# === helper functions ===
def _expect_token(tokens: list, pos: int, expected_type: str, filename: str) -> Token:
    """检查当前位置是否为期望的 token 类型。"""
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: unexpected end of file, expected {expected_type}")
    token = tokens[pos]
    if token["type"] != expected_type:
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: expected {expected_type}, got '{token['value']}'")
    return token

def _raise_error(filename: str, line: int, column: int, message: str) -> None:
    """抛出语法错误。"""
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

# === OOP compatibility layer ===
