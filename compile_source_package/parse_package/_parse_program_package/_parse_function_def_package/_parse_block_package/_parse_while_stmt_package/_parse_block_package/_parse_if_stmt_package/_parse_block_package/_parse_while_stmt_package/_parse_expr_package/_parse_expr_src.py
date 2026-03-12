# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "args": list,
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
def _parse_expr(parser_state: dict) -> dict:
    """
    解析表达式入口函数。
    输入：parser_state（pos 指向表达式起始 token）
    输出：表达式的 AST 节点
    行为：调用最低优先级的解析函数开始递归下降解析
    """
    # 检查是否已有错误
    if parser_state.get("error"):
        return _make_invalid_node(parser_state)
    
    # 检查是否为空或已结束
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        _set_error(parser_state, "Unexpected end of input, expected expression")
        return _make_invalid_node(parser_state)
    
    # 从最低优先级开始解析（OR 表达式）
    result = _parse_or(parser_state)
    
    return result

# === helper functions ===
def _make_invalid_node(parser_state: dict) -> dict:
    """创建无效的 AST 节点。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    line = tokens[pos]["line"] if pos < len(tokens) else 0
    column = tokens[pos]["column"] if pos < len(tokens) else 0
    return {"type": "INVALID", "value": None, "line": line, "column": column}

def _set_error(parser_state: dict, description: str) -> None:
    """设置错误信息。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    line = tokens[pos]["line"] if pos < len(tokens) else 0
    column = tokens[pos]["column"] if pos < len(tokens) else 0
    filename = parser_state.get("filename", "unknown")
    parser_state["error"] = f"{filename}:{line}:{column}: error: {description}"

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
