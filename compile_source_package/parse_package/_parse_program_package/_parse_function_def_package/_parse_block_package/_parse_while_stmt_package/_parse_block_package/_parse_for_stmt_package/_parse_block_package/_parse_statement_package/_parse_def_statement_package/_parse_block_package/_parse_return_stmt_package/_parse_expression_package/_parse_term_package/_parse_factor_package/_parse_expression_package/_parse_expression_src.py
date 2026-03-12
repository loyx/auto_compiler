# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析表达式（expression）。
    expression := term (('+' | '-') term)*
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    # 解析第一个 term
    left_ast = _parse_term(parser_state)
    
    # 循环处理 '+' 或 '-' 运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 消费运算符
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # 解析右侧 term
        right_ast = _parse_term(parser_state)
        
        # 构建二元运算符 AST 节点
        left_ast = {
            "type": "BINARY_OP",
            "operator": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left_ast


# === helper functions ===
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    期望当前 token 为指定类型，否则抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Expected {token_type} but found end of input at {parser_state.get('filename', 'unknown')}"
        )
    
    current_token = tokens[pos]
    if current_token["type"] != token_type:
        raise SyntaxError(
            f"Expected {token_type} but found {current_token['type']} "
            f"at line {current_token.get('line', 0)}, column {current_token.get('column', 0)}"
        )
    
    parser_state["pos"] += 1
    return current_token


# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
