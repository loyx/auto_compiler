# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Using lazy imports to avoid circular dependency
_parse_expression = None
_parse_primary = None


def _get_parse_expression():
    global _parse_expression
    if _parse_expression is None:
        from ._parse_expression_package._parse_expression_src import _parse_expression as _pe
        _parse_expression = _pe
    return _parse_expression


def _get_parse_primary():
    global _parse_primary
    if _parse_primary is None:
        from ._parse_primary_package._parse_primary_src import _parse_primary as _pp
        _parse_primary = _pp
    return _parse_primary

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, MULTI, DIV, MOD, LPAREN, RPAREN, IDENTIFIER, LITERAL, etc.)
#   "value": str,            # token 值 (+, -, *, /, %, (, ), 标识符名，字面量值等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（运算符字符串或标识符/字面量值）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_factor(parser_state: ParserState) -> AST:
    """解析 factor 层级（括号表达式、一元运算符、primary）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)

    # 边界检查：tokens 为空或 pos 越界
    if not tokens or pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input: expected factor"
        return {"type": "ERROR", "value": "Unexpected end of input", "children": [], "line": 0, "column": 0}

    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)

    # 情况 1: LPAREN -> 括号表达式
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1  # 消耗 LPAREN
        expr_ast = _get_parse_expression()(parser_state)

        # 检查是否有 error
        if parser_state.get("error"):
            return expr_ast

        # 期望并消耗 RPAREN
        new_pos = parser_state.get("pos", 0)
        if new_pos >= len(tokens) or tokens[new_pos].get("type") != "RPAREN":
            parser_state["error"] = "Expected ')' after expression"
            return {"type": "ERROR", "value": "Expected ')'", "children": [], "line": token_line, "column": token_column}

        parser_state["pos"] = new_pos + 1  # 消耗 RPAREN
        return expr_ast

    # 情况 2: PLUS 或 MINUS -> 一元运算符
    if token_type in ("PLUS", "MINUS"):
        parser_state["pos"] = pos + 1  # 消耗一元运算符
        operand_ast = _parse_factor(parser_state)

        # 检查是否有 error
        if parser_state.get("error"):
            return operand_ast

        return {
            "type": "UNARY_OP",
            "value": token_value,
            "children": [operand_ast],
            "line": token_line,
            "column": token_column
        }

    # 情况 3: primary
    primary_ast = _get_parse_primary()(parser_state)
    return primary_ast


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
