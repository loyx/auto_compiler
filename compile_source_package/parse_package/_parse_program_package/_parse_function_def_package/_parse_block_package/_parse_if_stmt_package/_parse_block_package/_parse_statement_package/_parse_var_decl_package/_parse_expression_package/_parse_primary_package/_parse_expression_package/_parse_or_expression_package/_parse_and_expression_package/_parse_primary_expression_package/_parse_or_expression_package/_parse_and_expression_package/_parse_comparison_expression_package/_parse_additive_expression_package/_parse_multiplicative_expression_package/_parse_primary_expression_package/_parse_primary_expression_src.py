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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
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
def _parse_primary_expression(parser_state: ParserState) -> AST:
    """解析原子表达式（数字、标识符、括号表达式）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]

    # 空 token 列表或越界
    if pos >= len(tokens):
        parser_state["error"] = "Expected primary expression"
        return {"type": "empty", "line": 0, "column": 0}

    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    token_line = current_token["line"]
    token_column = current_token["column"]

    # 数字
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {"type": "number", "value": token_value, "line": token_line, "column": token_column}

    # 标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {"type": "identifier", "value": token_value, "line": token_line, "column": token_column}

    # 左括号 - 递归解析内部表达式
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # 消费 LPAREN
        inner_ast = _parse_expression(parser_state)

        # 检查内部表达式是否出错
        if parser_state.get("error"):
            return inner_ast

        # 期望右括号
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            parser_state["error"] = "Expected ')'"
            return inner_ast

        next_token = tokens[new_pos]
        if next_token["type"] != "RPAREN":
            parser_state["error"] = "Expected ')'"
            return inner_ast

        # 消费 RPAREN
        parser_state["pos"] += 1
        return inner_ast

    # 无法匹配任何原子表达式
    parser_state["error"] = "Expected primary expression"
    return {"type": "empty", "line": token_line, "column": token_column}


# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# Not needed - this is a parser function, not a framework entry point
