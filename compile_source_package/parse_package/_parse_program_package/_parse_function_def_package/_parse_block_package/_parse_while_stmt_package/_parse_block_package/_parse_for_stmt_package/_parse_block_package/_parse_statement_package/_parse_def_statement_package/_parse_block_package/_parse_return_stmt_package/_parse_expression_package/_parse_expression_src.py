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
    解析表达式。
    
    表达式语法：
    expression := term ((PLUS | MINUS) term)*
    
    输入：parser_state（pos 指向表达式起始 token）
    输出：表达式 AST 节点（左结合的运算符树）
    副作用：更新 parser_state["pos"] 到表达式结束后的位置
    异常：遇到无法解析的 token 时抛出 SyntaxError
    """
    # 解析第一个 term
    left_node = _parse_term(parser_state)
    
    # 循环处理 PLUS/MINUS 运算符
    while True:
        token = _current_token(parser_state)
        if token is None:
            break
        if token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 消费运算符 token
        op_token = _consume_token(parser_state)
        
        # 解析右侧 term
        right_node = _parse_term(parser_state)
        
        # 构建左结合的 AST 节点
        left_node = {
            "type": op_token["type"],
            "line": op_token["line"],
            "column": op_token["column"],
            "children": [left_node, right_node]
        }
    
    return left_node


# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token，越界返回 None。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    return tokens[pos] if pos < len(tokens) else None


def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并前进 pos，返回被消费的 token。"""
    token = _current_token(parser_state)
    if token is None:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        raise SyntaxError(
            f"Unexpected end of input at line {tokens[-1]['line'] if tokens else 0}, "
            f"column {tokens[-1]['column'] if tokens else 0}"
        )
    parser_state["pos"] = pos + 1
    return token


# === OOP compatibility layer ===
# Not needed for this parser module
