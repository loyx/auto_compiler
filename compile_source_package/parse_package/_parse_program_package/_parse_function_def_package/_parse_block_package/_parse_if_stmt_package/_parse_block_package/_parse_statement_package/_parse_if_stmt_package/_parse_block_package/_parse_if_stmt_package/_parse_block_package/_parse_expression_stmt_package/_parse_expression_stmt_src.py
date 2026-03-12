# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
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
def _parse_expression_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句。语法：expression ';'
    
    返回 EXPRESSION_STMT AST 节点：
    {
        "type": "EXPRESSION_STMT",
        "expression": AST,
        "line": int,
        "column": int
    }
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 记录起始位置
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input, expected expression"
        return {"type": "EXPRESSION_STMT", "expression": None, "line": 0, "column": 0}
    
    start_token = tokens[pos]
    start_line = start_token.get("line", 0)
    start_column = start_token.get("column", 0)
    
    # 解析表达式
    expr_ast = _parse_expression(parser_state)
    
    # 检查解析是否失败
    if parser_state.get("error"):
        return {"type": "EXPRESSION_STMT", "expression": None, "line": start_line, "column": start_column}
    
    # 消费可选的分号
    _consume_token(parser_state, "SEMICOLON")
    
    # 返回 EXPRESSION_STMT 节点
    return {
        "type": "EXPRESSION_STMT",
        "expression": expr_ast,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function