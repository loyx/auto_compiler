# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_binary_op(parser_state: ParserState, left: AST, min_precedence: int) -> AST:
    """
    解析二元运算，处理运算符优先级。
    
    支持运算符：+ -（优先级 1），* /（优先级 2）
    """
    result = left
    
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # 检查是否还有 token
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        token_value = current_token.get("value", "")
        
        # 获取运算符优先级
        precedence = _get_operator_precedence(token_value)
        
        # 如果不是运算符或优先级不足，返回当前结果
        if precedence is None or precedence < min_precedence:
            break
        
        # 记录运算符信息
        op_token = current_token
        op_line = op_token.get("line", 0)
        op_column = op_token.get("column", 0)
        
        # 消费运算符 token
        parser_state["pos"] += 1
        
        # 解析右侧操作数
        right = _parse_primary(parser_state)
        
        # 递归处理右侧可能存在的更高优先级运算
        right = _parse_binary_op(parser_state, right, precedence + 1)
        
        # 构建二元运算 AST 节点
        result = {
            "type": "binary_op",
            "children": [result, right],
            "value": token_value,
            "line": op_line,
            "column": op_column
        }
    
    return result

# === helper functions ===
def _get_operator_precedence(token_value: str) -> int:
    """
    获取运算符优先级。
    
    返回：
    - 1: 加法/减法 (+, -)
    - 2: 乘法/除法 (*, /)
    - None: 不是二元运算符
    """
    if token_value in ("+", "-"):
        return 1
    elif token_value in ("*", "/"):
        return 2
    else:
        return None

def _raise_error(parser_state: ParserState, message: str) -> None:
    """
    抛出语法错误。
    
    错误格式：filename:line:column: message
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 0)
        column = token.get("column", 0)
    else:
        line = 0
        column = 0
    
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.
