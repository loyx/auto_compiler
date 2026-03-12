# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
#   "operator": str,
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

BINARY_OPERATORS = {
    "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO",
    "EQ", "NEQ", "LT", "GT", "LTE", "GTE", "AND", "OR"
}

OPERATOR_MAP = {
    "PLUS": "+", "MINUS": "-", "MULTIPLY": "*", "DIVIDE": "/",
    "MODULO": "%", "EQ": "==", "NEQ": "!=", "LT": "<", "GT": ">",
    "LTE": "<=", "GTE": ">=", "AND": "and", "OR": "or"
}


# === main function ===
def _parse_binop_tail(parser_state: ParserState, left: AST) -> AST:
    """解析二元运算符尾部，构建左结合的二叉表达式树。"""
    tokens = parser_state["tokens"]

    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        token_type = token.get("type", "")

        if token_type not in BINARY_OPERATORS:
            break

        # 消耗运算符 token
        parser_state["pos"] += 1
        op_symbol = OPERATOR_MAP[token_type]
        op_line = token["line"]
        op_column = token["column"]

        # 解析右操作数
        right = _parse_primary_expr(parser_state)

        # 检查是否有错误
        if parser_state.get("error", ""):
            return {
                "type": "ERROR",
                "value": None,
                "line": op_line,
                "column": op_column,
                "children": []
            }

        # 构建 BINOP_EXPR 节点
        left = {
            "type": "BINOP_EXPR",
            "operator": op_symbol,
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }

    return left


# === helper functions ===

# === OOP compatibility layer ===
