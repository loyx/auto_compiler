# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_package._parse_logical_src import _parse_logical

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
def _parse_expression(parser_state: dict) -> dict:
    """
    解析完整表达式的主入口函数。
    
    按运算符优先级从低到高调用各层级解析函数：
    1. logical (AND, OR) - 最低优先级
    2. comparison (==, !=, <, >, <=, >=)
    3. additive (+, -)
    4. multiplicative (*, /, %)
    5. unary (NOT, -)
    6. primary (字面量、标识符、括号) - 最高优先级
    
    输入：parser_state（pos 指向表达式起始 token）
    输出：完整表达式 AST 节点
    副作用：修改 parser_state["pos"] 到表达式结束位置
    异常：语法错误时抛出 SyntaxError
    """
    # 从最低优先级开始解析（逻辑运算符）
    # 逻辑运算符内部会递归调用比较、加法、乘法、一元、初级解析
    return _parse_logical(parser_state)

# === helper functions ===
def _check_token(parser_state: ParserState, token_type: str, token_value: str = None) -> bool:
    """检查当前位置是否匹配指定 token。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    if token["type"] != token_type:
        return False
    if token_value is not None and token["value"] != token_value:
        return False
    return True

def _consume_token(parser_state: ParserState, token_type: str, token_value: str = None) -> Token:
    """消耗并返回当前 token，如果不匹配则抛出语法错误。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "unknown")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected {token_type}")
    
    token = tokens[pos]
    if token["type"] != token_type:
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Expected {token_type}, got {token['type']}")
    
    if token_value is not None and token["value"] != token_value:
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: Expected '{token_value}', got '{token['value']}'")
    
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
