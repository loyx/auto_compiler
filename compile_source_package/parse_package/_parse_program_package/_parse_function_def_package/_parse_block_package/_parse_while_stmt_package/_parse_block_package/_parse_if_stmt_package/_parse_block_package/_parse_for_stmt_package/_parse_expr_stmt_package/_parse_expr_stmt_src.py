# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# only import child functions
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
# define the data structures used between parent and child functions
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
    语法格式：表达式 ;
    输入：parser_state（pos 指向表达式起始 token）
    输出：EXPR_STMT 类型 AST 节点
    
    AST 节点结构：
    {
        "type": "EXPR_STMT",
        "expression": AST,  # 表达式 AST 节点
        "line": int,
        "column": int
    }
    """
    # 记录起始位置（从表达式第一个 token 获取）
    tokens = parser_state["tokens"]
    current_pos = parser_state["pos"]
    
    # 检查是否有 token 可解析
    if current_pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input at {parser_state['filename']}"
        )
    
    start_token = tokens[current_pos]
    start_line = start_token["line"]
    start_column = start_token["column"]
    
    # 解析表达式
    expression_ast = _parse_expression(parser_state)
    
    # 消费分号
    _consume_token(parser_state, "SEMICOLON")
    
    # 构建 EXPR_STMT AST 节点
    return {
        "type": "EXPR_STMT",
        "expression": expression_ast,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# 本函数逻辑简单，无需额外 helper 函数

# === OOP compatibility layer ===
# 本函数为解析器内部函数，无需 OOP wrapper