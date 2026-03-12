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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句。
    
    表达式语句语法：expression SEMICOLON
    注意：本函数不消费 SEMICOLON，由调用者处理。
    
    输入：parser_state（pos 指向表达式起始 token）
    输出：EXPR_STMT AST 节点
    副作用：修改 parser_state["pos"] 到表达式结束位置
    异常：语法错误时抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 检查是否有 token 可解析
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected expression")
    
    # 记录起始位置
    start_token = tokens[pos]
    start_line = start_token.get("line", 0)
    start_column = start_token.get("column", 0)
    
    # 解析表达式
    expression_ast = _parse_expression(parser_state)
    
    # 构建 EXPR_STMT AST 节点
    expr_stmt_node: AST = {
        "type": "EXPR_STMT",
        "expression": expression_ast,
        "line": start_line,
        "column": start_column
    }
    
    return expr_stmt_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function