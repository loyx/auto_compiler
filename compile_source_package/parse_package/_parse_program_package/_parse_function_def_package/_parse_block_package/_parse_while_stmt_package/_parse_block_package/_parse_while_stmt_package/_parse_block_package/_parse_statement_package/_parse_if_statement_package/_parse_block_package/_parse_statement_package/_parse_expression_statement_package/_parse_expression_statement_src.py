# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._peek_token_package._peek_token_src import _peek_token

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
#   "error": str | None
# }

# === main function ===
def _parse_expression_statement(parser_state: ParserState) -> AST:
    """
    解析表达式语句并返回 EXPRESSION_STATEMENT AST 节点。
    原地修改 parser_state（推进 pos）。
    """
    # 获取当前 token 的 line/column 用于 AST 节点
    current_token = _peek_token(parser_state)
    if current_token is None:
        raise SyntaxError("Unexpected end of input at expression statement")
    
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # 解析表达式
    expression_ast = _parse_expression(parser_state)
    
    # 消费 SEMICOLON
    _consume_token(parser_state, "SEMICOLON")
    
    # 返回 AST
    return {
        "type": "EXPRESSION_STATEMENT",
        "expression": expression_ast,
        "line": line,
        "column": column
    }

# === helper functions ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    内联实现：解析表达式。
    这是一个简化版本，实际可能需要更复杂的表达式解析逻辑。
    """
    # 获取当前 token
    current_token = _peek_token(parser_state)
    if current_token is None:
        raise SyntaxError("Unexpected end of input in expression")
    
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # 简化实现：消费一个 token 作为表达式
    # 实际实现可能需要递归下降解析等更复杂的逻辑
    token = _consume_token(parser_state, current_token.get("type", ""))
    
    return {
        "type": "EXPRESSION",
        "value": token.get("value"),
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
