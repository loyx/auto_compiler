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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句。
    
    表达式语句语法：expr_stmt := expr SEMICOLON
    
    输入：parser_state（pos 指向表达式起始 token）
    输出：EXPR_STMT AST 节点
    副作用：更新 parser_state['pos'] 到表达式语句结束后的位置
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 记录表达式起始位置
    start_line = tokens[pos]["line"] if pos < len(tokens) else 0
    start_column = tokens[pos]["column"] if pos < len(tokens) else 0
    
    # 1. 解析表达式
    expr_ast = _parse_expr(parser_state)
    
    # 2. 消费 SEMICOLON token
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"Expected SEMICOLON, found end of file")
    
    current_token = tokens[pos]
    if current_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"Expected SEMICOLON, found {current_token['type']} "
            f"at line {current_token['line']}, column {current_token['column']}"
        )
    
    # 消费 SEMICOLON
    parser_state["pos"] = pos + 1
    
    # 3. 构建 EXPR_STMT AST 节点
    return {
        "type": "EXPR_STMT",
        "line": start_line,
        "column": start_column,
        "children": [expr_ast]
    }

# === helper functions ===
# (none needed - logic is simple enough)

# === OOP compatibility layer ===
# (not needed - this is a parser helper function, not a framework entry point)
