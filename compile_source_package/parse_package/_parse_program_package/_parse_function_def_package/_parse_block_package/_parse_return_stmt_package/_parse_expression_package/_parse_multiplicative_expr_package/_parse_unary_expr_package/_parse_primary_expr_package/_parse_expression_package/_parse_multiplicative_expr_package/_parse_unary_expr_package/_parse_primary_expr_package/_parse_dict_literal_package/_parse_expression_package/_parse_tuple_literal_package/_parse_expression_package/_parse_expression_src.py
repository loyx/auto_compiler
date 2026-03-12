# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_tuple_literal_package._parse_tuple_literal_src import _parse_tuple_literal
from ._parse_number_literal_package._parse_number_literal_src import _parse_number_literal
from ._parse_string_literal_package._parse_string_literal_src import _parse_string_literal
from ._parse_identifier_package._parse_identifier_src import _parse_identifier
from ._parse_unary_expression_package._parse_unary_expression_src import _parse_unary_expression
from ._parse_binary_expression_package._parse_binary_expression_src import _parse_binary_expression

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    表达式解析的入口函数。根据当前 token 类型分发到具体的解析函数。
    输入：parser_state（当前位置应在表达式起始处）
    输出：表达式的 AST 节点
    副作用：推进 parser_state["pos"] 到表达式结束位置
    异常：语法错误时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file while parsing expression in {filename}")
    
    token = tokens[pos]
    token_type = token.get("type", "")
    line = token.get("line", "?")
    column = token.get("column", "?")
    
    # 根据 token 类型分发到具体解析函数
    if token_type == "LEFT_PAREN":
        return _parse_tuple_literal(parser_state)
    elif token_type == "NUMBER":
        return _parse_number_literal(parser_state)
    elif token_type == "STRING":
        return _parse_string_literal(parser_state)
    elif token_type == "IDENTIFIER":
        return _parse_identifier(parser_state)
    elif token_type == "TRUE":
        return _parse_bool_literal(parser_state, True)
    elif token_type == "FALSE":
        return _parse_bool_literal(parser_state, False)
    elif token_type == "NONE":
        return _parse_none_literal(parser_state)
    elif token_type in ("PLUS", "MINUS", "NOT"):
        return _parse_unary_expression(parser_state)
    else:
        # 可能是二元表达式的左操作数起始，尝试解析二元表达式
        # 这里先尝试解析一个原子表达式，然后检查是否有二元运算符
        return _parse_binary_expression(parser_state)

# === helper functions ===
def _parse_bool_literal(parser_state: ParserState, value: bool) -> AST:
    """解析布尔字面量（TRUE/FALSE）。"""
    token = parser_state["tokens"][parser_state["pos"]]
    parser_state["pos"] += 1
    return {
        "type": "BOOL_LITERAL",
        "value": value,
        "line": token.get("line", 0),
        "column": token.get("column", 0)
    }

def _parse_none_literal(parser_state: ParserState) -> AST:
    """解析 None 字面量。"""
    token = parser_state["tokens"][parser_state["pos"]]
    parser_state["pos"] += 1
    return {
        "type": "NONE_LITERAL",
        "value": None,
        "line": token.get("line", 0),
        "column": token.get("column", 0)
    }

# === OOP compatibility layer ===
