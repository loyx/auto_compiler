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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析条件表达式：expression := term ((PLUS | MINUS) term)*
    输入：parser_state（pos 指向表达式起始 token）
    输出：表达式 AST 节点
    副作用：更新 parser_state["pos"] 到表达式之后的位置
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 解析左侧 term
    left_ast = _parse_term(parser_state)
    
    # 处理后续的 PLUS/MINUS 运算符
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        token_type = current_token.get("type", "")
        
        if token_type not in ("PLUS", "MINUS"):
            break
        
        op_token = current_token
        parser_state["pos"] += 1
        
        # 解析右侧 term
        right_ast = _parse_term(parser_state)
        
        # 构建二元操作 AST 节点
        left_ast = {
            "type": "BINOP",
            "op": op_token["type"],
            "left": left_ast,
            "right": right_ast,
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left_ast

# === helper functions ===
def _expect_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    期望当前 token 是指定类型，否则抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    
    current_token = tokens[pos]
    if current_token.get("type") != expected_type:
        raise SyntaxError(
            f"Expected token type {expected_type}, got {current_token.get('type')} "
            f"at line {current_token.get('line', 0)}, column {current_token.get('column', 0)}"
        )
    
    parser_state["pos"] += 1
    return current_token

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
