# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or
from ._raise_error_package._raise_error_src import _raise_error

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
def _parse_conditional(parser_state: dict) -> dict:
    """解析条件表达式（三元运算符 ?:），优先级高于赋值运算符。"""
    # 步骤 1: 先调用下层解析函数获取条件部分
    condition = _parse_or(parser_state)
    
    # 步骤 2: 检查当前 token 是否为 `?`
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return condition
    
    current_token = tokens[pos]
    if current_token.get("value") != "?":
        return condition
    
    # 步骤 3: 如果是 `?`，解析三元表达式
    # 记录 `?` 的位置用于 AST 节点
    question_line = current_token.get("line", 0)
    question_column = current_token.get("column", 0)
    
    # 消耗 `?` token
    parser_state["pos"] = pos + 1
    
    # 调用下层解析函数获取真值分支表达式
    true_expr = _parse_or(parser_state)
    
    # 检查并消耗 `:` token
    pos = parser_state["pos"]
    if pos >= len(tokens):
        _raise_error(parser_state, "Expected ':' after conditional expression")
    
    colon_token = tokens[pos]
    if colon_token.get("value") != ":":
        _raise_error(parser_state, "Expected ':' after conditional expression")
    
    # 消耗 `:` token
    parser_state["pos"] = pos + 1
    
    # 调用下层解析函数获取假值分支表达式（右结合）
    false_expr = _parse_conditional(parser_state)
    
    # 返回 CONDITIONAL 类型的 AST 节点
    return {
        "type": "CONDITIONAL",
        "condition": condition,
        "true_expr": true_expr,
        "false_expr": false_expr,
        "line": question_line,
        "column": question_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
