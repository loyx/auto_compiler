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
def _parse_paren_expression(parser_state: ParserState, start_line: int, start_column: int) -> AST:
    """
    解析括号表达式 (...) 并构建 paren_expression AST 节点。
    
    前置条件：parser_state['pos'] 已指向 '(' 之后的内部表达式起始 token。
    """
    # 1. 解析括号内的完整表达式
    inner_expr = _parse_expression(parser_state)
    
    # 2. 检查当前 token 是否为 RPAREN
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Missing ')' in {parser_state.get('filename', '<unknown>')}:"
            f"{start_line}:{start_column}"
        )
    
    current_token = tokens[pos]
    if current_token.get("type") != "RPAREN":
        raise SyntaxError(
            f"Expected ')' but found '{current_token.get('value')}' in "
            f"{parser_state.get('filename', '<unknown>')}:{start_line}:{start_column}"
        )
    
    # 3. 消费 RPAREN
    parser_state["pos"] = pos + 1
    
    # 4. 构建并返回 paren_expression AST 节点
    return {
        "type": "paren_expression",
        "value": None,
        "children": [inner_expr],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for parser function nodes