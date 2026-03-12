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
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句（expr;）。
    如：x = 5; 或 func();
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 记录起始位置的行号和列号
    start_token = tokens[pos] if pos < len(tokens) else {"line": 1, "column": 1}
    start_line = start_token["line"]
    start_column = start_token["column"]
    
    # 调用 _parse_expression 解析表达式
    expr_ast = _parse_expression(parser_state)
    
    # 消费 SEMICOLON
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: expected ';' after expression")
    
    current_token = tokens[pos]
    if current_token["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: expected ';' after expression, got '{current_token['value']}'")
    
    # 消费分号，更新位置
    parser_state["pos"] = pos + 1
    
    # 构建 EXPR_STMT AST 节点
    return {
        "type": "EXPR_STMT",
        "children": [expr_ast],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
