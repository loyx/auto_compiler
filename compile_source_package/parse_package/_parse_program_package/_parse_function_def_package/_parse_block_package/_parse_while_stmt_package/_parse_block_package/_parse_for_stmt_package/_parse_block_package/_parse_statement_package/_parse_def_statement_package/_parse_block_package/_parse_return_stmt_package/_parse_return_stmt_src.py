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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """解析 return 语句。输入：parser_state（pos 指向 RETURN 关键字）。输出：RETURN AST 节点。"""
    # 消费 RETURN 关键字
    return_token = _expect_token(parser_state, "RETURN")
    start_line = return_token["line"]
    start_column = return_token["column"]
    
    # 检查是否有表达式
    current = _current_token(parser_state)
    expression_ast = None
    if current is not None and current["type"] != "SEMICOLON":
        expression_ast = _parse_expression(parser_state)
    
    # 消费 SEMICOLON
    _expect_token(parser_state, "SEMICOLON")
    
    return {
        "type": "RETURN",
        "line": start_line,
        "column": start_column,
        "children": [expression_ast] if expression_ast is not None else []
    }

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token，若越界则返回 None。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    return tokens[pos] if pos < len(tokens) else None

def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """验证当前 token 类型并消费。类型不匹配时抛 SyntaxError。"""
    token = _current_token(parser_state)
    if token is None or token["type"] != token_type:
        raise SyntaxError(
            f"Expected token type {token_type}, got {token['type'] if token else 'EOF'} "
            f"at line {token['line'] if token else 0}, column {token['column'] if token else 0}"
        )
    parser_state["pos"] += 1
    return token

def _advance(parser_state: ParserState) -> None:
    """前进到下一个 token。"""
    parser_state["pos"] += 1

# === OOP compatibility layer ===
