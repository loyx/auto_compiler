# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_postfix_package._parse_postfix_src import _parse_postfix
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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
    解析通用表达式的主入口函数。
    处理字面量、标识符、一元/二元运算符、函数调用、容器字面量、索引/属性访问等。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return _make_error_node(parser_state, "Unexpected end of expression")
    
    # 1. 先解析一元运算符（如果有）
    current_token = tokens[pos]
    if current_token.get("type") == "OPERATOR" and current_token.get("value") in ("-", "not"):
        op_token = current_token
        parser_state["pos"] = pos + 1
        operand = _parse_expression(parser_state)
        return {
            "type": "UNARY_OP",
            "operator": op_token.get("value"),
            "operand": operand,
            "line": op_token.get("line"),
            "column": op_token.get("column")
        }
    
    # 2. 解析左侧基础表达式
    left = _parse_primary(parser_state)
    if left.get("type") == "ERROR":
        return left
    
    # 3. 解析后缀操作（函数调用、索引、属性访问）
    left = _parse_postfix(parser_state, left)
    if left.get("type") == "ERROR":
        return left
    
    # 4. 解析二元运算符（使用优先级爬升）
    result = _parse_binary_op(parser_state, 0, left)
    return result

# === helper functions ===
def _make_error_node(parser_state: ParserState, message: str) -> AST:
    """创建错误 AST 节点并设置 parser_state 的 error 字段。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    token = tokens[pos] if pos < len(tokens) else {}
    parser_state["error"] = message
    return {
        "type": "ERROR",
        "value": message,
        "line": token.get("line", 0),
        "column": token.get("column", 0)
    }

# === OOP compatibility layer ===
# Not required for this parser function node
