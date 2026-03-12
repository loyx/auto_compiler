# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token

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
    """解析表达式语句。输入：parser_state（当前位置指向表达式开始）。
    输出：EXPR_STMT 类型 AST 节点。遇到语法错误抛出 SyntaxError。"""
    # 获取表达式起始位置
    first_token = _peek_token(parser_state)
    if first_token is None:
        raise SyntaxError("Unexpected end of input while parsing expression statement")
    
    line = first_token.get("line", 0)
    column = first_token.get("column", 0)
    filename = parser_state.get("filename", "unknown")
    
    # 解析表达式
    expr_node = _parse_expression(parser_state)
    
    # 验证并消费分号
    token = _peek_token(parser_state)
    if token is None or token.get("type") != "SEMICOLON":
        actual = token.get("type", "EOF") if token else "EOF"
        raise SyntaxError(f"{filename}:{line}:{column}: 期望 ';'，但遇到 '{actual}'")
    
    parser_state = _consume_token(parser_state, "SEMICOLON")
    
    return {
        "type": "EXPR_STMT",
        "children": [expr_node],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
