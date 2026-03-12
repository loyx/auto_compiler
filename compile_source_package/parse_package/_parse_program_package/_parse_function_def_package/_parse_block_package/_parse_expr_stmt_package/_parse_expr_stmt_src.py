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
def _parse_expr_stmt(parser_state: dict) -> dict:
    """解析表达式语句。
    
    输入：parser_state（当前位置指向表达式起始 token）
    输出：EXPR_STMT 类型 AST 节点
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected expression")
    
    # 记录起始位置
    start_line = tokens[pos]["line"]
    start_column = tokens[pos]["column"]
    
    # 解析表达式
    expr_node = _parse_expression(parser_state)
    
    # 消费可选的分号
    pos = parser_state["pos"]
    if pos < len(tokens) and tokens[pos]["type"] == "SEMICOLON":
        parser_state["pos"] = pos + 1
    
    # 构建 EXPR_STMT 节点
    return {
        "type": "EXPR_STMT",
        "children": [expr_node],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===
